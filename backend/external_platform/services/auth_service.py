# -*- coding: utf-8 -*-

"""
认证服务
提供统一的认证状态管理接口
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from django.utils import timezone
from django.db import transaction

from external_platform.models import Platform, AuthSession
from external_platform.choices import PlatformAuthStatus

logger = logging.getLogger(__name__)


class AuthService:
    """认证服务类，提供统一的认证状态管理"""
    
    @staticmethod
    def get_valid_session(platform_sign: str, account: str) -> Optional[AuthSession]:
        """获取有效的认证会话
        
        Args:
            platform_sign: 平台标识
            account: 账户名
            
        Returns:
            有效的AuthSession实例，如果不存在则返回None
        """
        logger.debug(f"查询有效会话 - 平台: {platform_sign}, 账户: {account}")
        
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            logger.warning(f"平台不存在 - 标识: {platform_sign}")
            return None
        
        try:
            session = AuthSession.objects.get(
                platform=platform,
                account=account,
                is_deleted=False
            )
            
            # 检查会话是否有效
            if AuthService.is_session_valid(session):
                logger.debug(f"找到有效会话 - 平台: {platform_sign}, 账户: {account}, "
                           f"会话ID: {session.id}")
                return session
            else:
                logger.debug(f"会话已过期 - 平台: {platform_sign}, 账户: {account}, "
                           f"会话ID: {session.id}")
                # 更新会话状态为过期
                AuthService.mark_session_expired(session)
                return None
                
        except AuthSession.DoesNotExist:
            logger.debug(f"未找到会话 - 平台: {platform_sign}, 账户: {account}")
            return None
        except Exception as e:
            logger.error(f"查询会话异常 - 平台: {platform_sign}, 账户: {account}, "
                        f"错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def is_session_valid(session: AuthSession) -> bool:
        """检查会话是否有效
        
        Args:
            session: AuthSession实例
            
        Returns:
            会话是否有效
        """
        if not session:
            return False
        
        # 检查状态
        if session.status != PlatformAuthStatus.ACTIVE:
            logger.debug(f"会话状态无效 - 会话ID: {session.id}, 状态: {session.status}")
            return False
        
        # 检查过期时间
        if session.expire_time and session.expire_time <= timezone.now():
            logger.debug(f"会话已过期 - 会话ID: {session.id}, "
                        f"过期时间: {session.expire_time}")
            return False
        
        # 检查认证信息
        if not session.auth:
            logger.debug(f"会话缺少认证信息 - 会话ID: {session.id}")
            return False
        
        return True

    @staticmethod
    def mark_session_expired(session: AuthSession) -> bool:
        """标记会话为过期状态
        
        Args:
            session: AuthSession实例
            
        Returns:
            操作是否成功
        """
        try:
            with transaction.atomic():
                session.status = PlatformAuthStatus.EXPIRED
                session.save(update_fields=['status', 'update_time'])
                
            logger.info(f"会话已标记为过期 - 会话ID: {session.id}, "
                       f"平台: {session.platform.sign}, 账户: {session.account}")
            return True
            
        except Exception as e:
            logger.error(f"标记会话过期失败 - 会话ID: {session.id}, "
                        f"错误: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def create_or_update_session(platform_sign: str, account: str, 
                               auth_data: Dict[str, Any], 
                               expire_hours: int = 24) -> Optional[AuthSession]:
        """创建或更新认证会话
        
        Args:
            platform_sign: 平台标识
            account: 账户名
            auth_data: 认证数据（如Cookie等）
            expire_hours: 过期小时数
            
        Returns:
            AuthSession实例，失败返回None
        """
        logger.info(f"创建或更新会话 - 平台: {platform_sign}, 账户: {account}")
        
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            logger.error(f"平台不存在 - 标识: {platform_sign}")
            return None
        
        try:
            with transaction.atomic():
                # 计算过期时间
                expire_time = timezone.now() + timedelta(hours=expire_hours)
                login_time = timezone.now()
                
                # 尝试更新现有会话
                session, created = AuthSession.objects.update_or_create(
                    platform=platform,
                    account=account,
                    defaults={
                        'auth': auth_data,
                        'status': PlatformAuthStatus.ACTIVE,
                        'expire_time': expire_time,
                        'login_time': login_time,
                        'is_deleted': False
                    }
                )
                
                action = "创建" if created else "更新"
                logger.info(f"会话{action}成功 - 会话ID: {session.id}, "
                           f"平台: {platform_sign}, 账户: {account}, "
                           f"过期时间: {expire_time}")
                
                return session
                
        except Exception as e:
            logger.error(f"创建或更新会话失败 - 平台: {platform_sign}, 账户: {account}, "
                        f"错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def get_sessions_near_expiry(hours_before_expiry: int = 2) -> list:
        """获取即将过期的会话列表
        
        Args:
            hours_before_expiry: 过期前多少小时算作即将过期
            
        Returns:
            即将过期的AuthSession列表
        """
        threshold_time = timezone.now() + timedelta(hours=hours_before_expiry)
        
        try:
            sessions = AuthSession.objects.filter(
                status=PlatformAuthStatus.ACTIVE,
                expire_time__lte=threshold_time,
                expire_time__gt=timezone.now(),
                is_deleted=False
            ).select_related('platform')
            
            session_list = list(sessions)
            logger.info(f"查询到{len(session_list)}个即将过期的会话")
            
            return session_list
            
        except Exception as e:
            logger.error(f"查询即将过期会话失败 - 错误: {str(e)}", exc_info=True)
            return []

    @staticmethod
    def get_expired_sessions() -> list:
        """获取已过期但状态未更新的会话列表
        
        Returns:
            已过期的AuthSession列表
        """
        try:
            sessions = AuthSession.objects.filter(
                status=PlatformAuthStatus.ACTIVE,
                expire_time__lte=timezone.now(),
                is_deleted=False
            ).select_related('platform')
            
            session_list = list(sessions)
            logger.info(f"查询到{len(session_list)}个已过期的会话")
            
            return session_list
            
        except Exception as e:
            logger.error(f"查询已过期会话失败 - 错误: {str(e)}", exc_info=True)
            return []

    @staticmethod
    def cleanup_expired_sessions() -> int:
        """清理已过期的会话
        
        Returns:
            清理的会话数量
        """
        logger.info("开始清理已过期会话")
        
        try:
            expired_sessions = AuthService.get_expired_sessions()
            cleaned_count = 0
            
            for session in expired_sessions:
                if AuthService.mark_session_expired(session):
                    cleaned_count += 1
            
            logger.info(f"会话清理完成 - 清理数量: {cleaned_count}")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"清理过期会话失败 - 错误: {str(e)}", exc_info=True)
            return 0

    @staticmethod
    def get_session_info(session: AuthSession) -> Dict[str, Any]:
        """获取会话信息摘要
        
        Args:
            session: AuthSession实例
            
        Returns:
            会话信息字典
        """
        if not session:
            return {}
        
        return {
            'session_id': session.id,
            'platform_sign': session.platform.sign,
            'platform_name': session.platform.name,
            'account': session.account,
            'status': session.status,
            'login_time': session.login_time,
            'expire_time': session.expire_time,
            'is_valid': AuthService.is_session_valid(session),
            'has_auth_data': bool(session.auth)
        }

    @staticmethod
    def trigger_login_task(platform_sign: str, account: str, password: str) -> Optional[str]:
        """触发异步登录任务
        
        Args:
            platform_sign: 平台标识
            account: 账户名
            password: 密码
            
        Returns:
            任务ID，失败返回None
        """
        logger.info(f"触发登录任务 - 平台: {platform_sign}, 账户: {account}")
        
        try:
            # 导入任务函数（避免循环导入）
            from external_platform.tasks import login_task
            
            # 异步执行登录任务
            result = login_task.delay(platform_sign, account, password)
            task_id = result.id
            
            logger.info(f"登录任务已触发 - 任务ID: {task_id}, "
                       f"平台: {platform_sign}, 账户: {account}")
            
            return task_id
            
        except Exception as e:
            logger.error(f"触发登录任务失败 - 平台: {platform_sign}, 账户: {account}, "
                        f"错误: {str(e)}", exc_info=True)
            return None