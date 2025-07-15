import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { SystemDictDataApi } from '#/api/system/dict_data';

import { z } from '#/adapter/form';
import { getDictTypeList } from '#/api/system/dict_type';
import { $t } from '#/locales';
import { format_datetime } from '#/utils/date';
import { op } from '#/utils/permission';

/**
 * 获取编辑表单的字段配置。如果没有使用多语言，可以直接export一个数组常量
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'ApiSelect',
      componentProps: {
        allowClear: true,
        api: getDictTypeList,
        class: 'w-full',
        resultField: 'items',
        labelField: 'name',
        valueField: 'id',
      },
      fieldName: 'dict_type',
      label: '字典类型',
      rules: z.any(),
    },
    {
      component: 'Input',
      fieldName: 'label',
      label: '字典标签',
      rules: z.string(),
    },
    {
      component: 'Input',
      fieldName: 'value',
      label: '字典键值',
      rules: z.string(),
    },
    {
      component: 'InputNumber',
      fieldName: 'sort',
      label: '字典排序',
      rules: z.number(),
    },
    {
      component: 'ApiSelect',
      fieldName: 'color_type',
      label: '颜色类型',
      componentProps: {
        name: 'CellTag',
        options: [
          {
            value: 'default',
            label: '默认',
          },
          {
            value: 'primary',
            label: '主要',
          },
          {
            value: 'success',
            label: '成功',
          },
          {
            value: 'info',
            label: '信息',
          },
          {
            value: 'warning',
            label: '警告',
          },
          {
            value: 'danger',
            label: '危险',
          },
        ],
      },
    },
    {
      component: 'Input',
      fieldName: 'css_class',
      label: 'CSS Class',
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
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<SystemDictDataApi.SystemDictData>,
): VxeTableGridOptions<SystemDictDataApi.SystemDictData>['columns'] {
  return [
    {
      align: 'left',
      field: 'id',
      fixed: 'left',
      title: 'id',
      treeNode: true,
      width: 150,
    },
    {
      field: 'label',
      title: '字典标签',
    },
    {
      field: 'value',
      title: '字典键值',
    },
    {
      field: 'sort',
      title: '字典排序',
    },
    {
      field: 'color_type',
      title: '颜色类型',
    },
    {
      field: 'css_class',
      title: 'CSS Class',
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
          nameTitle: $t('system.dict_data.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('system:dict_data:edit', 'edit'),
          op('system:dict_data:delete', 'delete'),
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
