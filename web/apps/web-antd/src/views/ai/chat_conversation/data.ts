import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { AiChatConversationApi } from '#/models/ai/chat_conversation';

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
      fieldName: 'title',
      label: '对话标题',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['对话标题']))
        .max(100, $t('ui.formRules.maxLength', ['对话标题', 100])),
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
      fieldName: 'pinned',
      label: '是否置顶',
    },
    {
      component: 'Input',
      fieldName: 'pinned_time',
      label: '置顶时间',
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
      fieldName: 'model_id',
      label: '向量模型编号',
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
      fieldName: 'system_message',
      label: '角色设定',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['角色设定']))
        .max(100, $t('ui.formRules.maxLength', ['角色设定', 100])),
    },
    {
      component: 'Input',
      fieldName: 'temperature',
      label: '温度参数',
    },
    {
      component: 'InputNumber',
      fieldName: 'max_tokens',
      label: '单条回复的最大 Token 数量',
    },
    {
      component: 'InputNumber',
      fieldName: 'max_contexts',
      label: '上下文的最大 Message 数量',
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
      fieldName: 'title',
      label: '对话标题',
    },
    {
      component: 'Input',
      fieldName: 'user',
      label: '用户',
    },
    {
      component: 'Input',
      fieldName: 'model',
      label: '模型标识',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<AiChatConversationApi.AiChatConversation>,
): VxeTableGridOptions<AiChatConversationApi.AiChatConversation>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
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
      field: 'model_id',
      title: '向量模型编号',
    },
    {
      field: 'model',
      title: '模型标识',
    },
    {
      field: 'system_message',
      title: '角色设定',
    },
    {
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('ai.chat_conversation.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          // op('ai:chat_conversation:edit', 'edit'),
          // op('ai:chat_conversation:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
