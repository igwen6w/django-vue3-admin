import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { AiAIApiKeyApi } from '#/models/ai/ai_api_key';

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
      label: 'name',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['name']))
        .max(100, $t('ui.formRules.maxLength', ['name', 100])),
    },
    {
      component: 'Input',
      fieldName: 'platform',
      label: 'platform',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['platform']))
        .max(100, $t('ui.formRules.maxLength', ['platform', 100])),
    },
    {
      component: 'Input',
      fieldName: 'api_key',
      label: 'api key',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['api key']))
        .max(100, $t('ui.formRules.maxLength', ['api key', 100])),
    },
    {
      component: 'Input',
      fieldName: 'url',
      label: 'url',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['url']))
        .max(100, $t('ui.formRules.maxLength', ['url', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'status',
      label: '状态',
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: 'remark',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['remark']))
        .max(100, $t('ui.formRules.maxLength', ['remark', 100])),
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
      label: 'name',
    },
    {
      component: 'Input',
      fieldName: 'platform',
      label: 'platform',
    },
    {
      component: 'Input',
      fieldName: 'api_key',
      label: 'api key',
    },
    {
      component: 'Input',
      fieldName: 'url',
      label: 'url',
    },
    {
      component: 'InputNumber',
      fieldName: 'status',
      label: '状态',
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: 'remark',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<AiAIApiKeyApi.AiAIApiKey>,
): VxeTableGridOptions<AiAIApiKeyApi.AiAIApiKey>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'name',
      title: 'name',
    },
    {
      field: 'platform',
      title: 'platform',
    },
    {
      field: 'api_key',
      title: 'api key',
    },
    {
      field: 'url',
      title: 'url',
    },
    {
      field: 'status',
      title: '状态',
    },
    {
      field: 'remark',
      title: 'remark',
    },
    {
      field: 'creator',
      title: 'creator',
    },
    {
      field: 'modifier',
      title: 'modifier',
    },
    {
      field: 'update_time',
      title: 'update time',
    },
    {
      field: 'create_time',
      title: 'create time',
    },
    {
      field: 'is_deleted',
      title: 'is deleted',
    },
    {
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('ai.ai_api_key.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('ai:ai_api_key:edit', 'edit'),
          op('ai:ai_api_key:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
