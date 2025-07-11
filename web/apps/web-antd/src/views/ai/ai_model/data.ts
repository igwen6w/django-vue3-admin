import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { AiAIModelApi } from '#/models/ai/ai_model';

import { z } from '#/adapter/form';
import { $t } from '#/locales';
import { AiAIApiKeyModel } from '#/models/ai/ai_api_key';
import { op } from '#/utils/permission';

const AiKeyModel = new AiAIApiKeyModel();

/**
 * 获取编辑表单的字段配置
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'name',
      label: '模型名字',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['模型名字']))
        .max(100, $t('ui.formRules.maxLength', ['模型名字', 100])),
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
      component: 'ApiSelect',
      componentProps: {
        api: () => AiKeyModel.list(),
        class: 'w-full',
        resultField: 'items',
        labelField: 'name',
        valueField: 'id',
      },
      fieldName: 'key',
      label: 'API 秘钥',
    },
    {
      component: 'InputNumber',
      fieldName: 'sort',
      label: '排序',
    },
    {
      component: 'Input',
      fieldName: 'platform',
      label: '模型平台',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['模型平台']))
        .max(100, $t('ui.formRules.maxLength', ['模型平台', 100])),
    },
    {
      component: 'Input',
      fieldName: 'model',
      label: '模型标识',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['模型标识']))
        .max(100, $t('ui.formRules.maxLength', ['模型标识', 100])),
    },
    {
      component: 'Input',
      fieldName: 'temperature',
      label: '温度参数',
    },
    {
      component: 'InputNumber',
      fieldName: 'max_tokens',
      label: '回复数 Token 数',
    },
    {
      component: 'InputNumber',
      fieldName: 'max_contexts',
      label: '上下文数量',
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
      label: '模型名字',
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
    {
      component: 'Input',
      fieldName: 'platform',
      label: '模型平台',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<AiAIModelApi.AiAIModel>,
): VxeTableGridOptions<AiAIModelApi.AiAIModel>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'name',
      title: '模型名字',
    },
    {
      field: 'sort',
      title: '排序',
    },
    {
      cellRender: {
        name: 'CellTag',
      },
      field: 'status',
      title: '状态',
    },
    {
      field: 'api_key_name',
      title: 'API 秘钥',
    },
    {
      field: 'platform',
      title: '模型平台',
    },
    {
      field: 'model',
      title: '模型标识',
    },
    {
      field: 'temperature',
      title: '温度参数',
    },
    {
      field: 'max_tokens',
      title: 'Token 数量',
    },
    {
      field: 'max_contexts',
      title: 'Message 数量',
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
          nameTitle: $t('ai.ai_model.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('ai:ai_model:edit', 'edit'),
          op('ai:ai_model:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
