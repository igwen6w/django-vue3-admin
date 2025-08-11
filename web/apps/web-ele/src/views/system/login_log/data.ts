import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { SystemLoginLogApi } from '#/models/system/login_log';

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
      fieldName: 'username',
      label: 'username',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['username']))
        .max(100, $t('ui.formRules.maxLength', ['username', 100])),
    },
    {
      component: 'InputNumber',
      fieldName: 'result',
      label: 'result',
    },
    {
      component: 'Input',
      fieldName: 'user_ip',
      label: 'user ip',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['user ip']))
        .max(100, $t('ui.formRules.maxLength', ['user ip', 100])),
    },
    {
      component: 'Input',
      fieldName: 'user_agent',
      label: 'user agent',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['user agent']))
        .max(100, $t('ui.formRules.maxLength', ['user agent', 100])),
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: 'remark',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['remark']))
        .max(100, $t('ui.formRules.maxLength', ['remark', 100])),
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 */
export function useColumns(): VxeTableGridOptions<SystemLoginLogApi.SystemLoginLog>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'username',
      title: '用户名',
    },
    {
      cellRender: {
        name: 'CellTag',
      },
      field: 'result_text',
      title: '登录结果',
    },
    {
      field: 'user_ip',
      title: '登录地址',
    },
    {
      field: 'user_agent',
      title: '浏览器',
    },
    {
      field: 'create_time',
      title: $t('system.createTime'),
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
  ];
}
