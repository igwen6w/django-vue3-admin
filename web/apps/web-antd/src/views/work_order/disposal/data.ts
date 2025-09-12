import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { WorkOrderDisposalApi } from '#/models/work_order/disposal';

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
      component: 'Input',
      fieldName: 'sync_task_name',
      label: '同步任务名称',
      rules: z.string().min(1, $t('ui.formRules.required', ['同步任务名称'])).max(100, $t('ui.formRules.maxLength', ['同步任务名称', 100])),
    },
    {
      component: 'Input',
      fieldName: 'sync_task_id',
      label: '同步任务ID',
      rules: z.string().min(1, $t('ui.formRules.required', ['同步任务ID'])).max(100, $t('ui.formRules.maxLength', ['同步任务ID', 100])),
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
      rules: z.string().min(1, $t('ui.formRules.required', ['co_di_ids'])).max(100, $t('ui.formRules.maxLength', ['co_di_ids', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_co_di_ids_hide',
      label: 'co_di_ids_hide',
      rules: z.string().min(1, $t('ui.formRules.required', ['co_di_ids_hide'])).max(100, $t('ui.formRules.maxLength', ['co_di_ids_hide', 100])),
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
      label: 'di_ids',
      rules: z.string().min(1, $t('ui.formRules.required', ['di_ids'])).max(100, $t('ui.formRules.maxLength', ['di_ids', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_di_ids_hide',
      label: 'di_ids_hide',
      rules: z.string().min(1, $t('ui.formRules.required', ['di_ids_hide'])).max(100, $t('ui.formRules.maxLength', ['di_ids_hide', 100])),
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
      fieldName: 'external_note1',
      label: '诉求属实',
      rules: z.string().min(1, $t('ui.formRules.required', ['诉求属实'])).max(100, $t('ui.formRules.maxLength', ['诉求属实', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_distribute_way',
      label: '超职责诉求',
      rules: z.string().min(1, $t('ui.formRules.required', ['超职责诉求'])).max(100, $t('ui.formRules.maxLength', ['超职责诉求', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note8',
      label: '申请类型',
      rules: z.string().min(1, $t('ui.formRules.required', ['申请类型'])).max(100, $t('ui.formRules.maxLength', ['申请类型', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_d_attachments',
      label: '附件',
    },
    {
      component: 'Input',
      fieldName: 'external_note3',
      label: '联系群众',
      rules: z.string().min(1, $t('ui.formRules.required', ['联系群众'])).max(100, $t('ui.formRules.maxLength', ['联系群众', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note4',
      label: '联系号码',
      rules: z.string().min(1, $t('ui.formRules.required', ['联系号码'])).max(100, $t('ui.formRules.maxLength', ['联系号码', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note5',
      label: '联系时间',
      rules: z.string().min(1, $t('ui.formRules.required', ['联系时间'])).max(100, $t('ui.formRules.maxLength', ['联系时间', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note6',
      label: '是否解决',
      rules: z.string().min(1, $t('ui.formRules.required', ['是否解决'])).max(100, $t('ui.formRules.maxLength', ['是否解决', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note11',
      label: '未解决原因',
      rules: z.string().min(1, $t('ui.formRules.required', ['未解决原因'])).max(100, $t('ui.formRules.maxLength', ['未解决原因', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note',
      label: '办理情况',
      rules: z.string().min(1, $t('ui.formRules.required', ['办理情况'])).max(100, $t('ui.formRules.maxLength', ['办理情况', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note10',
      label: '公开答复内容',
      rules: z.string().min(1, $t('ui.formRules.required', ['公开答复内容'])).max(100, $t('ui.formRules.maxLength', ['公开答复内容', 100])),
    },
    {
      component: 'Input',
      fieldName: 'attachments_credentials',
      label: '证件附件',
    },
    {
      component: 'Input',
      fieldName: 'attachments_contact',
      label: '联系证据',
    },
    {
      component: 'Input',
      fieldName: 'attachments_handle',
      label: '办理附件',
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
      component: 'Input',
      fieldName: 'sync_task_name',
      label: '同步任务名称',
    },
    {
      component: 'Input',
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
      label: 'di_ids',
    },
    {
      component: 'Input',
      fieldName: 'external_di_ids_hide',
      label: 'di_ids_hide',
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
      fieldName: 'external_note1',
      label: '诉求属实',
    },
    {
      component: 'Input',
      fieldName: 'external_distribute_way',
      label: '超职责诉求',
    },
    {
      component: 'Input',
      fieldName: 'external_note8',
      label: '申请类型',
    },
    {
      component: 'Input',
      fieldName: 'external_d_attachments',
      label: '附件',
    },
    {
      component: 'Input',
      fieldName: 'external_note3',
      label: '联系群众',
    },
    {
      component: 'Input',
      fieldName: 'external_note4',
      label: '联系号码',
    },
    {
      component: 'Input',
      fieldName: 'external_note5',
      label: '联系时间',
    },
    {
      component: 'Input',
      fieldName: 'external_note6',
      label: '是否解决',
    },
    {
      component: 'Input',
      fieldName: 'external_note11',
      label: '未解决原因',
    },
    {
      component: 'Input',
      fieldName: 'external_note',
      label: '办理情况',
    },
    {
      component: 'Input',
      fieldName: 'external_note10',
      label: '公开答复内容',
    },
    {
      component: 'Input',
      fieldName: 'attachments_credentials',
      label: '证件附件',
    },
    {
      component: 'Input',
      fieldName: 'attachments_contact',
      label: '联系证据',
    },
    {
      component: 'Input',
      fieldName: 'attachments_handle',
      label: '办理附件',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<WorkOrderDisposalApi.WorkOrderDisposal>,
): VxeTableGridOptions<WorkOrderDisposalApi.WorkOrderDisposal>['columns'] {
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
      field: 'sync_task_name',
      title: '同步任务名称',
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
      title: 'di_ids',
    },
    {
      field: 'external_di_ids_hide',
      title: 'di_ids_hide',
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
      field: 'external_note1',
      title: '诉求属实',
    },
    {
      field: 'external_distribute_way',
      title: '超职责诉求',
    },
    {
      field: 'external_note8',
      title: '申请类型',
    },
    {
      field: 'external_d_attachments',
      title: '附件',
    },
    {
      field: 'external_note3',
      title: '联系群众',
    },
    {
      field: 'external_note4',
      title: '联系号码',
    },
    {
      field: 'external_note5',
      title: '联系时间',
    },
    {
      field: 'external_note6',
      title: '是否解决',
    },
    {
      field: 'external_note11',
      title: '未解决原因',
    },
    {
      field: 'external_note',
      title: '办理情况',
    },
    {
      field: 'external_note10',
      title: '公开答复内容',
    },
    {
      field: 'attachments_credentials',
      title: '证件附件',
    },
    {
      field: 'attachments_contact',
      title: '联系证据',
    },
    {
      field: 'attachments_handle',
      title: '办理附件',
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
          nameTitle: $t('work_order.disposal.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('work_order:disposal:edit', 'edit'),
          op('work_order:disposal:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
