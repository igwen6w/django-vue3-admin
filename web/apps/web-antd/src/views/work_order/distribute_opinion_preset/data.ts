import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { WorkOrderDistributeOpinionPresetApi } from '#/models/work_order/distribute_opinion_preset';

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
      fieldName: 'dept',
      label: '部门',
    },
    {
      component: 'Input',
      fieldName: 'category',
      label: '分类',
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'description',
      label: '下派意见预设',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['下派意见预设', 500])).optional(),
    },
    {
      component: 'Input',
      fieldName: 'title',
      label: '标题',
      rules: z.string().min(1, $t('ui.formRules.required', ['标题'])).max(100, $t('ui.formRules.maxLength', ['标题', 100])),
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
      fieldName: 'dept',
      label: '部门',
    },
    {
      component: 'Input',
      fieldName: 'category',
      label: '分类',
    },
    {
      component: 'Input',
      fieldName: 'description',
      label: '下派意见预设',
    },
    {
      component: 'Input',
      fieldName: 'title',
      label: '标题',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<WorkOrderDistributeOpinionPresetApi.WorkOrderDistributeOpinionPreset>,
): VxeTableGridOptions<WorkOrderDistributeOpinionPresetApi.WorkOrderDistributeOpinionPreset>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'dept',
      title: '部门',
    },
    {
      field: 'category',
      title: '分类',
    },
    {
      field: 'description',
      title: '下派意见预设',
    },
    {
      field: 'title',
      title: '标题',
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
          nameTitle: $t('work_order.distribute_opinion_preset.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('work_order:distribute_opinion_preset:edit', 'edit'),
          op('work_order:distribute_opinion_preset:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
