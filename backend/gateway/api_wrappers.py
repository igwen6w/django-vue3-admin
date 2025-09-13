# -*- coding: utf-8 -*-

"""
平台网关SDK API封装层
为开发人员提供业务友好的API接口，隐藏底层的会话管理和认证细节
"""

import json
import time
import logging
import mimetypes

from typing import Dict, Any, Optional, Union, List
from functools import wraps
from datetime import timedelta
import redis
from django.conf import settings
from django.utils import timezone

from .services import SessionManager
from .config import get_gateway_config
from .exceptions import (
    GatewayError, AuthenticationError, SessionExpiredError,
    PlatformUnavailableError, PlatformAPIError, ConfigurationError
)
from .utils import (
    validate_response, extract_error_message, safe_get_config,
    log_request_info, format_duration
)

logger = logging.getLogger(__name__)


class PlatformAPI:
    """平台API封装类
    
    提供业务友好的API接口，自动处理会话管理、认证和错误处理。
    支持单例模式，确保整个应用中只有一个API实例。
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, redis_client: Optional[redis.Redis] = None, 
                 config: Optional[Dict[str, Any]] = None):
        """初始化API实例
        
        Args:
            redis_client: Redis客户端实例
            config: 配置字典
        """
        # 避免重复初始化
        if self._initialized:
            return
        
        try:
            # 加载配置
            self.config = config or get_gateway_config()
            
            # 初始化SessionManager
            self.session_manager = SessionManager(redis_client, self.config)
            
            # API调用统计
            self._call_count = 0
            self._last_call_time = None
            self._error_count = 0
            
            # 标记为已初始化
            self._initialized = True
            
            logger.info("PlatformAPI初始化成功")
            
        except Exception as e:
            logger.error(f"PlatformAPI初始化失败: {e}")
            raise ConfigurationError(f"API初始化失败: {e}")
    
    def _ensure_authenticated(func):
        """装饰器：确保API调用前已经认证"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                # 检查会话是否有效
                if not self.session_manager.is_session_valid():
                    logger.info("会话无效，尝试重新登录")
                    if not self.session_manager.login():
                        raise AuthenticationError("登录失败，无法执行API调用")
                
                # 执行原始方法
                return func(self, *args, **kwargs)
                
            except (AuthenticationError, SessionExpiredError):
                # 认证相关异常直接抛出
                raise
            except Exception as e:
                logger.error(f"API调用异常 - {func.__name__}: {e}")
                raise GatewayError(f"API调用异常: {e}")
        
        return wrapper
    
    def _handle_api_response(self, response, api_name: str) -> Dict[str, Any]:
        """处理API响应，标准化返回格式
        
        Args:
            response: HTTP响应对象
            api_name: API名称
            
        Returns:
            标准化的响应数据
        """
        try:
            # 记录API调用
            self._call_count += 1
            self._last_call_time = time.time()
            
            # 验证响应状态
            if not validate_response(response):
                self._error_count += 1
                error_msg = extract_error_message(response)
                
                logger.warning(f"API调用失败 - {api_name}: HTTP {response.status_code}, {error_msg}")
                
                raise PlatformAPIError(
                    f"{api_name} API调用失败: {error_msg}",
                    status_code=response.status_code,
                    api_endpoint=response.url,
                    response_data=self._safe_parse_json(response)
                )
            
            # 解析响应数据
            data = self._parse_response_data(response)
            
            logger.info(f"API调用成功 - {api_name}: 返回数据大小 {len(str(data))} 字符")
            
            return {
                'success': True,
                'data': data,
                'api_name': api_name,
                'status_code': response.status_code,
                'call_time': self._last_call_time
            }
            
        except PlatformAPIError:
            raise
        except Exception as e:
            self._error_count += 1
            logger.error(f"响应处理异常 - {api_name}: {e}")
            raise GatewayError(f"响应处理异常: {e}")
    
    def _parse_response_data(self, response) -> Any:
        """解析响应数据
        
        Args:
            response: HTTP响应对象
            
        Returns:
            解析后的数据
        """
        try:
            content_type = response.headers.get('content-type', '').lower()

            if 'application/json' in content_type:
                data = response.json()
                return self._normalize_json_response(data)
            elif 'text/html' in content_type:
                # 对方响应格式不正确，尝试解析为JSON
                data = response.json()
                return self._normalize_json_response(data)
                # 对于HTML响应，尝试提取有用信息
                # return self._parse_html_response(response)
            elif 'text/' in content_type:
                return self._parse_text_response(response)
            elif 'application/xml' in content_type:
                return self._parse_xml_response(response)
            else:
                return {
                    'content_type': content_type,
                    'content_length': len(response.content),
                    'raw_data': response.content[:100].decode('utf-8', errors='ignore')
                }
                
        except Exception as e:
            logger.warning(f"解析响应数据失败: {e}")
            return {
                'raw_data': str(response.content)[:500],
                'parse_error': str(e),
                'content_type': response.headers.get('content-type', 'unknown')
            }
    
    def _normalize_json_response(self, data: Any) -> Dict[str, Any]:
        """标准化JSON响应数据
        
        Args:
            data: 原始JSON数据
            
        Returns:
            标准化后的数据
        """
        if isinstance(data, dict):
            # 检查是否有标准的响应格式
            if 'code' in data and 'data' in data:
                # 标准格式: {"code": 0, "data": {...}, "message": "..."}
                return {
                    'status_code': data.get('code', 0),
                    'message': data.get('message', data.get('msg', '')),
                    'data': data.get('data'),
                    'success': data.get('code', 0) == 0
                }
            elif 'success' in data:
                # 另一种格式: {"success": true, "result": {...}}
                return {
                    'success': data.get('success', False),
                    'data': data.get('result', data.get('data')),
                    'message': data.get('message', data.get('error', ''))
                }
            else:
                # 直接返回数据
                return data
        elif isinstance(data, list):
            # 列表数据，包装为标准格式
            return {
                'success': True,
                'data': data,
                'total': len(data)
            }
        else:
            # 其他类型数据
            return {
                'success': True,
                'data': data
            }
    
    def _parse_html_response(self, response) -> Dict[str, Any]:
        """解析HTML响应
        
        Args:
            response: HTTP响应对象
            
        Returns:
            解析后的HTML信息
        """
        try:
            html_content = response.text
            
            # 提取基本信息
            result = {
                'content_type': 'text/html',
                'content_length': len(html_content),
                'title': self._extract_html_title(html_content)
            }
            
            # 检查是否包含错误信息
            error_indicators = ['error', '错误', '失败', 'failed', 'exception']
            content_lower = html_content.lower()
            
            has_error = any(indicator in content_lower for indicator in error_indicators)
            if has_error:
                result['error_detected'] = True
                result['error_snippet'] = self._extract_error_from_html(html_content)
            
            # 检查是否为登录页面
            login_indicators = ['login', '登录', 'signin', 'username', 'password']
            is_login_page = any(indicator in content_lower for indicator in login_indicators)
            
            if is_login_page:
                result['is_login_page'] = True
                result['requires_auth'] = True
            
            return result
            
        except Exception as e:
            logger.error(f"解析HTML响应失败: {e}")
            return {
                'content_type': 'text/html',
                'parse_error': str(e),
                'content_preview': response.text[:200]
            }
    
    def _parse_text_response(self, response) -> Dict[str, Any]:
        """解析文本响应
        
        Args:
            response: HTTP响应对象
            
        Returns:
            解析后的文本信息
        """
        try:
            text_content = response.text
            content_type = response.headers.get('content-type', 'text/plain')
            
            result = {
                'content_type': content_type,
                'content_length': len(text_content),
                'text': text_content[:1000],  # 限制长度
                'encoding': response.encoding or 'utf-8'
            }
            
            # 尝试检测是否为CSV或其他结构化文本
            if 'csv' in content_type.lower() or text_content.count(',') > text_content.count('\n') * 2:
                result['format'] = 'csv'
                result['estimated_rows'] = text_content.count('\n') + 1
            elif text_content.count('\t') > text_content.count('\n'):
                result['format'] = 'tsv'
            else:
                result['format'] = 'plain_text'
            
            return result
            
        except Exception as e:
            logger.error(f"解析文本响应失败: {e}")
            return {
                'content_type': 'text/plain',
                'parse_error': str(e)
            }
    
    def _parse_xml_response(self, response) -> Dict[str, Any]:
        """解析XML响应
        
        Args:
            response: HTTP响应对象
            
        Returns:
            解析后的XML信息
        """
        try:
            import xml.etree.ElementTree as ET
            
            xml_content = response.text
            root = ET.fromstring(xml_content)
            
            # 转换XML为字典
            def xml_to_dict(element):
                result = {}
                for child in element:
                    if len(child) == 0:
                        result[child.tag] = child.text
                    else:
                        result[child.tag] = xml_to_dict(child)
                return result
            
            data = xml_to_dict(root)
            
            return {
                'content_type': 'application/xml',
                'root_tag': root.tag,
                'data': data,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"解析XML响应失败: {e}")
            return {
                'content_type': 'application/xml',
                'parse_error': str(e),
                'raw_xml': response.text[:500]
            }
    
    def _extract_error_from_html(self, html_content: str) -> str:
        """从HTML中提取错误信息
        
        Args:
            html_content: HTML内容
            
        Returns:
            错误信息
        """
        try:
            import re
            
            # 尝试提取常见的错误信息
            error_patterns = [
                r'<div[^>]*class=["\']?error["\']?[^>]*>([^<]+)</div>',
                r'<span[^>]*class=["\']?error["\']?[^>]*>([^<]+)</span>',
                r'<p[^>]*class=["\']?error["\']?[^>]*>([^<]+)</p>',
                r'错误[：:]([^<\n]+)',
                r'Error[:]([^<\n]+)',
            ]
            
            for pattern in error_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
                if match:
                    return match.group(1).strip()
            
            # 如果没有找到特定模式，返回简短的内容摘要
            text_content = re.sub(r'<[^>]+>', '', html_content)
            lines = text_content.split('\n')
            for line in lines:
                line = line.strip()
                if line and ('错误' in line or 'error' in line.lower()):
                    return line[:100]
            
            return '未能提取具体错误信息'
            
        except Exception:
            return '错误信息提取失败'
    
    def _safe_parse_json(self, response) -> Optional[Dict]:
        """安全解析JSON响应"""
        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
            return None
    
    def _extract_html_title(self, html_content: str) -> str:
        """从HTML内容中提取标题"""
        try:
            import re
            match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            return match.group(1).strip() if match else '无标题'
        except Exception:
            return '无标题'
    
    @_ensure_authenticated
    def get_user_info(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """获取用户信息
        
        Args:
            user_id: 用户ID，如果不提供则获取当前用户信息
            
        Returns:
            用户信息字典
        """
        try:
            api_path = "/personal_center/sub_act.php?act=list_my"
            
            # 执行API请求
            response = self.session_manager.request('GET', api_path)
            
            # 处理响应
            return self._handle_api_response(response, 'get_user_info')
            
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
            raise
    
    @_ensure_authenticated
    def submit_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """提交订单
        
        Args:
            order_data: 订单数据字典
            
        Returns:
            提交结果
        """
        try:
            if not order_data:
                raise ValueError("订单数据不能为空")
            
            logger.info(f"提交订单 - 订单类型: {order_data.get('type', '未知')}")
            
            # 执行API请求
            response = self.session_manager.request(
                'POST', 
                '/api/order/submit',
                json=order_data
            )
            
            # 处理响应
            return self._handle_api_response(response, 'submit_order')
            
        except Exception as e:
            logger.error(f"提交订单失败: {e}")
            raise
    
    @_ensure_authenticated
    def keepalive(self) -> Dict[str, Any]:
        """保活接口，用于维持会话活跃状态
        
        Returns:
            保活结果
        """
        try:
            logger.debug("执行保活请求")
            
            # 执行保活请求
            response = self.session_manager.request('GET', '/personal_center/sub_act.php?act=list_my')
            
            # 处理响应
            result = self._handle_api_response(response, 'keepalive')
            
            # 更新会话活动时间
            self.session_manager.update_session_activity()
            
            return result
            
        except Exception as e:
            logger.error(f"保活请求失败: {e}")
            raise
    
    @_ensure_authenticated
    def get_order_list(self, page: int = 1, page_size: int = 20, 
                      filters: Optional[Dict] = None) -> Dict[str, Any]:
        """获取订单列表
        
        Args:
            page: 页码
            page_size: 每页数量
            filters: 过滤条件
            
        Returns:
            订单列表
        """
        try:
            # 构建查询参数
            params = {
                'page': page,
                'pagesize': page_size
            }
            
            if filters:
                params.update(filters)
            
            logger.info(f"获取订单列表 - 页码: {page}, 每页: {page_size}")
            
            # 执行API请求
            response = self.session_manager.request(
                'POST',
                '/payroll3/payroll_sub_list_act_doris.php',
                params=params
            )
            
            # 处理响应
            return self._handle_api_response(response, 'get_order_list')
            
        except Exception as e:
            logger.error(f"获取订单列表失败: {e}")
            raise


    @_ensure_authenticated
    def get_pending_disposal_order_list(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取待处置工单

        Args:
            page: 页码
            page_size: 每页数量

        Returns:
            订单列表
        """
        try:
            # 构建查询参数
            # 获取当前时间范围（默认获取最近30天的工单）
            end_time = timezone.now()
            start_time_param = end_time - timedelta(days=30)

            params = {
                'page': page,
                'pagesize': page_size,
                'act': 'search_payroll_list',
                'search_ps_caption': '处置',
                'search_payroll_result_tmp': '待处置',
                'end_pscaption_time_type': 1,
                'psr_ps_caption': '处置',
                'search_ps_captionName': '处置',
                'search_expire_time_type': 1,
                'search_start_time': start_time_param.strftime('%Y-%m-%d %H:%M:%S'),
                'search_end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            }

            logger.info(f"获取待处置工单 - 页码: {page}, 每页: {page_size}, 时间范围: {start_time_param} 到 {end_time}")

            # 执行API请求
            response = self.session_manager.request(
                'POST',
                '/payroll3/payroll_sub_list_act_doris.php',
                params=params
            )

            return self._handle_api_response(response, 'get_pending_disposal_order_list')
            
        except Exception as e:
            logger.error(f"获取订单列表失败: {e}")
            raise
    
    @_ensure_authenticated
    def get_order_detail(self, order_id: str) -> Dict[str, Any]:
        """获取订单详情
        
        Args:
            order_id: 订单ID
            
        Returns:
            订单详情
        """
        try:
            if not order_id:
                raise ValueError("订单ID不能为空")
            
            logger.info(f"获取订单详情 - 订单ID: {order_id}")
            
            # 执行API请求
            response = self.session_manager.request(
                'POST', 
                '/payroll3/sub_act.php',
                params={
                    'act': 'payroll_view_module',
                    'id': order_id,
                    'module_name': '系统默认'
                }
            )
            
            # 处理响应
            return self._handle_api_response(response, 'get_order_detail')
            
        except Exception as e:
            logger.error(f"获取订单详情失败: {e}")
            raise

    
    @_ensure_authenticated
    def edit_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """编辑订单
        
        Args:
            params: 编辑数据
            
        Returns:
            编辑结果
        """
        try:
            if not params:
                raise ValueError("数据不能为空")
            
            logger.info(f"编辑订单 - 订单编号: {params.get('roll_number')}")

            # 构建请求参数
            request_params = {
                'act': 'save_payroll_edit',
                **{key: params.get(key) for key in [
                    'roll_number',
                    'payroll_result',
                    'product_ids',
                    'addr2',
                    'company_address',
                    'order_number',
                    'normal_payroll_title',
                    'note16',
                    'note17'
                ]}
            }
            
            # 执行API请求
            response = self.session_manager.request(
                'POST', 
                '/payroll3/sub_act.php',
                params=request_params
            )
            
            # 实际预期的响应格式
            # {
            #     "status": "success",
            #     "des": "修改成功",
            #     "res": []
            # }
            # 处理响应
            return self._handle_api_response(response, 'edit_order')
            
        except Exception as e:
            logger.error(f"编辑订单失败: {e}")
            raise

    
    @_ensure_authenticated
    def update_order_status(self, order_id: str, status: str, 
                           note: Optional[str] = None) -> Dict[str, Any]:
        """更新订单状态
        
        Args:
            order_id: 订单ID
            status: 新状态
            note: 备注信息
            
        Returns:
            更新结果
        """
        try:
            if not order_id or not status:
                raise ValueError("订单ID和状态不能为空")
            
            update_data = {
                'status': status
            }
            
            if note:
                update_data['note'] = note
            
            logger.info(f"更新订单状态 - 订单ID: {order_id}, 状态: {status}")
            
            # 执行API请求
            response = self.session_manager.request(
                'PUT',
                f'/api/order/{order_id}/status',
                json=update_data
            )
            
            # 处理响应
            return self._handle_api_response(response, 'update_order_status')
            
        except Exception as e:
            logger.error(f"更新订单状态失败: {e}")
            raise
    
    @_ensure_authenticated
    def custom_request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """自定义API请求，用于调用未封装的API
        
        Args:
            method: HTTP方法
            path: API路径
            **kwargs: 其他请求参数
            
        Returns:
            API响应结果
        """
        try:
            logger.info(f"执行自定义API请求 - {method} {path}")
            
            # 执行API请求
            response = self.session_manager.request(method, path, **kwargs)
            
            # 处理响应
            return self._handle_api_response(response, f'custom_{method.lower()}')
            
        except Exception as e:
            logger.error(f"自定义API请求失败: {e}")
            raise
    
    @_ensure_authenticated
    def batch_request(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量API请求
        
        Args:
            requests: 请求列表，每个元素包含 method, path 和其他参数
            
        Returns:
            批量请求结果列表
        """
        if not requests:
            return []
        
        results = []
        
        for i, req in enumerate(requests):
            try:
                method = req.get('method', 'GET')
                path = req.get('path', '')
                kwargs = {k: v for k, v in req.items() if k not in ['method', 'path']}
                
                logger.debug(f"执行批量请求 {i+1}/{len(requests)} - {method} {path}")
                
                response = self.session_manager.request(method, path, **kwargs)
                result = self._handle_api_response(response, f'batch_{i+1}')
                
                results.append({
                    'index': i,
                    'success': True,
                    'result': result
                })
                
            except Exception as e:
                logger.error(f"批量请求第{i+1}个失败: {e}")
                results.append({
                    'index': i,
                    'success': False,
                    'error': str(e),
                    'error_type': type(e).__name__
                })
        
        success_count = sum(1 for r in results if r['success'])
        logger.info(f"批量请求完成 - 成功: {success_count}/{len(requests)}")
        
        return results
    
    @_ensure_authenticated
    def upload_file(self, file_path: str, upload_url: str = '/payroll3/upload_files.php',
                   field_name: str = 'files[]', extra_data: Optional[Dict] = None) -> Dict[str, Any]:
        """上传文件
        
        Args:
            file_path: 本地文件路径
            upload_url: 上传API路径
            field_name: 文件字段名
            extra_data: 额外的表单数据
            
        Returns:
            上传结果
        """
        try:
            import os
            
            if not os.path.exists(file_path):
                raise ValueError(f"文件不存在: {file_path}")
            
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            mime_type, _ = mimetypes.guess_type(file_name)
            mime_type = mime_type or "application/octet-stream"
            
            logger.warning(f"上传文件 - 文件名: {file_name}, 大小: {file_size} bytes, 类型: {mime_type}")
            
            # 准备表单数据
            payload = {
                'act': 'upload_files',
                'roll_number': extra_data.get('roll_number') if extra_data else None
            }

            logger.warning(f"data: {payload}")
            
            # 准备文件数据并执行上传请求
            with open(file_path, 'rb') as f:
                files = [
                    (field_name, (file_name, f, mime_type))
                ]
                
                # 执行上传请求
                response = self.session_manager.request(
                    'POST',
                    upload_url,
                    data=payload,
                    files=files
                )

                logger.warning(f"response: {response.content}")
            
            # 处理响应
            return self._handle_api_response(response, 'upload_file')
            
        except Exception as e:
            logger.error(f"文件上传失败: {e}")
            raise
    
    @_ensure_authenticated
    def download_file(self, download_url: str, save_path: Optional[str] = None,
                     chunk_size: int = 8192) -> Dict[str, Any]:
        """下载文件
        
        Args:
            download_url: 下载链接
            save_path: 保存路径，如为None则返回文件内容
            chunk_size: 分块大小
            
        Returns:
            下载结果
        """
        try:
            import os
            from urllib.parse import urlparse
            
            logger.info(f"下载文件 - URL: {download_url}")
            
            # 执行下载请求
            response = self.session_manager.request('GET', download_url, stream=True)
            
            if not validate_response(response):
                raise PlatformAPIError(f"下载请求失败: HTTP {response.status_code}")
            
            # 获取文件信息
            content_length = response.headers.get('content-length')
            content_type = response.headers.get('content-type', 'application/octet-stream')
            
            if save_path:
                # 保存到文件
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                total_size = 0
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            total_size += len(chunk)
                
                logger.info(f"文件下载完成 - 保存到: {save_path}, 大小: {total_size} bytes")
                
                return {
                    'success': True,
                    'saved_path': save_path,
                    'file_size': total_size,
                    'content_type': content_type
                }
            else:
                # 返回文件内容
                content = response.content
                
                logger.info(f"文件下载完成 - 内容大小: {len(content)} bytes")
                
                return {
                    'success': True,
                    'content': content,
                    'content_type': content_type,
                    'content_length': len(content)
                }
                
        except Exception as e:
            logger.error(f"文件下载失败: {e}")
            raise
    
    def get_api_statistics(self) -> Dict[str, Any]:
        """获取API调用统计信息
        
        Returns:
            API调用统计
        """
        try:
            uptime = time.time() - (self._last_call_time or time.time())
            
            return {
                'total_calls': self._call_count,
                'error_count': self._error_count,
                'success_count': self._call_count - self._error_count,
                'success_rate': (self._call_count - self._error_count) / max(self._call_count, 1) * 100,
                'last_call_time': self._last_call_time,
                'uptime_seconds': uptime,
                'average_success_rate': f"{(self._call_count - self._error_count) / max(self._call_count, 1) * 100:.2f}%",
                'instance_id': id(self)
            }
            
        except Exception as e:
            logger.error(f"获取API统计失败: {e}")
            return {'error': str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查
        
        Returns:
            健康状态信息
        """
        try:
            health_status = {
                'api_instance': 'healthy',
                'session_manager': 'unknown',
                'redis_connection': 'unknown',
                'platform_connectivity': 'unknown',
                'timestamp': time.time()
            }
            
            # 检查SessionManager
            try:
                if self.session_manager:
                    session_info = self.session_manager.get_session_info()
                    if 'error' not in session_info:
                        health_status['session_manager'] = 'healthy'
                        health_status['session_valid'] = session_info.get('is_valid', False)
                    else:
                        health_status['session_manager'] = 'error'
                        health_status['session_error'] = session_info['error']
                else:
                    health_status['session_manager'] = 'not_initialized'
            except Exception as e:
                health_status['session_manager'] = 'error'
                health_status['session_error'] = str(e)
            
            # 检查Redis连接
            try:
                if hasattr(self.session_manager, 'redis_client'):
                    self.session_manager.redis_client.ping()
                    health_status['redis_connection'] = 'healthy'
                else:
                    health_status['redis_connection'] = 'not_available'
            except Exception as e:
                health_status['redis_connection'] = 'error'
                health_status['redis_error'] = str(e)
            
            # 检查平台连通性（尝试保活请求）
            try:
                if health_status['session_manager'] == 'healthy':
                    keepalive_result = self.keepalive()
                    if keepalive_result.get('success'):
                        health_status['platform_connectivity'] = 'healthy'
                    else:
                        health_status['platform_connectivity'] = 'error'
                        health_status['platform_error'] = 'keepalive_failed'
                else:
                    health_status['platform_connectivity'] = 'cannot_test'
            except Exception as e:
                health_status['platform_connectivity'] = 'error'
                health_status['platform_error'] = str(e)
            
            # 计算总体健康状态
            healthy_components = sum(1 for status in health_status.values() 
                                   if isinstance(status, str) and status == 'healthy')
            total_components = 4  # api_instance, session_manager, redis_connection, platform_connectivity
            
            health_status['overall_health'] = 'healthy' if healthy_components >= 3 else 'degraded' if healthy_components >= 2 else 'unhealthy'
            health_status['health_score'] = f"{healthy_components}/{total_components}"
            
            return health_status
            
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return {
                'overall_health': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }
    
    def refresh_session(self) -> bool:
        """刷新会话
        
        Returns:
            刷新是否成功
        """
        try:
            logger.info("手动刷新会话")
            result = self.session_manager.refresh_session()
            
            if result:
                logger.info("会话刷新成功")
            else:
                logger.error("会话刷新失败")
            
            return result
            
        except Exception as e:
            logger.error(f"刷新会话异常: {e}")
            return False
    
    def extend_session(self, extra_seconds: int = 3600) -> bool:
        """延长会话有效期
        
        Args:
            extra_seconds: 额外的秒数
            
        Returns:
            延长是否成功
        """
        try:
            return self.session_manager.extend_session(extra_seconds)
        except Exception as e:
            logger.error(f"延长会话失败: {e}")
            return False
    
    def clear_session(self) -> None:
        """清除会话数据"""
        try:
            self.session_manager.clear_session()
            logger.info("会话数据已清除")
        except Exception as e:
            logger.error(f"清除会话失败: {e}")
    
    def close(self) -> None:
        """关闭API实例，清理资源"""
        try:
            if hasattr(self, 'session_manager'):
                self.session_manager.close()
            
            # 重置单例状态
            PlatformAPI._instance = None
            PlatformAPI._initialized = False
            
            logger.info("PlatformAPI实例已关闭")
            
        except Exception as e:
            logger.error(f"关闭API实例异常: {e}")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# 全局API实例管理
_global_api_instance = None


def get_api_instance(redis_client: Optional[redis.Redis] = None,
                    config: Optional[Dict[str, Any]] = None) -> PlatformAPI:
    """获取全局API实例（单例模式）
    
    Args:
        redis_client: Redis客户端实例
        config: 配置字典
        
    Returns:
        PlatformAPI实例
    """
    global _global_api_instance
    
    try:
        if _global_api_instance is None:
            _global_api_instance = PlatformAPI(redis_client, config)
        
        return _global_api_instance
        
    except Exception as e:
        logger.error(f"获取API实例失败: {e}")
        raise


def reset_api_instance():
    """重置全局API实例"""
    global _global_api_instance
    
    try:
        if _global_api_instance:
            _global_api_instance.close()
        
        _global_api_instance = None
        logger.info("全局API实例已重置")
        
    except Exception as e:
        logger.error(f"重置API实例失败: {e}")


# 便捷函数封装
def get_user_info(user_id: Optional[str] = None) -> Dict[str, Any]:
    """便捷函数：获取用户信息"""
    api = get_api_instance()
    return api.get_user_info(user_id)


def submit_order(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """便捷函数：提交订单"""
    api = get_api_instance()
    return api.submit_order(order_data)


def keepalive() -> Dict[str, Any]:
    """便捷函数：保活请求"""
    api = get_api_instance()
    return api.keepalive()


def get_order_list(page: int = 1, page_size: int = 20,
                  filters: Optional[Dict] = None) -> Dict[str, Any]:
    """便捷函数：获取订单列表"""
    api = get_api_instance()
    return api.get_order_list(page, page_size, filters)

def get_pending_disposal_order_list(page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """便捷函数：获取待处置工单列表"""
    api = get_api_instance()
    return api.get_pending_disposal_order_list(page, page_size)


def get_order_detail(order_id: str) -> Dict[str, Any]:
    """便捷函数：获取订单详情"""
    api = get_api_instance()
    return api.get_order_detail(order_id)


def edit_order(params: Dict[str, Any]) -> Dict[str, Any]:
    """便捷函数：编辑订单"""
    api = get_api_instance()
    return api.edit_order(params)

def update_order_status(order_id: str, status: str,
                       note: Optional[str] = None) -> Dict[str, Any]:
    """便捷函数：更新订单状态"""
    api = get_api_instance()
    return api.update_order_status(order_id, status, note)


def custom_request(method: str, path: str, **kwargs) -> Dict[str, Any]:
    """便捷函数：自定义API请求"""
    api = get_api_instance()
    return api.custom_request(method, path, **kwargs)


def batch_request(requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """便捷函数：批量API请求"""
    api = get_api_instance()
    return api.batch_request(requests)


def upload_file(file_path: str, upload_url: str = '/payroll3/upload_files.php',
               field_name: str = 'files[]', extra_data: Optional[Dict] = None) -> Dict[str, Any]:
    """便捷函数：上传文件"""
    api = get_api_instance()
    return api.upload_file(file_path, upload_url, field_name, extra_data)


def download_file(download_url: str, save_path: Optional[str] = None,
                 chunk_size: int = 8192) -> Dict[str, Any]:
    """便捷函数：下载文件"""
    api = get_api_instance()
    return api.download_file(download_url, save_path, chunk_size)


def get_api_statistics() -> Dict[str, Any]:
    """便捷函数：获取API统计信息"""
    api = get_api_instance()
    return api.get_api_statistics()


def health_check() -> Dict[str, Any]:
    """便捷函数：健康检查"""
    api = get_api_instance()
    return api.health_check()




def refresh_session() -> bool:
    """便捷函数：刷新会话"""
    api = get_api_instance()
    return api.refresh_session()