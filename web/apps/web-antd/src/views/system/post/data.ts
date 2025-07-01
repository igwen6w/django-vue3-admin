import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { SystemPostApi } from '#/models/system/post';

import { z } from '#/adapter/form';
import { $t } from '#/locales';
import { format_datetime } from '#/utils/date';

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
      component: 'Input',
      fieldName: 'code',
      label: '编码',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['编码']))
        .max(100, $t('ui.formRules.maxLength', ['编码', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'sort',
      label: '排序',
      rules: z.number(),
    },
    {
      component: 'RadioGroup',
      componentProps: {
        buttonStyle: 'solid',
        options: [
          { label: '开启', value: true },
          { label: '关闭', value: false },
        ],
        optionType: 'button',
      },
      defaultValue: true,
      fieldName: 'status',
      label: '是否启用',
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: '备注',
    },
  ];
}

export function useColumns(
  onActionClick?: OnActionClickFn<SystemPostApi.SystemPost>,
): VxeTableGridOptions<SystemPostApi.SystemPost>['columns'] {
  return [
    {
      field: 'id',
      title: 'id',
    },
    {
      field: 'name',
      title: '岗位名称',
    },
    {
      field: 'code',
      title: '岗位编码',
    },
    {
      cellRender: {
        name: 'CellTag',
        options: [
          { label: $t('common.enabled'), value: true },
          { label: $t('common.disabled'), value: false },
        ],
      },
      field: 'status',
      title: '状态',
      width: 100,
    },
    {
      field: 'remark',
      title: '备注',
    },
    {
      field: 'create_time',
      title: '创建时间',
      width: 180,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      align: 'right',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('system.{model_name_snake}.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          'edit', // 默认的编辑按钮
          {
            code: 'delete', // 默认的删除按钮
          },
        ],
      },
      field: 'operation',
      fixed: 'right',
      headerAlign: 'center',
      showOverflow: false,
      title: '操作',
      width: 200,
    },
  ];
}
