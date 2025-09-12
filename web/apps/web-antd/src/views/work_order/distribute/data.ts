import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { WorkOrderDistributeApi } from '#/models/work_order/distribute';

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
      fieldName: 'base',
      label: '工单',
    },
    {
      component: 'Input',
      fieldName: 'external_ps_caption',
      label: 'ps_caption',
      rules: z.string().min(1, $t('ui.formRules.required', ['ps_caption'])).max(100, $t('ui.formRules.maxLength', ['ps_caption', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_record_number',
      label: '工单编号',
      rules: z.string().min(1, $t('ui.formRules.required', ['工单编号'])).max(100, $t('ui.formRules.maxLength', ['工单编号', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'external_public_record',
      label: 'public_record',
    },
    {
      component: 'Input',
      fieldName: 'external_user_id_hide',
      label: 'user_id_hide',
      rules: z.string().min(1, $t('ui.formRules.required', ['user_id_hide'])).max(100, $t('ui.formRules.maxLength', ['user_id_hide', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_co_di_ids',
      label: 'co_di_ids',
    },
    {
      component: 'Input',
      fieldName: 'external_co_di_ids_hide',
      label: 'co_di_ids_hide',
    },
    {
      component: 'Input',
      fieldName: 'external_pss_status_attr',
      label: 'pss_status_attr',
      rules: z.string().min(1, $t('ui.formRules.required', ['pss_status_attr'])).max(100, $t('ui.formRules.maxLength', ['pss_status_attr', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_di_ids',
      label: '单位名称',
    },
    {
      component: 'Input',
      fieldName: 'external_di_ids_hide',
      label: '单位ID',
    },
    {
      component: 'Input',
      fieldName: 'external_psot_name',
      label: 'psot_name',
      rules: z.string().min(1, $t('ui.formRules.required', ['psot_name'])).max(100, $t('ui.formRules.maxLength', ['psot_name', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_psot_attr',
      label: 'psot_attr',
      rules: z.string().min(1, $t('ui.formRules.required', ['psot_attr'])).max(100, $t('ui.formRules.maxLength', ['psot_attr', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_pso_caption',
      label: 'pso_caption',
      rules: z.string().min(1, $t('ui.formRules.required', ['pso_caption'])).max(100, $t('ui.formRules.maxLength', ['pso_caption', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_dept_send_msg',
      label: '单位ID',
      rules: z.string().min(1, $t('ui.formRules.required', ['单位ID'])).max(100, $t('ui.formRules.maxLength', ['单位ID', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note',
      label: '办理情况',
      rules: z.string().min(1, $t('ui.formRules.required', ['办理情况'])).max(100, $t('ui.formRules.maxLength', ['办理情况', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'external_expires',
      label: '办理期限',
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
      fieldName: 'base',
      label: '工单',
    },
    {
      component: 'Input',
      fieldName: 'external_ps_caption',
      label: 'ps_caption',
    },
    {
      component: 'Input',
      fieldName: 'external_record_number',
      label: '工单编号',
    },
    {
      component: 'InputNumber',
      fieldName: 'external_public_record',
      label: 'public_record',
    },
    {
      component: 'Input',
      fieldName: 'external_user_id_hide',
      label: 'user_id_hide',
    },
    {
      component: 'Input',
      fieldName: 'external_co_di_ids',
      label: 'co_di_ids',
    },
    {
      component: 'Input',
      fieldName: 'external_co_di_ids_hide',
      label: 'co_di_ids_hide',
    },
    {
      component: 'Input',
      fieldName: 'external_pss_status_attr',
      label: 'pss_status_attr',
    },
    {
      component: 'Input',
      fieldName: 'external_di_ids',
      label: '单位名称',
    },
    {
      component: 'Input',
      fieldName: 'external_di_ids_hide',
      label: '单位ID',
    },
    {
      component: 'Input',
      fieldName: 'external_psot_name',
      label: 'psot_name',
    },
    {
      component: 'Input',
      fieldName: 'external_psot_attr',
      label: 'psot_attr',
    },
    {
      component: 'Input',
      fieldName: 'external_pso_caption',
      label: 'pso_caption',
    },
    {
      component: 'Input',
      fieldName: 'external_dept_send_msg',
      label: '单位ID',
    },
    {
      component: 'Input',
      fieldName: 'external_note',
      label: '办理情况',
    },
    {
      component: 'InputNumber',
      fieldName: 'external_expires',
      label: '办理期限',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<WorkOrderDistributeApi.WorkOrderDistribute>,
): VxeTableGridOptions<WorkOrderDistributeApi.WorkOrderDistribute>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'base',
      title: '工单',
    },
    {
      field: 'external_ps_caption',
      title: 'ps_caption',
    },
    {
      field: 'external_record_number',
      title: '工单编号',
    },
    {
      field: 'external_public_record',
      title: 'public_record',
    },
    {
      field: 'external_user_id_hide',
      title: 'user_id_hide',
    },
    {
      field: 'external_co_di_ids',
      title: 'co_di_ids',
    },
    {
      field: 'external_co_di_ids_hide',
      title: 'co_di_ids_hide',
    },
    {
      field: 'external_pss_status_attr',
      title: 'pss_status_attr',
    },
    {
      field: 'external_di_ids',
      title: '单位名称',
    },
    {
      field: 'external_di_ids_hide',
      title: '单位ID',
    },
    {
      field: 'external_psot_name',
      title: 'psot_name',
    },
    {
      field: 'external_psot_attr',
      title: 'psot_attr',
    },
    {
      field: 'external_pso_caption',
      title: 'pso_caption',
    },
    {
      field: 'external_dept_send_msg',
      title: '单位ID',
    },
    {
      field: 'external_note',
      title: '办理情况',
    },
    {
      field: 'external_expires',
      title: '办理期限',
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
          nameTitle: $t('work_order.distribute.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('work_order:distribute:edit', 'edit'),
          op('work_order:distribute:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
