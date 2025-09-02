"""
脱敏功能使用示例

这个文件展示了如何在不同的序列化器中使用 DesensitizationMixin 来实现字段脱敏
"""

from utils.serializers import CustomModelSerializer, DesensitizationMixin


# 示例1：基本用法 - 脱敏单个字段
class BasicDesensitizationExample(DesensitizationMixin, CustomModelSerializer):
    """
    基本脱敏示例
    """
    # 指定需要脱敏的字段
    desensitize_fields = ['password', 'api_key', 'secret_token']
    
    class Meta:
        model = None  # 这里应该是您的模型
        fields = '__all__'


# 示例2：自定义脱敏格式
class CustomDesensitizationExample(DesensitizationMixin, CustomModelSerializer):
    """
    自定义脱敏格式示例
    """
    # 指定需要脱敏的字段
    desensitize_fields = ['credit_card', 'phone_number', 'id_card']
    
    # 自定义脱敏参数
    desensitize_prefix_length = 2      # 保留前2位
    desensitize_suffix_length = 2      # 保留后2位
    desensitize_threshold = 6          # 长度小于等于6时全部脱敏
    desensitize_char = '#'             # 使用#作为脱敏字符
    
    class Meta:
        model = None
        fields = '__all__'


# 示例3：脱敏关联字段
class RelatedFieldDesensitizationExample(DesensitizationMixin, CustomModelSerializer):
    """
    脱敏关联字段示例
    """
    # 脱敏关联字段，使用点号分隔
    desensitize_fields = [
        'user.password',           # 用户密码
        'user.email',              # 用户邮箱
        'config.api_key',          # 配置中的API密钥
        'payment.credit_card',     # 支付信息中的信用卡
        'profile.phone_number'     # 个人资料中的电话号码
    ]
    
    class Meta:
        model = None
        fields = '__all__'


# 示例4：混合脱敏和普通字段
class MixedDesensitizationExample(DesensitizationMixin, CustomModelSerializer):
    """
    混合脱敏和普通字段示例
    """
    from rest_framework import serializers
    
    # 脱敏字段
    desensitize_fields = ['secret_key', 'user.password']
    
    # 普通字段
    name = serializers.CharField()
    description = serializers.CharField()
    
    # 计算字段
    full_name = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    class Meta:
        model = None
        fields = '__all__'


# 示例5：条件脱敏
class ConditionalDesensitizationExample(DesensitizationMixin, CustomModelSerializer):
    """
    条件脱敏示例
    """
    desensitize_fields = ['api_key', 'secret_token']
    
    def _can_view_full_value(self):
        """
        重写权限检查方法，实现自定义权限逻辑
        """
        request = self.context.get('request')
        if not request or not request.user:
            return False
        
        # 检查特定权限
        if request.user.has_perm('app.view_sensitive_data'):
            return True
        
        # 检查角色
        if request.user.role.filter(name='数据管理员').exists():
            return True
        
        # 检查用户组
        if request.user.groups.filter(name='高级用户').exists():
            return True
        
        # 默认只有超级用户和管理员可以查看
        return request.user.is_superuser or request.user.is_staff


# 示例6：不同字段使用不同脱敏规则
class MultiRuleDesensitizationExample(DesensitizationMixin, CustomModelSerializer):
    """
    不同字段使用不同脱敏规则的示例
    注意：这个示例需要自定义实现，因为 DesensitizationMixin 使用统一的规则
    """
    desensitize_fields = ['api_key', 'phone_number', 'credit_card']
    
    def _apply_desensitization(self, value):
        """
        重写脱敏方法，为不同字段应用不同规则
        """
        # 这里可以根据字段名或其他逻辑来应用不同的脱敏规则
        # 由于 DesensitizationMixin 的设计，这个示例需要额外的自定义逻辑
        return super()._apply_desensitization(value)


# 使用说明
"""
使用 DesensitizationMixin 的步骤：

1. 在序列化器中继承 DesensitizationMixin
   class MySerializer(DesensitizationMixin, CustomModelSerializer):
       pass

2. 设置需要脱敏的字段
   desensitize_fields = ['field1', 'field2', 'related.field3']

3. 可选：自定义脱敏参数
   desensitize_prefix_length = 3      # 保留前3位
   desensitize_suffix_length = 3      # 保留后3位
   desensitize_threshold = 10         # 长度小于等于10时全部脱敏
   desensitize_char = 'X'             # 使用X作为脱敏字符

4. 可选：重写权限检查方法
   def _can_view_full_value(self):
       # 自定义权限逻辑
       pass

5. 可选：重写脱敏方法
   def _apply_desensitization(self, value):
       # 自定义脱敏规则
       pass

注意事项：
- 脱敏字段会自动转换为 SerializerMethodField
- 关联字段使用点号分隔，如 'user.password'
- 脱敏只影响显示，不影响数据库存储
- 超级用户和管理员默认可以查看完整值
- 可以通过重写方法来扩展功能
""" 