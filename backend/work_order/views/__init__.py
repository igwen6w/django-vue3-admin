__all__ = [
    'DemoViewSet',
    'MetaViewSet',
    'DisposalViewSet',
    'CategoryViewSet',
    'BaseViewSet'
]

from work_order.views.demo import DemoViewSet
from work_order.views.meta import MetaViewSet
from work_order.views.disposal import DisposalViewSet
from work_order.views.category import CategoryViewSet
from work_order.views.base import BaseViewSet