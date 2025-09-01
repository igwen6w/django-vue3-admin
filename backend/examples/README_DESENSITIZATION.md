# 通用脱敏解决方案

## 概述

为了保护敏感信息，系统提供了一个通用的脱敏 Mixin (`DesensitizationMixin`)，可以轻松应用到任何序列化器中，实现字段的自动脱敏。

## 核心特性

- **通用性**：一个 Mixin 解决所有脱敏需求
- **灵活性**：支持直接字段和关联字段脱敏
- **可配置**：可自定义脱敏格式和权限规则
- **易使用**：只需几行代码即可启用脱敏
- **权限控制**：超级用户和管理员可查看完整值

## 快速开始

### 1. 基本用法

```python
from utils.serializers import CustomModelSerializer, DesensitizationMixin

class MySerializer(DesensitizationMixin, CustomModelSerializer):
    # 指定需要脱敏的字段
    desensitize_fields = ['password', 'api_key', 'secret_token']
    
    class Meta:
        model = MyModel
        fields = '__all__'
```

### 2. 脱敏关联字段

```python
class UserProfileSerializer(DesensitizationMixin, CustomModelSerializer):
    # 脱敏关联字段，使用点号分隔
    desensitize_fields = [
        'user.password',           # 用户密码
        'user.email',              # 用户邮箱
        'config.api_key',          # 配置中的API密钥
        'payment.credit_card'      # 支付信息中的信用卡
    ]
    
    class Meta:
        model = UserProfile
        fields = '__all__'
```

### 3. 自定义脱敏格式

```python
class CustomSerializer(DesensitizationMixin, CustomModelSerializer):
    desensitize_fields = ['credit_card', 'phone_number']
    
    # 自定义脱敏参数
    desensitize_prefix_length = 2      # 保留前2位
    desensitize_suffix_length = 2      # 保留后2位
    desensitize_threshold = 6          # 长度小于等于6时全部脱敏
    desensitize_char = '#'             # 使用#作为脱敏字符
    
    class Meta:
        model = MyModel
        fields = '__all__'
```

## 脱敏规则

### 默认脱敏格式
- **长度 ≤ 8 的字段**：全部用 `*` 替换
  - 例如：`sk-123` → `*****`
- **长度 > 8 的字段**：显示前4位和后4位，中间用 `*` 替换
  - 例如：`sk-1234567890abcdefghijklmnopqrstuvwxyz` → `sk-12****************************wxyz`

### 权限控制
- **超级用户 (`is_superuser=True`)**：可以查看完整的值
- **管理员用户 (`is_staff=True`)**：可以查看完整的值
- **普通用户**：只能查看脱敏后的值

## 配置选项

### 基本配置

```python
class MySerializer(DesensitizationMixin, CustomModelSerializer):
    # 需要脱敏的字段列表
    desensitize_fields = ['field1', 'field2', 'related.field3']
    
    # 脱敏时保留的前缀长度，默认4
    desensitize_prefix_length = 4
    
    # 脱敏时保留的后缀长度，默认4
    desensitize_suffix_length = 4
    
    # 脱敏阈值，字段长度小于等于此值时全部脱敏，默认8
    desensitize_threshold = 8
    
    # 脱敏字符，默认使用*
    desensitize_char = '*'
```

### 高级配置

```python
class AdvancedSerializer(DesensitizationMixin, CustomModelSerializer):
    desensitize_fields = ['secret_key', 'user.password']
    
    def _can_view_full_value(self):
        """重写权限检查方法，实现自定义权限逻辑"""
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
    
    def _apply_desensitization(self, value):
        """重写脱敏方法，实现自定义脱敏规则"""
        # 自定义脱敏逻辑
        if len(value) <= 6:
            return '#' * len(value)
        else:
            return value[:2] + '#' * (len(value) - 4) + value[-2:]
```

## 实际应用示例

### 示例1：用户信息脱敏

```python
class UserSerializer(DesensitizationMixin, CustomModelSerializer):
    desensitize_fields = [
        'password',           # 密码
        'email',              # 邮箱
        'phone_number',       # 电话号码
        'id_card_number'      # 身份证号
    ]
    
    class Meta:
        model = User
        fields = '__all__'
```

### 示例2：支付信息脱敏

```python
class PaymentSerializer(DesensitizationMixin, CustomModelSerializer):
    desensitize_fields = [
        'credit_card_number',     # 信用卡号
        'cvv',                    # CVV码
        'user.password',          # 用户密码
        'user.email'              # 用户邮箱
    ]
    
    # 为信用卡号使用更严格的脱敏
    desensitize_prefix_length = 2
    desensitize_suffix_length = 2
    desensitize_threshold = 10
    
    class Meta:
        model = Payment
        fields = '__all__'
```

### 示例3：系统配置脱敏

