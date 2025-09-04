import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ExternalPlatformRequestLogApi } from '#/models/external_platform/request_log';

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
      fieldName: 'platform',
      label: '外部平台',
    },
    {
      component: 'Input',
      fieldName: 'platform_endpoint',
      label: '平台端点',
    },
    {
      component: 'Input',
      fieldName: 'account',
      label: '账号',
      rules: z.string().min(1, $t('ui.formRules.required', ['账号'])).max(100, $t('ui.formRules.maxLength', ['账号', 100])),
    },
    {
      component: 'Input',
      fieldName: 'endpoint_path',
      label: '端点路径',
      rules: z.string().min(1, $t('ui.formRules.required', ['端点路径'])).max(100, $t('ui.formRules.maxLength', ['端点路径', 100])),
    },
    {
      component: 'Input',
      fieldName: 'method',
      label: '方法',
      rules: z.string().min(1, $t('ui.formRules.required', ['方法'])).max(100, $t('ui.formRules.maxLength', ['方法', 100])),
    },
    {
      component: 'Input',
      fieldName: 'payload',
      label: '请求参数',
    },
    {
      component: 'InputNumber',
      fieldName: 'status_code',
      label: '响应状态码',
    },
    {
      component: 'InputNumber',
      fieldName: 'response_time_ms',
      label: '响应耗时',
    },
    {
      component: 'Input',
      fieldName: 'response_body',
      label: '响应体',
    },
    {
      component: 'Input',
      fieldName: 'hook',
      label: '请求后钩子',
    },
    {
      component: 'Input',
      fieldName: 'hook_result',
      label: '钩子结果',
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'error_message',
      label: '请求错误消息',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['请求错误消息', 500])).optional(),
    },
    {
      component: 'Input',
      fieldName: 'tag',
      label: '标签',
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
      fieldName: 'platform',
      label: '外部平台',
    },
    {
      component: 'Input',
      fieldName: 'platform_endpoint',
      label: '平台端点',
    },
    {
      component: 'Input',
      fieldName: 'account',
      label: '账号',
    },
    {
      component: 'Input',
      fieldName: 'endpoint_path',
      label: '端点路径',
    },
    {
      component: 'Input',
      fieldName: 'method',
      label: '方法',
    },
    {
      component: 'Input',
      fieldName: 'payload',
      label: '请求参数',
    },
    {
      component: 'InputNumber',
      fieldName: 'status_code',
      label: '响应状态码',
    },
    {
      component: 'InputNumber',
      fieldName: 'response_time_ms',
      label: '响应耗时',
    },
    {
      component: 'Input',
      fieldName: 'response_body',
      label: '响应体',
    },
    {
      component: 'Input',
      fieldName: 'hook',
      label: '请求后钩子',
    },
    {
      component: 'Input',
      fieldName: 'hook_result',
      label: '钩子结果',
    },
    {
      component: 'Input',
      fieldName: 'error_message',
      label: '请求错误消息',
    },
    {
      component: 'Input',
      fieldName: 'tag',
      label: '标签',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<ExternalPlatformRequestLogApi.ExternalPlatformRequestLog>,
): VxeTableGridOptions<ExternalPlatformRequestLogApi.ExternalPlatformRequestLog>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'platform',
      title: '外部平台',
    },
    {
      field: 'platform_endpoint',
      title: '平台端点',
    },
    {
      field: 'account',
      title: '账号',
    },
    {
      field: 'endpoint_path',
      title: '端点路径',
    },
    {
      field: 'method',
      title: '方法',
    },
    {
      field: 'payload',
      title: '请求参数',
    },
    {
      field: 'status_code',
      title: '响应状态码',
    },
    {
      field: 'response_time_ms',
      title: '响应耗时',
    },
    {
      field: 'response_body',
      title: '响应体',
    },
    {
      field: 'hook',
      title: '请求后钩子',
    },
    {
      field: 'hook_result',
      title: '钩子结果',
    },
    {
      field: 'error_message',
      title: '请求错误消息',
    },
    {
      field: 'tag',
      title: '标签',
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
          nameTitle: $t('external_platform.request_log.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('external_platform:request_log:edit', 'edit'),
          op('external_platform:request_log:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
