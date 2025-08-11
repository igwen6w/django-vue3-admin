import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { AiChatMessageApi } from '#/models/ai/chat_message';

import { z } from '#/adapter/form';
import { $t } from '#/locales';
import { format_datetime } from '#/utils/date';

/**
 * 获取编辑表单的字段配置
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'InputNumber',
      fieldName: 'conversation_id',
      label: '对话编号',
    },
    {
      component: 'Input',
      fieldName: 'user',
      label: '用户',
    },
    {
      component: 'Input',
      fieldName: 'role',
      label: '聊天角色',
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
      fieldName: 'model_id',
      label: '向量模型编号',
    },
    {
      component: 'Input',
      fieldName: 'type',
      label: '消息类型',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['消息类型']))
        .max(100, $t('ui.formRules.maxLength', ['消息类型', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'reply_id',
      label: '回复编号',
    },
    {
      component: 'Input',
      fieldName: 'content',
      label: '消息内容',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['消息内容']))
        .max(100, $t('ui.formRules.maxLength', ['消息内容', 100])),
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
      fieldName: 'use_context',
      label: '是否携带上下文',
    },
    {
      component: 'Input',
      fieldName: 'segment_ids',
      label: '段落编号数组',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['段落编号数组']))
        .max(100, $t('ui.formRules.maxLength', ['段落编号数组', 100])),
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: '备注',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['备注']))
        .max(100, $t('ui.formRules.maxLength', ['备注', 100])),
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
      fieldName: 'user',
      label: '用户',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<AiChatMessageApi.AiChatMessage>,
): VxeTableGridOptions<AiChatMessageApi.AiChatMessage>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'conversation_id',
      title: '对话编号',
    },
    {
      field: 'username',
      title: '用户',
    },
    {
      field: 'role',
      title: '聊天角色',
    },
    {
      field: 'model',
      title: '模型标识',
      width: 150,
    },
    {
      field: 'model_id',
      title: '向量模型编号',
    },
    {
      field: 'type',
      title: '消息类型',
    },
    {
      field: 'reply_id',
      title: '回复编号',
    },
    {
      field: 'content',
      title: '消息内容',
      width: 200,
    },
    {
      field: 'use_context',
      title: '是否携带上下文',
    },
    {
      field: 'segment_ids',
      title: '段落编号数组',
    },
    {
      field: 'create_time',
      title: '创建时间',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
  ];
}
