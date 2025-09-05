import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ExternalPlatformPlatformEndpointApi } from '#/models/external_platform/platform_endpoint';

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
      fieldName: 'endpoint_type',
      label: '端点类型',
      rules: z.string().min(1, $t('ui.formRules.required', ['端点类型'])).max(100, $t('ui.formRules.maxLength', ['端点类型', 100])),
    },
    {
      component: 'Input',
      fieldName: 'name',
      label: '端点名称',
      rules: z.string().min(1, $t('ui.formRules.required', ['端点名称'])).max(100, $t('ui.formRules.maxLength', ['端点名称', 100])),
    },
    {
      component: 'Input',
      fieldName: 'path',
      label: '路径',
      rules: z.string().min(1, $t('ui.formRules.required', ['路径'])).max(100, $t('ui.formRules.maxLength', ['路径', 100])),
    },
    {
      component: 'Input',
      fieldName: 'http_method',
      label: '请求方式',
      rules: z.string().min(1, $t('ui.formRules.required', ['请求方式'])).max(100, $t('ui.formRules.maxLength', ['请求方式', 100])),
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
      fieldName: 'require_auth',
      label: '是否需要鉴权',
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'description',
      label: '端点说明',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['端点说明', 500])).optional(),
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
      fieldName: 'endpoint_type',
      label: '端点类型',
    },
    {
      component: 'Input',
      fieldName: 'name',
      label: '端点名称',
    },
    {
      component: 'Input',
      fieldName: 'path',
      label: '路径',
    },
    {
      component: 'Input',
      fieldName: 'http_method',
      label: '请求方式',
    },
    {
      component: 'Input',
      fieldName: 'require_auth',
      label: '是否需要鉴权',
    },
    {
      component: 'Input',
      fieldName: 'description',
      label: '端点说明',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<ExternalPlatformPlatformEndpointApi.ExternalPlatformPlatformEndpoint>,
): VxeTableGridOptions<ExternalPlatformPlatformEndpointApi.ExternalPlatformPlatformEndpoint>['columns'] {
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
      field: 'endpoint_type',
      title: '端点类型',
    },
    {
      field: 'name',
      title: '端点名称',
    },
    {
      field: 'path',
      title: '路径',
    },
    {
      field: 'http_method',
      title: '请求方式',
    },
    {
      field: 'require_auth',
      title: '是否需要鉴权',
    },
    {
      field: 'description',
      title: '端点说明',
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
          nameTitle: $t('external_platform.platform_endpoint.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('external_platform:platform_endpoint:edit', 'edit'),
          op('external_platform:platform_endpoint:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
