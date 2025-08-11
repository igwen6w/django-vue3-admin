import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { SystemDictTypeApi } from '#/api/system/dict_type';

import { z } from '#/adapter/form';
import { $t } from '#/locales';
import { format_datetime } from '#/utils/date';
import { op } from '#/utils/permission';

/**
 * 获取编辑表单的字段配置。如果没有使用多语言，可以直接export一个数组常量
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'name',
      label: '字典名称',
      rules: z
        .string()
        .min(2, $t('ui.formRules.minLength', [$t('system.dict_type.name'), 2]))
        .max(
          20,
          $t('ui.formRules.maxLength', [$t('system.dict_type.name'), 20]),
        ),
    },
    {
      component: 'Input',
      fieldName: 'value',
      label: '字典类型',
      rules: z
        .string()
        .min(2, $t('ui.formRules.minLength', [$t('system.dict_type.value'), 2]))
        .max(
          20,
          $t('ui.formRules.maxLength', [$t('system.dict_type.value'), 20]),
        ),
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
      fieldName: 'status',
      label: '状态',
    },
    {
      component: 'Input',
      componentProps: {
        maxLength: 50,
        rows: 3,
        showCount: true,
      },
      fieldName: 'remark',
      label: '备注',
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
  onActionClick?: OnActionClickFn<SystemDictTypeApi.SystemDictType>,
): VxeTableGridOptions<SystemDictTypeApi.SystemDictType>['columns'] {
  return [
    {
      align: 'left',
      field: 'id',
      fixed: 'left',
      title: '字典编号',
      treeNode: true,
      width: 150,
    },
    {
      field: 'name',
      title: '字典名称',
    },
    {
      field: 'value',
      title: '字典类型',
      width: 180,
    },
    {
      cellRender: {
        name: 'CellTag',
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
          nameTitle: $t('system.dict_type.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('system:dict_type:edit', 'edit'),
          {
            code: 'view', // 新增查看详情按钮（可自定义code）
            text: '数据', // 按钮文本（国际化）
          },
          op('system:dict_type:delete', 'delete'),
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

export function useGridFormSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'name',
      label: '字典名称',
      componentProps: { allowClear: true },
    },
    {
      component: 'Input',
      fieldName: 'value',
      label: '字典类型',
      componentProps: { allowClear: true },
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
  ];
}
