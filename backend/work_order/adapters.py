"""
外部工单系统适配器
提供统一的接口来连接不同的外部工单系统
"""
import requests
import json
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseWorkOrderAdapter(ABC):
    """工单系统适配器基类"""
    
    def __init__(self, system_config):
        self.system_config = system_config
        self.api_url = system_config.api_url
        self.api_key = system_config.api_key
        self.username = system_config.username
        self.password = system_config.password
        
    @abstractmethod
    def authenticate(self) -> bool:
        """认证方法"""
        pass
    
    @abstractmethod
    def get_work_orders(self, since: Optional[datetime] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取工单列表"""
        pass
    
    @abstractmethod
    def get_work_order_detail(self, external_id: str) -> Optional[Dict[str, Any]]:
        """获取工单详情"""
        pass
    
    @abstractmethod
    def update_work_order(self, external_id: str, data: Dict[str, Any]) -> bool:
        """更新工单"""
        pass
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> requests.Response:
        """发送HTTP请求"""
        url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        default_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        
        if headers:
            default_headers.update(headers)
            
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=default_headers, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=30)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=30)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, json=data, headers=default_headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            raise


class JiraAdapter(BaseWorkOrderAdapter):
    """Jira工单系统适配器"""
    
    def authenticate(self) -> bool:
        """Jira认证"""
        try:
            # 使用Basic认证
            auth = (self.username, self.password)
            response = requests.get(f"{self.api_url}/rest/api/2/myself", auth=auth, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Jira authentication failed: {str(e)}")
            return False
    
    def get_work_orders(self, since: Optional[datetime] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取Jira工单列表"""
        try:
            jql = "ORDER BY updated DESC"
            if since:
                jql = f"updated >= '{since.strftime('%Y-%m-%d %H:%M')}' ORDER BY updated DESC"
            
            params = {
                'jql': jql,
                'maxResults': limit,
                'fields': 'summary,description,status,priority,assignee,reporter,created,updated,duedate,labels,components'
            }
            
            response = self._make_request('GET', '/rest/api/2/search', data=params)
            data = response.json()
            
            work_orders = []
            for issue in data.get('issues', []):
                work_order = self._parse_jira_issue(issue)
                work_orders.append(work_order)
                
            return work_orders
            
        except Exception as e:
            logger.error(f"Failed to get Jira work orders: {str(e)}")
            return []
    
    def get_work_order_detail(self, external_id: str) -> Optional[Dict[str, Any]]:
        """获取Jira工单详情"""
        try:
            response = self._make_request('GET', f'/rest/api/2/issue/{external_id}')
            issue = response.json()
            return self._parse_jira_issue(issue)
        except Exception as e:
            logger.error(f"Failed to get Jira work order detail for {external_id}: {str(e)}")
            return None
    
    def update_work_order(self, external_id: str, data: Dict[str, Any]) -> bool:
        """更新Jira工单"""
        try:
            # 转换数据格式为Jira格式
            jira_data = self._convert_to_jira_format(data)
            response = self._make_request('PUT', f'/rest/api/2/issue/{external_id}', data=jira_data)
            return response.status_code == 204
        except Exception as e:
            logger.error(f"Failed to update Jira work order {external_id}: {str(e)}")
            return False
    
    def _parse_jira_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """解析Jira工单数据"""
        fields = issue.get('fields', {})
        
        return {
            'external_id': issue.get('key'),
            'title': fields.get('summary', ''),
            'description': fields.get('description', ''),
            'status': fields.get('status', {}).get('name', 'pending'),
            'priority': fields.get('priority', {}).get('name', 'medium'),
            'reporter': fields.get('reporter', {}).get('displayName', ''),
            'reporter_email': fields.get('reporter', {}).get('emailAddress', ''),
            'assignee': fields.get('assignee', {}).get('displayName', '') if fields.get('assignee') else '',
            'assignee_email': fields.get('assignee', {}).get('emailAddress', '') if fields.get('assignee') else '',
            'reported_at': fields.get('created'),
            'due_date': fields.get('duedate'),
            'resolved_at': fields.get('resolutiondate'),
            'category': fields.get('components', [{}])[0].get('name', '') if fields.get('components') else '',
            'tags': fields.get('labels', []),
            'raw_data': issue
        }
    
    def _convert_to_jira_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """转换数据为Jira格式"""
        jira_data = {'fields': {}}
        
        if 'title' in data:
            jira_data['fields']['summary'] = data['title']
        if 'description' in data:
            jira_data['fields']['description'] = data['description']
        if 'assignee' in data:
            jira_data['fields']['assignee'] = {'name': data['assignee']}
        if 'priority' in data:
            jira_data['fields']['priority'] = {'name': data['priority']}
            
        return jira_data


class ZendeskAdapter(BaseWorkOrderAdapter):
    """Zendesk工单系统适配器"""
    
    def authenticate(self) -> bool:
        """Zendesk认证"""
        try:
            response = self._make_request('GET', '/api/v2/users/me.json')
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Zendesk authentication failed: {str(e)}")
            return False
    
    def get_work_orders(self, since: Optional[datetime] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取Zendesk工单列表"""
        try:
            params = {'per_page': limit}
            if since:
                params['start_time'] = int(since.timestamp())
            
            response = self._make_request('GET', '/api/v2/tickets.json', data=params)
            data = response.json()
            
            work_orders = []
            for ticket in data.get('tickets', []):
                work_order = self._parse_zendesk_ticket(ticket)
                work_orders.append(work_order)
                
            return work_orders
            
        except Exception as e:
            logger.error(f"Failed to get Zendesk work orders: {str(e)}")
            return []
    
    def get_work_order_detail(self, external_id: str) -> Optional[Dict[str, Any]]:
        """获取Zendesk工单详情"""
        try:
            response = self._make_request('GET', f'/api/v2/tickets/{external_id}.json')
            data = response.json()
            return self._parse_zendesk_ticket(data.get('ticket', {}))
        except Exception as e:
            logger.error(f"Failed to get Zendesk work order detail for {external_id}: {str(e)}")
            return None
    
    def update_work_order(self, external_id: str, data: Dict[str, Any]) -> bool:
        """更新Zendesk工单"""
        try:
            zendesk_data = self._convert_to_zendesk_format(data)
            response = self._make_request('PUT', f'/api/v2/tickets/{external_id}.json', data=zendesk_data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to update Zendesk work order {external_id}: {str(e)}")
            return False
    
    def _parse_zendesk_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """解析Zendesk工单数据"""
        return {
            'external_id': str(ticket.get('id')),
            'title': ticket.get('subject', ''),
            'description': ticket.get('description', ''),
            'status': ticket.get('status', 'pending'),
            'priority': ticket.get('priority', 'medium'),
            'reporter': ticket.get('requester_id', ''),
            'assignee': ticket.get('assignee_id', ''),
            'reported_at': ticket.get('created_at'),
            'due_date': ticket.get('due_at'),
            'resolved_at': ticket.get('solved_at'),
            'category': ticket.get('type', ''),
            'tags': ticket.get('tags', []),
            'raw_data': ticket
        }
    
    def _convert_to_zendesk_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """转换数据为Zendesk格式"""
        return {'ticket': data}


class WorkOrderAdapterFactory:
    """工单系统适配器工厂"""
    
    ADAPTERS = {
        'jira': JiraAdapter,
        'zendesk': ZendeskAdapter,
    }
    
    @classmethod
    def create_adapter(cls, system_type: str, system_config) -> BaseWorkOrderAdapter:
        """创建适配器实例"""
        adapter_class = cls.ADAPTERS.get(system_type.lower())
        if not adapter_class:
            raise ValueError(f"Unsupported work order system type: {system_type}")
        
        return adapter_class(system_config)
    
    @classmethod
    def get_supported_systems(cls) -> List[str]:
        """获取支持的系统类型"""
        return list(cls.ADAPTERS.keys())
