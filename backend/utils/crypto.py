import os
import json
import base64
from typing import Optional, Union, Dict, Any

from django.conf import settings
from django.core.exceptions import ValidationError
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoUtils:
    """简洁高效的加解密工具类"""
    
    DEFAULT_ITERATIONS = 310000
    SALT_LENGTH = 16
    
    @classmethod
    def _get_default_key(cls) -> bytes:
        """从Django AES_KEY生成默认密钥"""
        _key = getattr(settings, 'AES_KEY', None)
        _salt = getattr(settings, 'AES_SALT', None)
        if not _key:
            raise ValidationError('Django AES_KEY未配置')
        if not _salt:
            raise CryptoError('Django AES_SALT 未配置')
        
        # 使用AES_KEY生成固定的Fernet密钥
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=_salt.encode('utf-8'),  # 固定盐值，确保密钥一致性
            iterations=cls.DEFAULT_ITERATIONS,
        )
        return base64.urlsafe_b64encode(kdf.derive(_key.encode('utf-8')))
    
    @classmethod
    def _derive_key(cls, password: str, salt: bytes) -> bytes:
        """从密码和盐值派生密钥"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=cls.DEFAULT_ITERATIONS,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
    
    @classmethod
    def encrypt(cls, data: str, key: Optional[bytes] = None) -> str:
        """加密字符串"""
        if not data:
            raise ValidationError('待加密数据不能为空')
        
        if key is None:
            key = cls._get_default_key()
        
        try:
            f = Fernet(key)
            encrypted_data = f.encrypt(data.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            raise ValidationError(f'加密失败: {str(e)}')
    
    @classmethod
    def decrypt(cls, encrypted_data: str, key: Optional[bytes] = None) -> str:
        """解密字符串"""
        if not encrypted_data:
            raise ValidationError('待解密数据不能为空')
        
        if key is None:
            key = cls._get_default_key()
        
        try:
            f = Fernet(key)
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = f.decrypt(decoded_data)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise ValidationError(f'解密失败: {str(e)}')
    
    @classmethod
    def encrypt_with_password(cls, data: str, password: str) -> Dict[str, str]:
        """使用密码加密数据，返回加密数据和盐值"""
        if not password:
            raise ValidationError('密码不能为空')
        
        salt = os.urandom(cls.SALT_LENGTH)
        key = cls._derive_key(password, salt)
        encrypted_data = cls.encrypt(data, key)
        
        return {
            'encrypted_data': encrypted_data,
            'salt': base64.urlsafe_b64encode(salt).decode('utf-8')
        }
    
    @classmethod
    def decrypt_with_password(cls, encrypted_data: str, password: str, salt: str) -> str:
        """使用密码解密数据"""
        if not password or not salt:
            raise ValidationError('密码和盐值不能为空')
        
        try:
            salt_bytes = base64.urlsafe_b64decode(salt.encode('utf-8'))
            key = cls._derive_key(password, salt_bytes)
            return cls.decrypt(encrypted_data, key)
        except Exception as e:
            raise ValidationError(f'解密失败: {str(e)}')


# 便捷函数
def encrypt_text(text: str, password: Optional[str] = None) -> Union[str, Dict[str, str]]:
    """
    加密文本
    :param text: 要加密的文本
    :param password: 可选密码，不提供则使用AES_KEY
    :return: 加密结果，使用密码时返回字典，否则返回字符串
    """
    if password:
        return CryptoUtils.encrypt_with_password(text, password)
    return CryptoUtils.encrypt(text)


def decrypt_text(encrypted_data: str, password: Optional[str] = None, salt: Optional[str] = None) -> str:
    """
    解密文本
    :param encrypted_data: 加密后的文本
    :param password: 可选密码
    :param salt: 使用密码时必需的盐值
    :return: 解密后的原始文本
    """
    if password:
        if not salt:
            raise ValidationError('使用密码解密时必须提供盐值')
        return CryptoUtils.decrypt_with_password(encrypted_data, password, salt)
    return CryptoUtils.decrypt(encrypted_data)


def encrypt_file(file_path: str, output_path: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
    """加密文件"""
    if not os.path.exists(file_path):
        raise ValidationError(f'文件不存在: {file_path}')
    
    output_path = output_path or f"{file_path}.enc"
    
    try:
        with open(file_path, 'rb') as f:
            file_data = base64.urlsafe_b64encode(f.read()).decode('utf-8')
        
        if password:
            result = CryptoUtils.encrypt_with_password(file_data, password)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f)
            return {'encrypted_file': output_path, 'salt': result['salt']}
        else:
            encrypted_data = CryptoUtils.encrypt(file_data)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_data)
            return {'encrypted_file': output_path}
            
    except Exception as e:
        raise ValidationError(f'文件加密失败: {str(e)}')


def decrypt_file(encrypted_file_path: str, output_path: Optional[str] = None, password: Optional[str] = None) -> str:
    """解密文件"""
    if not os.path.exists(encrypted_file_path):
        raise ValidationError(f'加密文件不存在: {encrypted_file_path}')
    
    if output_path is None:
        output_path = encrypted_file_path[:-4] if encrypted_file_path.endswith('.enc') else f"{encrypted_file_path}.dec"
    
    try:
        with open(encrypted_file_path, 'r', encoding='utf-8') as f:
            if password:
                data = json.load(f)
                decrypted_data_b64 = CryptoUtils.decrypt_with_password(
                    data['encrypted_data'], password, data['salt']
                )
            else:
                encrypted_data = f.read()
                decrypted_data_b64 = CryptoUtils.decrypt(encrypted_data)
        
        file_data = base64.urlsafe_b64decode(decrypted_data_b64.encode('utf-8'))
        
        with open(output_path, 'wb') as f:
            f.write(file_data)
        
        return output_path
        
    except Exception as e:
        raise ValidationError(f'文件解密失败: {str(e)}')


# # Simple encryption using AES_KEY
# encrypted = encrypt_text("sensitive data")
# decrypted = decrypt_text(encrypted)

# # Password-based encryption
# result = encrypt_text("data", password="mypassword")
# decrypted = decrypt_text(result['encrypted_data'], password="mypassword", salt=result['salt'])

# # File encryption
# encrypt_file("document.pdf")  # Uses AES_KEY
# encrypt_file("document.pdf", password="mypassword")  # Uses password