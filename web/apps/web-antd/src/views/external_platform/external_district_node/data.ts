import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ExternalPlatformExternalDistrictNodeApi } from '#/models/external_platform/external_district_node';

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
      rules: z.string().min(1, $t('ui.formRules.required', ['名称'])).max(100, $t('ui.formRules.maxLength', ['名称', 100])),
    },
    {
      component: 'Input',
      fieldName: 'code',
      label: '编码',
      rules: z.string().min(1, $t('ui.formRules.required', ['编码'])).max(100, $t('ui.formRules.maxLength', ['编码', 100])),
    },
    {
      component: 'Input',
      fieldName: 'parent',
      label: '父节点',
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
      fieldName: 'code',
      label: '编码',
    },
    {
      component: 'Input',
      fieldName: 'parent',
      label: '父节点',
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<ExternalPlatformExternalDistrictNodeApi.ExternalPlatformExternalDistrictNode>,
): VxeTableGridOptions<ExternalPlatformExternalDistrictNodeApi.ExternalPlatformExternalDistrictNode>['columns'] {
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
      field: 'code',
      title: '编码',
    },
    {
      field: 'parent',
      title: '父节点',
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
          nameTitle: $t('external_platform.external_district_node.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('external_platform:external_district_node:edit', 'edit'),
          op('external_platform:external_district_node:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
