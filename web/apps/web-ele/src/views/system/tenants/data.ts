import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { SystemTenantsApi } from '#/api/system/tenants';

import { z } from '#/adapter/form';
import { $t } from '#/locales';

/**
 * 获取编辑表单的字段配置。如果没有使用多语言，可以直接export一个数组常量
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'name',
      label: $t('system.tenant.tenantName'),
      rules: z
        .string()
        .min(
          2,
          $t('ui.formRules.minLength', [$t('system.tenant.tenantName'), 2]),
        )
        .max(
          20,
          $t('ui.formRules.maxLength', [$t('system.tenant.tenantName'), 20]),
        ),
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
      component: 'Textarea',
      componentProps: {
        maxLength: 50,
        rows: 3,
        showCount: true,
      },
      fieldName: 'remark',
      label: $t('system.remark'),
      rules: z
        .string()
        .max(50, $t('ui.formRules.maxLength', [$t('system.remark'), 50]))
        .optional(),
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<SystemTenantsApi.SystemTenants>,
): VxeTableGridOptions<SystemTenantsApi.SystemTenants>['columns'] {
  return [
    {
      align: 'left',
      field: 'name',
      fixed: 'left',
      title: $t('system.tenant.tenantName'),
      treeNode: true,
      width: 150,
    },
    //  `contact_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '联系人',
    // `contact_mobile` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系手机',
    // `status` tinyint NOT NULL DEFAULT '0' COMMENT '租户状态（0正常 1停用）',
    // `website` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '绑定域名',
    // `package_id` bigint NOT NULL COMMENT '租户套餐编号',
    // `expire_time` datetime NOT NULL COMMENT '过期时间',
    // `account_count` int NOT NULL COMMENT '账号数量',
    {
      cellRender: { name: 'CellTag' },
      field: 'contact_name',
      title: $t('system.tenant.contact_mobile'),
      width: 100,
    },
    {
      cellRender: { name: 'CellTag' },
      field: 'website',
      title: $t('system.tenant.website'),
      width: 100,
    },
    {
      cellRender: { name: 'CellTag' },
      field: 'package_id',
      title: $t('system.tenant.package_id'),
      width: 100,
    },
    {
      cellRender: { name: 'CellTag' },
      field: 'expire_time',
      title: $t('system.tenant.expire_time'),
      width: 100,
    },
    {
      cellRender: { name: 'CellTag' },
      field: 'account_count',
      title: $t('system.tenant.account_count'),
      width: 100,
    },
    {
      cellRender: { name: 'CellTag' },
      field: 'status',
      title: $t('system.status'),
      width: 100,
    },
    {
      field: 'create_time',
      title: $t('system.createTime'),
      width: 180,
    },
    {
      field: 'remark',
      title: $t('system.remark'),
    },
    {
      align: 'right',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('system.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          'edit', // 默认的编辑按钮
          {
            code: 'delete', // 默认的删除按钮
            disabled: (row: SystemTenantsApi.SystemTenants) => {
              return !!(row.children && row.children.length > 0);
            },
          },
        ],
      },
      field: 'operation',
      fixed: 'right',
      headerAlign: 'center',
      showOverflow: false,
      title: $t('system.operation'),
      width: 200,
    },
  ];
}
