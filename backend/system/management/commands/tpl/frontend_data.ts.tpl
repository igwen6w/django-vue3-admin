import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ${app_name_camel}${model_name}Api } from '#/models/$app_name/${model_name_snake}';

import { z } from '#/adapter/form';
import { $$t } from '#/locales';
import { format_datetime } from '#/utils/date';

/**
 * 获取编辑表单的字段配置
 */
export function useSchema(): VbenFormSchema[] {
  return [
$form_fields
  ];
}

export function useColumns(
  onActionClick?: OnActionClickFn<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}>,
): VxeTableGridOptions<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}>['columns'] {
  return [
    {
      align: 'left',
      field: 'id',
    },
    {
      cellRender: {
        name: 'CellTag',
        options: [
          { label: $$t('common.enabled'), value: true },
          { label: $$t('common.disabled'), value: false },
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
          nameTitle: $$t('${app_name}.{model_name_snake}.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          'edit', // 默认的编辑按钮
          {
            code: 'view', // 新增查看详情按钮（可自定义code）
            text: '数据', // 按钮文本（国际化）
          },
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
