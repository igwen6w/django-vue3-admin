import type { VxeTableGridOptions } from '@vben/plugins/vxe-table';

import type { VbenFormSchema } from '#/adapter/form';
import type { OnActionClickFn } from '#/adapter/vxe-table';
import type { SystemUserApi } from '#/models/system/user';

import { z } from '#/adapter/form';
import { getDeptList, getRoleList } from '#/api/system';
import { $t } from '#/locales';
import { SystemPostModel } from '#/models/system/post';
import { format_datetime } from '#/utils/date';

const systemPost = new SystemPostModel();

/**
 * 获取编辑表单的字段配置
 */
export function useSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'username',
      label: '用户名',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['用户名']))
        .max(100, $t('ui.formRules.maxLength', ['用户名', 100])),
    },
    {
      component: 'Input',
      fieldName: 'email',
      label: '电子邮件地址',
      rules: z
        .string()
        .min(1, $t('ui.formRules.required', ['电子邮件地址']))
        .max(100, $t('ui.formRules.maxLength', ['电子邮件地址', 100])),
    },
    {
      component: 'ApiTreeSelect',
      componentProps: {
        allowClear: true,
        multiple: true, // 允许多选
        api: getDeptList,
        class: 'w-full',
        resultField: 'items',
        labelField: 'name',
        valueField: 'id',
        childrenField: 'children',
      },
      fieldName: 'dept',
      label: $t('system.dept.name'),
    },
    {
      component: 'ApiSelect',
      componentProps: {
        allowClear: true,
        multiple: true, // 允许多选
        mode: 'multiple', // 允许多选
        api: getRoleList,
        class: 'w-full',
        resultField: 'items',
        labelField: 'name',
        valueField: 'id',
      },
      fieldName: 'role',
      label: $t('system.role.name'),
    },
    {
      component: 'ApiSelect',
      componentProps: {
        allowClear: true,
        multiple: true, // 允许多选
        mode: 'multiple', // 允许多选
        api: () => systemPost.list(),
        class: 'w-full',
        resultField: 'items',
        labelField: 'name',
        valueField: 'id',
        childrenField: 'children',
      },
      fieldName: 'post',
      label: $t('system.post.name'),
    },
    {
      component: 'Input',
      fieldName: 'mobile',
      label: '手机号',
    },
    {
      component: 'Input',
      fieldName: 'nickname',
      label: '昵称',
    },
    {
      component: 'InputPassword',
      fieldName: 'password',
      label: '密码',
    },
    {
      component: 'Input',
      fieldName: 'city',
      label: '城市',
    },
    {
      component: 'Input',
      fieldName: 'province',
      label: '省份',
    },
    {
      component: 'Input',
      fieldName: 'country',
      label: '国家',
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
      label: $t('system.status'),
    },
    {
      component: 'Input',
      fieldName: 'remark',
      label: $t('system.remark'),
    },
  ];
}

/**
 * 获取表格列配置
 * @description 使用函数的形式返回列数据而不是直接export一个Array常量，是为了响应语言切换时重新翻译表头
 * @param onActionClick 表格操作按钮点击事件
 */

export function useColumns(
  onActionClick?: OnActionClickFn<SystemUserApi.SystemUser>,
): VxeTableGridOptions<SystemUserApi.SystemUser>['columns'] {
  return [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'username',
      title: '用户名',
      width: 100,
    },

    {
      field: 'is_superuser',
      title: '超级用户状态',
    },
    {
      field: 'date_joined',
      title: '加入日期',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      field: 'mobile',
      title: 'mobile',
    },
    {
      cellRender: {
        name: 'CellTag',
      },
      field: 'status',
      title: $t('system.status'),
      width: 100,
    },
    {
      field: 'login_ip',
      title: 'login ip',
      width: 150,
    },
    {
      field: 'last_login',
      title: '最后登录',
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      field: 'remark',
      title: $t('system.remark'),
    },
    {
      field: 'creator',
      title: $t('system.creator'),
      width: 80,
    },
    {
      field: 'modifier',
      title: $t('system.modifier'),
      width: 80,
    },
    {
      field: 'update_time',
      title: $t('system.updateTime'),
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      field: 'create_time',
      title: $t('system.createTime'),
      width: 150,
      formatter: ({ cellValue }) => format_datetime(cellValue),
    },
    {
      align: 'center',
      cellRender: {
        attrs: {
          nameField: 'name',
          nameTitle: $t('system.user.name'),
          onClick: onActionClick,
        },
        name: 'CellOperation',
        options: ['edit', 'delete'],
      },
      field: 'action',
      fixed: 'right',
      title: '操作',
      width: 120,
    },
  ];
}
