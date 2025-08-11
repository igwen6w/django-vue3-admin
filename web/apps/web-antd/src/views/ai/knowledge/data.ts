import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { AiKnowledgeApi } from '#/models/ai/knowledge';

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
      fieldName: 'name',
      label: '知识库名称',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['知识库名称']))
        .max(100, $t('ui.formRules.maxLength', ['知识库名称', 100])),
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'description',
      label: '知识库描述',
      rules: z
        .string()
        .max(500, $t('ui.formRules.maxLength', ['知识库描述', 500]))
        .optional(),
    },
    {
      component: 'Input',
      fieldName: 'embedding_model_id',
      label: '向量模型编号',
    },
    {
      component: 'Input',
      fieldName: 'embedding_model',
      label: '向量模型标识',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['向量模型标识']))
        .max(100, $t('ui.formRules.maxLength', ['向量模型标识', 100])),
    },
    { component: 'InputNumber', fieldName: 'top_k', label: 'topK' },
    {
      component: 'Input',
      fieldName: 'similarity_threshold',
      label: '相似度阈值',
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
    { component: 'Input', fieldName: 'name', label: '知识库名称' },
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
  onActionClick?: OnActionClickFn<AiKnowledgeApi.AiKnowledge>,
): VxeTableGridOptions<AiKnowledgeApi.AiKnowledge>['columns'] {
  return [
    { field: 'id', title: 'ID' },
    { field: 'name', title: '知识库名称' },
    { field: 'description', title: '知识库描述' },
    { field: 'embedding_model_id', title: '向量模型编号' },
    { field: 'embedding_model', title: '向量模型标识' },
    { field: 'top_k', title: 'topK' },
    { field: 'similarity_threshold', title: '相似度阈值' },
    { field: 'status', title: '状态', cellRender: { name: 'CellTag' } },
    { field: 'remark', title: '备注' },
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
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('ai.knowledge.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('ai:knowledge:edit', 'edit'),
          op('ai:knowledge:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