```python
class SystemConfigSerializer(DesensitizationMixin, CustomModelSerializer):
    desensitize_fields = [
        'database_password',      # 数据库密码
        'redis_password',         # Redis密码
        'api_keys.openai_key',    # OpenAI API密钥
        'api_keys.aws_secret'     # AWS密钥
    ]
    
    class Meta:
        model = SystemConfig
        fields = '__all__'
```

## 字段映射规则

### 直接字段
- 字段名：`password` → 序列化后字段名：`password`

### 关联字段
- 字段名：`user.password` → 序列化后字段名：`user_password`
- 字段名：`config.api_key` → 序列化后字段名：`config_api_key`

### 注意事项
- 脱敏字段会自动转换为 `SerializerMethodField`
- 原字段会被移除，避免重复
- 关联字段的脱敏会创建新的方法字段

## 测试

### 运行测试

```bash
cd backend
python manage.py test ai.tests.DesensitizationMixinTest
python manage.py test ai.tests.AIApiKeyDesensitizationTest
```

### 测试用例

```python
def test_desensitization_mixin_inheritance(self):
    """测试脱敏 Mixin 是否正确继承"""
    serializer = AIApiKeySerializer()
    
    # 验证序列化器有脱敏相关的方法
    self.assertTrue(hasattr(serializer, '_desensitize_field'))
    self.assertTrue(hasattr(serializer, '_can_view_full_value'))
    self.assertTrue(hasattr(serializer, '_apply_desensitization'))

def test_desensitization_fields_configuration(self):
    """测试脱敏字段配置"""
    serializer = AIApiKeySerializer()
    
    # 验证脱敏字段配置
    self.assertIn('api_key', serializer.desensitize_fields)
    self.assertEqual(serializer.desensitize_prefix_length, 4)
    self.assertEqual(serializer.desensitize_suffix_length, 4)
```

## 故障排除

### 常见问题

1. **脱敏不生效**
   - 检查是否正确继承了 `DesensitizationMixin`
   - 确认 `desensitize_fields` 配置正确
   - 验证序列化器是否正确设置了 `context`

2. **关联字段脱敏失败**
   - 检查关联字段路径是否正确（使用点号分隔）
   - 确认关联对象存在且可访问
   - 验证字段名拼写正确

3. **权限检查失败**
   - 检查用户是否已登录
   - 验证 `is_superuser` 和 `is_staff` 字段
   - 确认 `_can_view_full_value` 方法实现正确

### 调试方法

```python
# 在序列化器中添加调试信息
def _desensitize_field(self, obj, field_name):
    """脱敏指定字段"""
    print(f"脱敏字段: {field_name}")
    print(f"对象: {obj}")
    
    # 继续原有的脱敏逻辑
    return super()._desensitize_field(obj, field_name)

def _can_view_full_value(self):
    """检查当前用户是否可以查看完整值"""
    request = self.context.get('request')
    print(f"Request: {request}")
    print(f"User: {request.user if request else 'None'}")
    
    # 继续原有的权限检查逻辑
    return super()._can_view_full_value()
```

## 性能考虑

- 脱敏字段会转换为 `SerializerMethodField`，可能影响性能
- 对于大量数据的场景，建议只对必要的敏感字段启用脱敏
- 可以考虑使用缓存来优化重复的脱敏计算

## 扩展功能

### 自定义脱敏规则

```python
class CustomDesensitizationMixin(DesensitizationMixin):
    """自定义脱敏 Mixin"""
    
    def _apply_desensitization(self, value):
        """实现自定义脱敏规则"""
        # 根据字段类型应用不同的脱敏规则
        if self._is_credit_card(value):
            return self._desensitize_credit_card(value)
        elif self._is_phone_number(value):
            return self._desensitize_phone_number(value)
        else:
            return super()._apply_desensitization(value)
    
    def _is_credit_card(self, value):
        """判断是否为信用卡号"""
        return len(value) == 16 and value.isdigit()
    
    def _desensitize_credit_card(self, value):
        """信用卡号脱敏：前4位 + 8个* + 后4位"""
        return value[:4] + '*' * 8 + value[-4:]
```

### 批量脱敏

```python
class BatchDesensitizationMixin(DesensitizationMixin):
    """批量脱敏 Mixin"""
    
    def _batch_desensitize(self, obj_list):
        """批量脱敏对象列表"""
        for obj in obj_list:
            for field_name in self.desensitize_fields:
                if hasattr(obj, field_name):
                    setattr(obj, f'_{field_name}_desensitized', 
                           self._desensitize_field(obj, field_name))
        return obj_list
```

## 更新日志

- **v1.0.0**：初始实现，支持基本字段脱敏
- **v1.1.0**：添加关联字段脱敏支持
- **v1.2.0**：支持自定义脱敏参数和权限规则
- **v1.3.0**：添加完整的测试用例和文档
- **v2.0.0**：重构为通用 Mixin，支持所有序列化器 