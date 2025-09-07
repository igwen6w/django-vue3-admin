from django.db import models
from django.core.exceptions import ValidationError
from utils.crypto import CryptoUtils


class EncryptedTextField(models.TextField):
    """
    加密文本字段，自动加解密存储的数据
    使用 backend.utils.crypto 中的 CryptoUtils 进行加解密操作
    """
    
    description = "加密文本字段"
    
    def __init__(self, *args, **kwargs):
        # 移除自定义参数，避免传递给父类
        self.use_password = kwargs.pop('use_password', False)
        self.password_field = kwargs.pop('password_field', None)
        super().__init__(*args, **kwargs)
    
    def from_db_value(self, value, expression, connection):
        """从数据库读取时自动解密"""
        if value is None:
            return value
        
        try:
            return CryptoUtils.decrypt(value)
        except Exception as e:
            # 如果解密失败，可能是未加密的旧数据，直接返回
            return value
    
    def to_python(self, value):
        """转换为Python对象时的处理"""
        if value is None:
            return value
        
        # 如果已经是解密后的字符串，直接返回
        if isinstance(value, str):
            return value
        
        return str(value)
    
    def get_prep_value(self, value):
        """保存到数据库前自动加密"""
        if value is None:
            return value
        
        # 确保是字符串
        value = str(value)
        
        if not value:
            return value
        
        try:
            return CryptoUtils.encrypt(value)
        except Exception as e:
            raise ValidationError(f'字段加密失败: {str(e)}')
    
    def value_to_string(self, obj):
        """序列化时的处理"""
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
    
    def deconstruct(self):
        """用于迁移文件生成"""
        name, path, args, kwargs = super().deconstruct()
        if self.use_password:
            kwargs['use_password'] = self.use_password
        if self.password_field:
            kwargs['password_field'] = self.password_field
        return name, path, args, kwargs


class EncryptedCharField(models.CharField):
    """
    加密字符字段，自动加解密存储的数据
    适用于较短的加密文本
    """
    
    description = "加密字符字段"
    
    def __init__(self, *args, **kwargs):
        # 加密后的数据会比原始数据长，需要调整max_length
        if 'max_length' in kwargs:
            # Fernet加密后的数据大约是原始数据的1.3-1.4倍，再加上base64编码
            kwargs['max_length'] = max(kwargs['max_length'] * 2, 500)
        super().__init__(*args, **kwargs)
    
    def from_db_value(self, value, expression, connection):
        """从数据库读取时自动解密"""
        if value is None:
            return value
        
        try:
            return CryptoUtils.decrypt(value)
        except Exception as e:
            # 如果解密失败，可能是未加密的旧数据，直接返回
            return value
    
    def to_python(self, value):
        """转换为Python对象时的处理"""
        if value is None:
            return value
        
        if isinstance(value, str):
            return value
        
        return str(value)
    
    def get_prep_value(self, value):
        """保存到数据库前自动加密"""
        if value is None:
            return value
        
        value = str(value)
        
        if not value:
            return value
        
        try:
            return CryptoUtils.encrypt(value)
        except Exception as e:
            raise ValidationError(f'字段加密失败: {str(e)}')