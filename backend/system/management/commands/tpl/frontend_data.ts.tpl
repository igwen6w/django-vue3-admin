import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { ${app_name_camel}${model_name}Api } from '#/models/${app_name}/${model_name_snake}';

import { z } from '#/adapter/form';
import { $$t } from '#/locales';
import { format_datetime } from '#/utils/date';
import { op } from '#/utils/permission';

/**
 * 获取编辑表单的字段配置
 */
export function useSchema(): VbenFormSchema[] {
  return [
${form_fields}
  ];
}

/**
 * 获取编辑表单的字段配置
 */
export function useGridFormSchema(): VbenFormSchema[] {
  return [
${form_fields}
  ];
}


/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */
export function useColumns(
  onActionClick?: OnActionClickFn<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}>,
): VxeTableGridOptions<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}>['columns'] {
  return [
${columns}
    {
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $$t('${app_name}.${model_name_snake}.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: [
          op('${app_name}:${model_name_snake}:edit', 'edit'),
          op('${app_name}:${model_name_snake}:delete', 'delete'),
        ],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
