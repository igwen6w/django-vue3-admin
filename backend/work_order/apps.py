from django.apps import AppConfig


class WorkOrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'work_order'
    
    def ready(self):
        """应用启动时导入信号处理器"""
        import work_order.signals