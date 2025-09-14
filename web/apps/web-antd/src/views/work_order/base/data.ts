import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { WorkOrderBaseApi } from '#/models/work_order/base';

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
      fieldName: 'work_order_no',
      label: '工单编号',
      componentProps: { style: { width: '100px', marginRight: '10px' } },
      rules: z.string().min(1, $t('ui.formRules.required', ['工单编号'])),
    },
    {
      component: 'Input',
      fieldName: 'contact_method',
      label: '联系方式',
      componentProps: { style: { width: '100px', marginRight: '10px' } },
      rules: z.string().min(1, $t('ui.formRules.required', ['联系方式'])),
    },
    {
      component: 'Select',
      fieldName: 'business_type',
      label: '业务类型',
      componentProps: { style: { width: '100px', marginRight: '10px' } },
      rules: z.string().min(1, $t('ui.formRules.required', ['业务类型'])),
      options: [
        { label: '类型A', value: 'A' },
        { label: '类型B', value: 'B' },
      ],
    },
    {
      component: 'Select',
      fieldName: 'accept_method',
      label: '受理方式',
      componentProps: { style: { width: '100px', marginRight: '10px' }, mode: 'multiple' },
      rules: z.array(z.string()).min(1, $t('ui.formRules.required', ['受理方式'])),
      options: [
        { label: '电话', value: 'phone' },
        { label: '邮件', value: 'email' },
        { label: '现场', value: 'onsite' },
      ],
    },
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
      component: 'InputNumber',
      fieldName: 'external_id',
      label: '工单ID',
    },
    {
      component: 'Input',
      fieldName: 'external_roll_number',
      label: '工单编号',
      componentProps: { style: { width: '100px' } },
      rules: z.string().min(1, $t('ui.formRules.required', ['工单编号'])).max(100, $t('ui.formRules.maxLength', ['工单编号', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_handle_rel_expire_time',
      label: '处置实际到期时间',
      rules: z.string().min(1, $t('ui.formRules.required', ['处置实际到期时间'])).max(100, $t('ui.formRules.maxLength', ['处置实际到期时间', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_src_way',
      label: '受理方式',
      rules: z.string().min(1, $t('ui.formRules.required', ['受理方式'])).max(100, $t('ui.formRules.maxLength', ['受理方式', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_payroll_name',
      label: '姓名',
      rules: z.string().min(1, $t('ui.formRules.required', ['姓名'])).max(100, $t('ui.formRules.maxLength', ['姓名', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_company_tel',
      label: '联系方式',
      rules: z.string().min(1, $t('ui.formRules.required', ['联系方式'])).max(100, $t('ui.formRules.maxLength', ['联系方式', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_addr',
      label: '地址',
      rules: z.string().min(1, $t('ui.formRules.required', ['地址'])).max(100, $t('ui.formRules.maxLength', ['地址', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_region_district_id',
      label: '区域',
      rules: z.string().min(1, $t('ui.formRules.required', ['区域'])).max(100, $t('ui.formRules.maxLength', ['区域', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note14',
      label: '是否回访',
      rules: z.string().min(1, $t('ui.formRules.required', ['是否回访'])).max(100, $t('ui.formRules.maxLength', ['是否回访', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_distribute_way',
      label: '企业名称',
      rules: z.string().min(1, $t('ui.formRules.required', ['企业名称'])).max(100, $t('ui.formRules.maxLength', ['企业名称', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_payroll_type',
      label: '业务类别',
      rules: z.string().min(1, $t('ui.formRules.required', ['业务类别'])).max(100, $t('ui.formRules.maxLength', ['业务类别', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_event_type2_id',
      label: '事件类型',
      rules: z.string().min(1, $t('ui.formRules.required', ['事件类型'])).max(100, $t('ui.formRules.maxLength', ['事件类型', 100])),
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'external_roll_content',
      label: '事件描述',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['事件描述', 500])).optional(),
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'external_note',
      label: '备注',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['备注', 500])).optional(),
    },
    {
      component: 'Input',
      fieldName: 'external_product_ids',
      label: '三级复核',
      rules: z.string().min(1, $t('ui.formRules.required', ['三级复核'])).max(100, $t('ui.formRules.maxLength', ['三级复核', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_addr2',
      label: '区县复核',
      rules: z.string().min(1, $t('ui.formRules.required', ['区县复核'])).max(100, $t('ui.formRules.maxLength', ['区县复核', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_company_address',
      label: '满意研判',
      rules: z.string().min(1, $t('ui.formRules.required', ['满意研判'])).max(100, $t('ui.formRules.maxLength', ['满意研判', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_order_number',
      label: '解决研判',
      rules: z.string().min(1, $t('ui.formRules.required', ['解决研判'])).max(100, $t('ui.formRules.maxLength', ['解决研判', 100])),
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'external_normal_payroll_title',
      label: '复核原因',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['复核原因', 500])).optional(),
    },
    {
      component: 'Input',
      fieldName: 'external_addr3',
      label: '满意复核',
      rules: z.string().min(1, $t('ui.formRules.required', ['满意复核'])).max(100, $t('ui.formRules.maxLength', ['满意复核', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note1',
      label: '解决复核',
      rules: z.string().min(1, $t('ui.formRules.required', ['解决复核'])).max(100, $t('ui.formRules.maxLength', ['解决复核', 100])),
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'external_note15',
      label: '市复核意见',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['市复核意见', 500])).optional(),
    },
    {
      component: 'Input',
      fieldName: 'external_attachments',
      label: '附件',
    },
    {
      component: 'Input',
      fieldName: 'external_note4',
      label: '是否考核',
      rules: z.string().min(1, $t('ui.formRules.required', ['是否考核'])).max(100, $t('ui.formRules.maxLength', ['是否考核', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_handling_quality',
      label: '办理满意',
      rules: z.string().min(1, $t('ui.formRules.required', ['办理满意'])).max(100, $t('ui.formRules.maxLength', ['办理满意', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note12',
      label: '过程满意',
      rules: z.string().min(1, $t('ui.formRules.required', ['过程满意'])).max(100, $t('ui.formRules.maxLength', ['过程满意', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note2',
      label: '是否解决',
      rules: z.string().min(1, $t('ui.formRules.required', ['是否解决'])).max(100, $t('ui.formRules.maxLength', ['是否解决', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note3',
      label: '办理回复',
      rules: z.string().min(1, $t('ui.formRules.required', ['办理回复'])).max(100, $t('ui.formRules.maxLength', ['办理回复', 100])),
    },
    {
      component: 'Input',
      fieldName: 'external_note16',
      label: '自主研判',
      rules: z.string().min(1, $t('ui.formRules.required', ['自主研判'])).max(100, $t('ui.formRules.maxLength', ['自主研判', 100])),
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'external_note17',
      label: '研判原因',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['研判原因', 500])).optional(),
    },
    {
      component: 'Input',
      fieldName: 'current_node',
      label: '当前节点',
      rules: z.string().min(1, $t('ui.formRules.required', ['当前节点'])).max(100, $t('ui.formRules.maxLength', ['当前节点', 100])),
    },
    {
      component: 'Input',
      fieldName: 'work_flow',
      label: '工单流程',
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
      fieldName: 'external_roll_number',
      label: '工单编号',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_src_way',
      label: '受理方式',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Input',
      fieldName: 'external_company_tel',
      label: '联系方式',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    // {
    //   component: 'Input',
    //   fieldName: 'external_note14',
    //   label: '是否回访',
    //   componentProps: { style: { minWidth: '120px', width: 'auto' } }
    // },
    {
      component: 'Select',
      fieldName: 'external_distribute_way',
      label: '企业名称',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_payroll_type',
      label: '业务类别',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_event_type2_id',
      label: '事件类型',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_product_ids',
      label: '三级复核',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_addr2',
      label: '区县复核',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_company_address',
      label: '满意研判',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_order_number',
      label: '解决研判',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_addr3',
      label: '满意复核',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_note1',
      label: '解决复核',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_note4',
      label: '是否考核',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_handling_quality',
      label: '办理满意',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_note12',
      label: '过程满意',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_note2',
      label: '是否解决',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_note3',
      label: '办理回复',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
    {
      component: 'Select',
      fieldName: 'external_note16',
      label: '自主研判',
      componentProps: { style: { minWidth: '120px', width: 'auto' } }
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<WorkOrderBaseApi.WorkOrderBase>,
): VxeTableGridOptions<WorkOrderBaseApi.WorkOrderBase>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    // {
    //   field: 'version',
    //   title: '版本',
    // },
    // {
    //   field: 'source_system',
    //   title: '来源标识',
    // },
    // {
    //   field: 'sync_task_name',
    //   title: '同步任务名称',
    // },
    // {
    //   field: 'sync_task_id',
    //   title: '同步任务ID',
    // },
    // {
    //   field: 'sync_status',
    //   title: '同步状态',
    // },
    // {
    //   field: 'sync_time',
    //   title: '同步时间',
    //   width: 150,
    //   formatter: ({ cellValue }) => format_datetime(cellValue),
    // },
    // {
    //   field: 'external_id',
    //   title: '工单ID',
    // },
    {
      field: 'external_roll_number',
      title: '工单编号',
    },
    {
      field: 'external_handle_rel_expire_time',
      title: '处置实际到期时间',
    },
    {
      field: 'external_src_way',
      title: '受理方式',
    },
    {
      field: 'external_payroll_name',
      title: '姓名',
    },
    {
      field: 'external_company_tel',
      title: '联系方式',
    },
    // {
    //   field: 'external_addr',
    //   title: '地址',
    // },
    {
      field: 'external_region_district_id',
      title: '区域',
    },
    {
      field: 'external_note14',
      title: '是否回访',
    },
    // {
    //   field: 'external_distribute_way',
    //   title: '企业名称',
    // },
    {
      field: 'external_payroll_type',
      title: '业务类别',
    },
    {
      field: 'external_event_type2_id',
      title: '事件类型',
    },
    {
      field: 'external_roll_content',
      title: '事件描述',
    },
    // {
    //   field: 'external_note',
    //   title: '备注',
    // },
    // {
    //   field: 'external_product_ids',
    //   title: '三级复核',
    // },
    // {
    //   field: 'external_addr2',
    //   title: '区县复核',
    // },
    {
      field: 'external_company_address',
      title: '满意研判',
    },
    {
      field: 'external_order_number',
      title: '解决研判',
    },
    // {
    //   field: 'external_normal_payroll_title',
    //   title: '复核原因',
    // },
    {
      field: 'external_addr3',
      title: '满意复核',
    },
    {
      field: 'external_note1',
      title: '解决复核',
    },
    {
      field: 'external_note15',
      title: '市复核意见',
    },
    // {
    //   field: 'external_attachments',
    //   title: '附件',
    // },
    {
      field: 'external_note4',
      title: '是否考核',
    },
    {
      field: 'external_handling_quality',
      title: '办理满意',
    },
    {
      field: 'external_note12',
      title: '过程满意',
    },
    {
      field: 'external_note2',
      title: '是否解决',
    },
    {
      field: 'external_note3',
      title: '办理回复',
    },
    {
      field: 'external_note16',
      title: '自主研判',
    },
    {
      field: 'external_note17',
      title: '研判原因',
    },
    // {
    //   field: 'current_node',
    //   title: '当前节点',
    // },
    // {
    //   field: 'work_flow',
    //   title: '工单流程',
    // },
    // {
    //   field: 'remark',
    //   title: '备注',
    // },
    // {
    //   field: 'creator',
    //   title: '创建人',
    // },
    // {
    //   field: 'modifier',
    //   title: '修改人',
    // },
    // {
    //   field: 'update_time',
    //   title: '修改时间',
    //   width: 150,
    //   formatter: ({ cellValue }) => format_datetime(cellValue),
    // },
    // {
    //   field: 'create_time',
    //   title: '创建时间',
    //   width: 150,
    //   formatter: ({ cellValue }) => format_datetime(cellValue),
    // },
    // {
    //   field: 'is_deleted',
    //   title: '是否软删除',
    // },
    {
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('work_order.base.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('work_order:base:edit', 'edit'),
          op('work_order:base:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
