import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { WorkOrderMetaApi } from '#/models/work_order/meta';

import { z } from '#/adapter/form';
import { $t } from '#/locales';
import { format_datetime } from '#/utils/date';
import { op } from '#/utils/permission';

/**
 * 获取编辑表单的字段配置
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'version',
      label: '版本',
      rules: z.string().min(1, $t('ui.formRules.required', ['版本'])).max(100, $t('ui.formRules.maxLength', ['版本', 100])),
    },
    {
      component: 'Input',
      fieldName: 'source_system',
      label: '来源标识',
      rules: z.string().min(1, $t('ui.formRules.required', ['来源标识'])).max(100, $t('ui.formRules.maxLength', ['来源标识', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'sync_task_id',
      label: '同步任务ID',
    },
    {
      component: 'RadioGroup',
      componentProps: {
        buttonStyle: 'solid',
        options: [
          { label: '开启', value: 1 },
          { label: '关闭', value: 0 },
        ],
        optionType: 'button',
      },
      defaultValue: 1,
      fieldName: 'sync_status',
      label: '同步状态',
    },
    {
      component: 'Input',
      fieldName: 'sync_time',
      label: '同步时间',
    },
    {
      component: 'Input',
      fieldName: 'raw_data',
      label: '工单信息',
    },
    {
      component: 'InputNumber',
      fieldName: 'pull_task_id',
      label: '拉取任务ID',
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: '备注',
      rules: z.string().min(1, $t('ui.formRules.required', ['备注'])).max(100, $t('ui.formRules.maxLength', ['备注', 100])),
    },
  ];
}

/**
 * 获取编辑表单的字段配置
 */
export function useGridFormSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'version',
      label: '版本',
    },
    {
      component: 'Input',
      fieldName: 'source_system',
      label: '来源标识',
    },
    {
      component: 'InputNumber',
      fieldName: 'sync_task_id',
      label: '同步任务ID',
    },
    {
      component: 'Input',
      fieldName: 'sync_status',
      label: '同步状态',
    },
    {
      component: 'Input',
      fieldName: 'sync_time',
      label: '同步时间',
    },
    {
      component: 'Input',
      fieldName: 'raw_data',
      label: '工单信息',
    },
    {
      component: 'InputNumber',
      fieldName: 'pull_task_id',
      label: '拉取任务ID',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<WorkOrderMetaApi.WorkOrderMeta>,
): VxeTableGridOptions<WorkOrderMetaApi.WorkOrderMeta>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'version',
      title: '版本',
    },
    {
      field: 'source_system',
      title: '来源标识',
    },
    {
      field: 'sync_task_id',
      title: '同步任务ID',
    },
    {
      field: 'sync_status',
      title: '同步状态',
    },
    {
      field: 'sync_time',
      title: '同步时间',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      field: 'raw_data',
      title: '工单信息',
    },
    {
      field: 'pull_task_id',
      title: '拉取任务ID',
    },
    {
      field: 'remark',
      title: '备注',
    },
    {
      field: 'creator',
      title: '创建人',
    },
    {
      field: 'modifier',
      title: '修改人',
    },
    {
      field: 'update_time',
      title: '修改时间',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      field: 'create_time',
      title: '创建时间',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      field: 'is_deleted',
      title: '是否软删除',
    },
    {
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('work_order.meta.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('work_order:meta:edit', 'edit'),
          op('work_order:meta:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
