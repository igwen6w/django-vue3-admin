"""
工单同步管理命令
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from work_order.models import WorkOrderSystem
from work_order.services import WorkOrderSyncManager
from work_order.tasks import sync_work_order_data, clean_old_sync_logs


class Command(BaseCommand):
    help = '工单同步管理命令'

    def add_arguments(self, parser):
        parser.add_argument(
            '--system-id',
            type=int,
            help='指定工单系统ID进行同步',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='同步所有启用的工单系统',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='显示所有系统的同步状态',
        )
        parser.add_argument(
            '--clean-logs',
            action='store_true',
            help='清理旧的同步日志',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='清理日志时保留的天数（默认30天）',
        )
        parser.add_argument(
            '--async',
            action='store_true',
            help='异步执行同步任务',
        )

    def handle(self, *args, **options):
        if options['status']:
            self.show_sync_status()
        elif options['clean_logs']:
            self.clean_sync_logs(options['days'], options['async'])
        elif options['system_id']:
            self.sync_specific_system(options['system_id'], options['async'])
        elif options['all']:
            self.sync_all_systems(options['async'])
        else:
            self.stdout.write(
                self.style.ERROR('请指定操作类型，使用 --help 查看帮助')
            )

    def show_sync_status(self):
        """显示同步状态"""
        self.stdout.write('获取同步状态...')
        
        try:
            status = WorkOrderSyncManager.get_sync_status()
            
            self.stdout.write(self.style.SUCCESS('同步状态:'))
            for system_name, system_status in status.items():
                self.stdout.write(f'\n系统: {system_name}')
                self.stdout.write(f'  启用状态: {"启用" if system_status["is_active"] else "禁用"}')
                self.stdout.write(f'  同步间隔: {system_status["sync_interval"]} 秒')
                self.stdout.write(f'  最后同步: {system_status["last_sync_time"] or "从未同步"}')
                self.stdout.write(f'  同步状态: {system_status["last_sync_status"] or "未知"}')
                
                if system_status["last_sync_error"]:
                    self.stdout.write(
                        self.style.WARNING(f'  错误信息: {system_status["last_sync_error"]}')
                    )
                    
        except Exception as e:
            raise CommandError(f'获取同步状态失败: {str(e)}')

    def clean_sync_logs(self, days, async_mode):
        """清理同步日志"""
        self.stdout.write(f'清理 {days} 天前的同步日志...')
        
        try:
            if async_mode:
                # 异步执行
                task = clean_old_sync_logs.delay(days)
                self.stdout.write(
                    self.style.SUCCESS(f'清理任务已提交，任务ID: {task.id}')
                )
            else:
                # 同步执行
                result = clean_old_sync_logs(days)
                self.stdout.write(
                    self.style.SUCCESS(f'清理完成，删除了 {result["deleted_count"]} 条记录')
                )
                
        except Exception as e:
            raise CommandError(f'清理同步日志失败: {str(e)}')

    def sync_specific_system(self, system_id, async_mode):
        """同步指定系统"""
        try:
            system = WorkOrderSystem.objects.get(id=system_id)
            self.stdout.write(f'同步工单系统: {system.name}')
            
            if async_mode:
                # 异步执行
                from work_order.tasks import sync_work_order
                task = sync_work_order.delay(system_id)
                self.stdout.write(
                    self.style.SUCCESS(f'同步任务已提交，任务ID: {task.id}')
                )
            else:
                # 同步执行
                result = WorkOrderSyncManager.sync_system_by_id(system_id)
                self.stdout.write(
                    self.style.SUCCESS(f'同步完成: {result}')
                )
                
        except WorkOrderSystem.DoesNotExist:
            raise CommandError(f'工单系统不存在: {system_id}')
        except Exception as e:
            raise CommandError(f'同步失败: {str(e)}')

    def sync_all_systems(self, async_mode):
        """同步所有系统"""
        self.stdout.write('同步所有启用的工单系统...')
        
        try:
            if async_mode:
                # 异步执行
                task = sync_work_order_data.delay()
                self.stdout.write(
                    self.style.SUCCESS(f'同步任务已提交，任务ID: {task.id}')
                )
            else:
                # 同步执行
                results = WorkOrderSyncManager.sync_all_systems()
                
                self.stdout.write(self.style.SUCCESS('同步完成:'))
                for system_name, result in results.items():
                    if isinstance(result, dict) and 'status' in result:
                        status = result['status']
                        if status == 'success':
                            self.stdout.write(
                                self.style.SUCCESS(f'  {system_name}: 成功')
                            )
                        elif status == 'partial':
                            self.stdout.write(
                                self.style.WARNING(f'  {system_name}: 部分成功')
                            )
                        else:
                            self.stdout.write(
                                self.style.ERROR(f'  {system_name}: 失败')
                            )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'  {system_name}: 失败 - {result}')
                        )
                        
        except Exception as e:
            raise CommandError(f'同步失败: {str(e)}')
