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
      label: '名称',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['名称']))
        .max(100, $t('ui.formRules.maxLength', ['名称', 100])),
    },
    {
      component: 'Select',
      fieldName: 'platform',
      label: '平台',
      componentProps: {
        options: PLATFORM_OPTIONS,
        style: { minWidth: '180px' },
        dropdownStyle: { minWidth: '180px' },
      },
      rules: z.string(),
    },
    {
      component: 'Input',
      fieldName: 'api_key',
      label: '密钥',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['密钥']))
        .max(100, $t('ui.formRules.maxLength', ['密钥', 100])),
    },
    {
      component: 'Input',
      fieldName: 'url',
      label: '自定义 API 地址',
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
      label: $t('system.remark'),
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
      label: '名称',
    },
    {
      component: 'Select',
      fieldName: 'platform',
      label: '平台',
      componentProps: {
        allowClear: true,
        options: PLATFORM_OPTIONS,
      },
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
  onActionClick?: OnActionClickFn<AiAIApiKeyApi.AiAIApiKey>,
): VxeTableGridOptions<AiAIApiKeyApi.AiAIApiKey>['columns'] {
  // 平台映射表
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'name',
      title: '名称',
    },
    {
      cellRender: {
        name: 'CellTag',
      },
      field: 'platform',
      title: '平台',
      formatter: ({ cellValue }: { cellValue: string }) => {
        return PLATFORM_MAP[String(cellValue)] || String(cellValue);
      },
    },
    {
      field: 'url',
      title: '自定义 API 地址',
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

// 平台选项和映射常量
export const PLATFORM_OPTIONS = [
  { label: 'OpenAI 微软', value: 'AzureOpenAI' },
  { label: 'OpenAI', value: 'OpenAI' },
  { label: 'Ollama', value: 'Ollama' },
  { label: '文心一言', value: 'YiYan' },
  { label: '讯飞星火', value: 'XingHuo' },
  { label: '通义千问', value: 'TongYi' },
  { label: 'StableDiffusion', value: 'StableDiffusion' },
  { label: 'Midjourney', value: 'Midjourney' },
  { label: 'Suno', value: 'Suno' },
  { label: 'DeepSeek', value: 'DeepSeek' },
  { label: '字节豆包', value: 'DouBao' },
  { label: '腾讯混元', value: 'HunYuan' },
  { label: '硅基流动', value: 'SiliconFlow' },
  { label: '智谱', value: 'ZhiPu' },
  { label: 'MiniMax', value: 'MiniMax' },
  { label: '月之暗灭', value: 'Moonshot' },
  { label: '百川智能', value: 'BaiChuan' },
];
export const PLATFORM_MAP: Record<string, string> = Object.fromEntries(
  PLATFORM_OPTIONS.map((opt) => [opt.value, opt.label]),
);
