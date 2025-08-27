"""
@Remark: 自定义序列化器
"""
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from django.utils.functional import cached_property
from rest_framework.utils.serializer_helpers import BindingDict


class AuditUserFieldsMixin:
    """
    用于自动赋值 creator 和 modifier 字段的 Mixin
    """
    # 修改人的审计字段名称, 默认modifier, 继承使用时可自定义覆盖
    modifier_field_id = 'modifier'
    # 创建人的审计字段名称, 默认creator, 继承使用时可自定义覆盖
    creator_field_id = 'creator'

    def set_audit_user_fields(self, validated_data, is_create=True):
        username = self.get_request_user_name() if hasattr(self, 'get_request_user_name') else None
        if getattr(self, 'request', None):
            if self.modifier_field_id in self.fields:
                validated_data[self.modifier_field_id] = username
            if is_create and self.creator_field_id in self.fields:
                validated_data[self.creator_field_id] = username


class DesensitizationMixin:
    """
    用于敏感字段脱敏的通用 Mixin
    使用方法：
    1. 在序列化器中继承此 Mixin
    2. 设置 desensitize_fields 属性，指定需要脱敏的字段
    3. 可选：设置 desensitize_prefix_length 和 desensitize_suffix_length 来自定义脱敏格式
    """
    
    # 需要脱敏的字段列表，格式：['field_name', 'related_field.field_name']
    desensitize_fields = []
    
    # 脱敏时保留的前缀长度，默认4
    desensitize_prefix_length = 4
    
    # 脱敏时保留的后缀长度，默认4
    desensitize_suffix_length = 4
    
    # 脱敏阈值，字段长度小于等于此值时全部用*替换，默认8
    desensitize_threshold = 8
    
    # 脱敏字符，默认使用*
    desensitize_char = '*'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个脱敏字段创建脱敏方法
        for field_name in self.desensitize_fields:
            if '.' in field_name:
                # 处理关联字段，如 'key.api_key'
                method_name = f'get_{field_name.replace(".", "_")}_desensitized'
                setattr(self, method_name, self._create_desensitize_method(field_name))
            else:
                # 处理直接字段
                method_name = f'get_{field_name}_desensitized'
                setattr(self, method_name, self._create_desensitize_method(field_name))
    
    def _create_desensitize_method(self, field_name):
        """创建脱敏方法的闭包"""
        def desensitize_method(obj):
            return self._desensitize_field(obj, field_name)
        return desensitize_method
    
    def _desensitize_field(self, obj, field_name):
        """脱敏指定字段"""
        if '.' in field_name:
            # 处理关联字段，如 'key.api_key'
            parts = field_name.split('.')
            value = obj
            for part in parts:
                if hasattr(value, part):
                    value = getattr(value, part)
                else:
                    return None
        else:
            # 处理直接字段
            if not hasattr(obj, field_name):
                return None
            value = getattr(obj, field_name)
        
        # 如果值为空，直接返回
        if not value:
            return value

        # 检查用户权限
        if self._can_view_full_value():
            return value

        # 执行脱敏
        return self._apply_desensitization(str(value))
    
    def _can_view_full_value(self):
        """检查当前用户是否可以查看完整值"""
        # request = self.context.get('request')
        # if not request or not request.user:
        #     return False
        #
        # # 超级用户或管理员可以查看完整值
        # return request.user.is_superuser or request.user.is_staff
        return False  # 默认不允许查看完整值，需根据实际权限逻辑调整

    def _apply_desensitization(self, value):
        """应用脱敏规则"""
        if len(value) <= self.desensitize_threshold:
            # 如果长度小于等于阈值，则全部用脱敏字符替换
            return self.desensitize_char * len(value)
        else:
            # 显示前缀和后缀，中间用脱敏字符替换
            prefix = value[:self.desensitize_prefix_length]
            suffix = value[-self.desensitize_suffix_length:]
            middle_length = len(value) - self.desensitize_prefix_length - self.desensitize_suffix_length
            middle = self.desensitize_char * middle_length
            return prefix + middle + suffix
    
    def get_fields(self):
        """重写 get_fields 方法，为脱敏字段添加脱敏版本"""
        fields = super().get_fields()

        is_list = getattr(self.root, 'many', False)

        for field_name in self.desensitize_fields:
            if '.' in field_name:
                # 处理关联字段，如 'key.api_key'
                method_name = f'get_{field_name.replace(".", "_")}_desensitized'
                field_key = f"{field_name.replace('.', '_')}_desensitized"
            else:
                # 处理直接字段
                method_name = f'get_{field_name}_desensitized'
                field_key = f"{field_name}_desensitized"
            
            # 创建脱敏字段的 SerializerMethodField
            fields[field_key] = serializers.SerializerMethodField(method_name=method_name)
            
            # 保持原字段不变，确保创建/更新功能正常
            # 原字段仍然可以接收输入数据
            if is_list:
                # 如果是列表序列化，移除原始字段
                fields.pop(field_name, None)

        return fields


class CustomModelSerializer(AuditUserFieldsMixin, ModelSerializer):
    """
    增强DRF的ModelSerializer,可自动更新模型的审计字段记录
    (1)self.request能获取到rest_framework.request.Request对象
    """
    # 添加默认时间返回格式
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request or self.context.get('request', None)

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        self.set_audit_user_fields(validated_data, is_create=True)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.set_audit_user_fields(validated_data, is_create=False)
        return super().update(instance, validated_data)

    def get_request_username(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'username', None)
        return None

    def get_request_name(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'name', None)
        return None

    def get_request_user_id(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'id', None)
        return None

    @cached_property
    def fields(self):
        fields = BindingDict(self)
        for key, value in self.get_fields().items():
            fields[key] = value

        if not hasattr(self, '_context'):
            return fields
        is_root = self.root == self
        parent_is_list_root = self.parent == self.root and getattr(self.parent, 'many', False)
        if not (is_root or parent_is_list_root):
            return fields

        try:
            request = self.request or self.context['request']
        except KeyError:
            return fields
        params = getattr(
            request, 'query_params', getattr(request, 'GET', None)
        )
        if params is None:
            pass
        try:
            filter_fields = params.get('_fields', None).split(',')
        except AttributeError:
            filter_fields = None

        try:
            omit_fields = params.get('_exclude', None).split(',')
        except AttributeError:
            omit_fields = []

        existing = set(fields.keys())
        if filter_fields is None:
            allowed = existing
        else:
            allowed = set(filter(None, filter_fields))

        omitted = set(filter(None, omit_fields))
        for field in existing:
            if field not in allowed:
                fields.pop(field, None)
            if field in omitted:
                fields.pop(field, None)

        return fields
