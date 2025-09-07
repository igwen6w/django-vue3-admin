import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ExternalPlatformPlatformApi } from '#/models/external_platform/platform';

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
      label: '名称',
      rules: z.string().min(1, $t('ui.formRules.required', ['name'])).max(100, $t('ui.formRules.maxLength', ['name', 100])),
    },
    {
      component: 'Input',
      fieldName: 'sign',
      label: '标识',
      rules: z.string().min(1, $t('ui.formRules.required', ['sign'])).max(100, $t('ui.formRules.maxLength', ['sign', 100])),
    },
    {
      component: 'Input',
      fieldName: 'base_url',
      label: '基础 URL',
      rules: z.string().min(1, $t('ui.formRules.required', ['base url'])).max(100, $t('ui.formRules.maxLength', ['base url', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'captcha_type',
      label: '验证码类型',
    },
    {
      component: 'InputNumber',
      fieldName: 'session_timeout_hours',
      label: '会话超时小时',
    },
    {
      component: 'InputNumber',
      fieldName: 'retry_limit',
      label: '最大重试次数',
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
      fieldName: 'is_active',
      label: '是否启用',
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'description',
      label: '描述',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['description', 500])).optional(),
    },
    {
      component: 'Textarea',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'login_config',
      label: '登录配置',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['login_config', 500])).optional(),
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
      fieldName: 'name',
      label: '名称',
    },
    {
      component: 'Input',
      fieldName: 'sign',
      label: '标识',
    },
    {
      component: 'Input',
      fieldName: 'base_url',
      label: '基础 URL',
    },
    {
      component: 'InputNumber',
      fieldName: 'captcha_type',
      label: '验证码类型',
    },
    {
      component: 'InputNumber',
      fieldName: 'session_timeout_hours',
      label: '会话超时小时',
    },
    {
      component: 'InputNumber',
      fieldName: 'retry_limit',
      label: '最大重试次数',
    },
    {
      component: 'Input',
      fieldName: 'is_active',
      label: '是否启用',
    },
    {
      component: 'Input',
      fieldName: 'description',
      label: '描述',
    },
    {
      component: 'Textarea',
      fieldName: 'login_config',
      label: '登录配置',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<ExternalPlatformPlatformApi.ExternalPlatformPlatform>,
): VxeTableGridOptions<ExternalPlatformPlatformApi.ExternalPlatformPlatform>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
      visible: false,
    },
    {
      field: 'name',
      title: '名称',
    },
    {
      field: 'sign',
      title: '标识',
    },
    {
      field: 'base_url',
      title: '基础 URL',
    },
    {
      field: 'captcha_type',
      title: '验证码类型',
    },
    {
      field: 'session_timeout_hours',
      title: '会话超时小时',
    },
    {
      field: 'retry_limit',
      title: '最大重试次数',
    },
    {
      field: 'is_active',
      title: '是否启用',
    },
    {
      field: 'description',
      title: '描述',
    },
    {
      field: 'login_config',
      title: '登录配置',
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
          nameTitle: $t('external_platform.platform.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('external_platform:platform:login', 'login'),
          op('external_platform:platform:edit', 'edit'),
          op('external_platform:platform:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
