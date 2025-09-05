import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ExternalPlatformAuthSessionApi } from '#/models/external_platform/auth_session';

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
      fieldName: 'account',
      label: '账号',
      rules: z.string().min(1, $t('ui.formRules.required', ['账号'])).max(100, $t('ui.formRules.maxLength', ['账号', 100])),
    },
    {
      component: 'Input',
      fieldName: 'auth',
      label: '鉴权信息',
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
      fieldName: 'expire_time',
      label: '过期时间',
    },
    {
      component: 'Input',
      fieldName: 'login_time',
      label: '登录时间',
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
      fieldName: 'account',
      label: '账号',
    },
    {
      component: 'Input',
      fieldName: 'auth',
      label: '鉴权信息',
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
      fieldName: 'expire_time',
      label: '过期时间',
    },
    {
      component: 'Input',
      fieldName: 'login_time',
      label: '登录时间',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<ExternalPlatformAuthSessionApi.ExternalPlatformAuthSession>,
): VxeTableGridOptions<ExternalPlatformAuthSessionApi.ExternalPlatformAuthSession>['columns'] {
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
      field: 'account',
      title: '账号',
    },
    {
      field: 'auth',
      title: '鉴权信息',
    },
    {
      field: 'status',
      title: '状态',
      cellRender: { name: 'CellTag' },
    },
    {
      field: 'expire_time',
      title: '过期时间',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      field: 'login_time',
      title: '登录时间',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
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
          nameTitle: $t('external_platform.auth_session.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('external_platform:auth_session:edit', 'edit'),
          op('external_platform:auth_session:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
