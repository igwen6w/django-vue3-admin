import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ExternalPlatformPlatformConfigApi } from '#/models/external_platform/platform_config';

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
      fieldName: 'config_key',
      label: '配置键',
      rules: z.string().min(1, $t('ui.formRules.required', ['配置键'])).max(100, $t('ui.formRules.maxLength', ['配置键', 100])),
    },
    {
      component: 'Input',
      fieldName: 'config_value',
      label: '配置值',
    },
    {
      component: 'Input',
      componentProps: { rows: 3, showCount: true },
      fieldName: 'description',
      label: '配置说明',
      rules: z.string().max(500, $t('ui.formRules.maxLength', ['配置说明', 500])).optional(),
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
      fieldName: 'config_key',
      label: '配置键',
    },
    {
      component: 'Input',
      fieldName: 'config_value',
      label: '配置值',
    },
    {
      component: 'Input',
      fieldName: 'description',
      label: '配置说明',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<ExternalPlatformPlatformConfigApi.ExternalPlatformPlatformConfig>,
): VxeTableGridOptions<ExternalPlatformPlatformConfigApi.ExternalPlatformPlatformConfig>['columns'] {
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
      field: 'config_key',
      title: '配置键',
    },
    {
      field: 'config_value',
      title: '配置值',
    },
    {
      field: 'description',
      title: '配置说明',
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
          nameTitle: $t('external_platform.platform_config.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('external_platform:platform_config:edit', 'edit'),
          op('external_platform:platform_config:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
