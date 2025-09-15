import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from external_platform.models import ExternalDistrictNode


class Command(BaseCommand):
    help = '导入区县节点数据从 di_node.json 文件到 ExternalDistrictNode 模型'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='external_platform/external/di_node.json',
            help='JSON 文件路径（相对于项目根目录）'
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='导入前先清空现有数据'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='试运行模式，不实际写入数据库'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== 区县节点数据导入工具 ===')
        )
        
        # 获取文件路径
        json_file = options['file']
        if not os.path.isabs(json_file):
            # 相对路径，基于项目根目录
            from django.conf import settings
            base_dir = getattr(settings, 'BASE_DIR', os.getcwd())
            json_file = os.path.join(base_dir, json_file)
        
        # 检查文件是否存在
        if not os.path.exists(json_file):
            raise CommandError(f'文件不存在: {json_file}')
        
        # 读取 JSON 数据
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)
            self.stdout.write(
                self.style.SUCCESS(f'✓ 成功读取 JSON 文件，共 {len(nodes_data)} 条记录')
            )
        except json.JSONDecodeError as e:
            raise CommandError(f'JSON 格式错误: {e}')
        except Exception as e:
            raise CommandError(f'读取文件失败: {e}')
        
        # 验证数据格式
        if not self._validate_data(nodes_data):
            raise CommandError('数据格式验证失败')
        
        # 清空现有数据（如果指定）
        if options['clean']:
            if options['dry_run']:
                self.stdout.write('🔍 [试运行] 将清空现有数据')
            else:
                count = ExternalDistrictNode.objects.count()
                if count > 0:
                    ExternalDistrictNode.objects.all().delete()
                    self.stdout.write(
                        self.style.WARNING(f'✓ 已清空 {count} 条现有数据')
                    )
        
        # 排序数据以处理父子关系
        sorted_nodes = self._sort_nodes_by_hierarchy(nodes_data)
        self.stdout.write('✓ 节点层级排序完成')
        
        # 导入数据
        if options['dry_run']:
            self._dry_run_import(sorted_nodes)
        else:
            self._import_nodes(sorted_nodes)

    def _validate_data(self, nodes_data):
        """验证数据格式"""
        if not isinstance(nodes_data, list):
            self.stdout.write(
                self.style.ERROR('✗ 数据格式错误：应该是数组格式')
            )
            return False
        
        required_fields = ['id', 'name']
        for i, node in enumerate(nodes_data):
            if not isinstance(node, dict):
                self.stdout.write(
                    self.style.ERROR(f'✗ 第 {i+1} 条记录格式错误：应该是对象格式')
                )
                return False
            
            for field in required_fields:
                if field not in node:
                    self.stdout.write(
                        self.style.ERROR(f'✗ 第 {i+1} 条记录缺少必需字段: {field}')
                    )
                    return False
        
        self.stdout.write('✓ 数据格式验证通过')
        return True

    def _sort_nodes_by_hierarchy(self, nodes):
        """按层级关系排序节点，父节点在前"""
        sorted_nodes = []
        processed_ids = set()
        
        def add_node_and_children(node_id):
            # 查找当前节点
            current_node = None
            for node in nodes:
                if str(node['id']) == str(node_id) and str(node_id) not in processed_ids:
                    current_node = node
                    break
            
            if current_node is None:
                return
                
            # 添加当前节点
            sorted_nodes.append(current_node)
            processed_ids.add(str(node_id))
            
            # 递归添加子节点
            for node in nodes:
                if str(node.get('pId', '')) == str(node_id) and str(node['id']) not in processed_ids:
                    add_node_and_children(node['id'])
        
        # 首先处理顶层节点（没有父节点或父节点不在数据中的节点）
        all_ids = {str(node['id']) for node in nodes}
        for node in nodes:
            parent_id = node.get('pId')
            if parent_id is None or str(parent_id) not in all_ids:
                if str(node['id']) not in processed_ids:
                    add_node_and_children(node['id'])
        
        # 处理剩余节点（防止遗漏）
        for node in nodes:
            if str(node['id']) not in processed_ids:
                add_node_and_children(node['id'])
        
        return sorted_nodes

    def _dry_run_import(self, sorted_nodes):
        """试运行模式"""
        self.stdout.write(
            self.style.WARNING('🔍 试运行模式 - 不会实际写入数据库')
        )
        
        for node_data in sorted_nodes:
            code = str(node_data['id'])
            name = node_data['name']
            parent_code = str(node_data['pId']) if node_data.get('pId') else None
            
            # 检查节点是否已存在
            exists = ExternalDistrictNode.objects.filter(code=code).exists()
            action = "更新" if exists else "创建"
            
            # 检查父节点
            parent_info = ""
            if parent_code:
                parent_exists = ExternalDistrictNode.objects.filter(code=parent_code).exists()
                if parent_exists:
                    parent_info = f", 父节点: {parent_code}"
                else:
                    parent_info = f", 父节点: {parent_code} (不存在，将作为顶层节点)"
            
            self.stdout.write(f"🔍 将{action}节点: {code} - {name}{parent_info}")

    @transaction.atomic
    def _import_nodes(self, sorted_nodes):
        """实际导入数据"""
        created_count = 0
        updated_count = 0
        error_count = 0
        
        for node_data in sorted_nodes:
            try:
                code = str(node_data['id'])
                name = node_data['name']
                parent_code = str(node_data['pId']) if node_data.get('pId') else None
                
                # 查找父节点
                parent_instance = None
                if parent_code:
                    try:
                        parent_instance = ExternalDistrictNode.objects.get(code=parent_code)
                    except ExternalDistrictNode.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠ 节点 {code}({name}) 的父节点 {parent_code} 不存在，将作为顶层节点处理'
                            )
                        )
                        parent_instance = None
                
                # 创建或更新节点
                node, created = ExternalDistrictNode.objects.update_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'parent': parent_instance
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f"✓ 创建节点: {code} - {name}")
                else:
                    updated_count += 1
                    self.stdout.write(f"✓ 更新节点: {code} - {name}")
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ 处理节点 {node_data} 时出错: {e}')
                )
        
        # 输出统计信息
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== 导入完成 ==='))
        self.stdout.write(f'创建节点数: {created_count}')
        self.stdout.write(f'更新节点数: {updated_count}')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'错误节点数: {error_count}'))
        self.stdout.write(f'总处理数: {len(sorted_nodes)}')
        
        # 验证数据
        total_in_db = ExternalDistrictNode.objects.count()
        self.stdout.write(f'数据库中总节点数: {total_in_db}')
        
        if error_count == 0:
            self.stdout.write(
                self.style.SUCCESS('🎉 所有数据导入成功！')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ 导入完成，但有 {error_count} 个错误')
            )
