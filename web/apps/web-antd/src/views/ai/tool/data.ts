import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { AiToolApi } from '#/models/ai/tool';

import { z } from '#/adapter/form';
import { $t } from '#/locales';
import { op } from '#/utils/permission';

/**
 * 获取编辑表单的字段配置
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'name',
      label: '工具名称',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['工具名称']))
        .max(100, $t('ui.formRules.maxLength', ['工具名称', 100])),
    },
    {
      component: 'Input',
      fieldName: 'description',
      label: '工具描述',
    },
    {
      component: 'RadioGroup',
      componentProps: {
        buttonStyle: 'solid',
        options: [
          { label: $t('common.enabled'), value: 1 },
          { label: $t('common.disabled'), value: 0 },
        ],
        optionType: 'button',
      },
      defaultValue: 1,
      fieldName: 'status',
      label: $t('system.status'),
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: '备注',
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
      fieldName: 'name',
      label: '工具名称',
    },
    {
      component: 'Input',
      fieldName: 'description',
      label: '工具描述',
    },
    {
      component: 'Select',
      fieldName: 'status',
      label: '状态',
      componentProps: {
        allowClear: true,
        options: [
          { label: '启用', value: 1 },
          { label: '禁用', value: 0 },
        ],
      },
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<AiToolApi.AiTool>,
): VxeTableGridOptions<AiToolApi.AiTool>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'name',
      title: '工具名称',
    },
    {
      field: 'description',
      title: '工具描述',
    },
    {
      cellRender: {
        name: 'CellTag',
      },
      field: 'status',
      title: '状态',
    },
    {
      field: 'remark',
      title: '备注',
    },
    {
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('ai.tool.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [op('ai:tool:edit', 'edit'), op('ai:tool:delete', 'delete')],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
