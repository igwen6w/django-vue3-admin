<script lang="ts" setup>
import type {
  OnActionClickParams,
  VxeTableGridOptions,
} from '#/adapter/vxe-table';
import type { ${app_name_camel}${model_name}Api } from '#/models/$app_name/${model_name_snake}';

import { Page, useVbenModal } from '@vben/common-ui';
import { Plus } from '@vben/icons';

import { Button, message } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { $$t } from '#/locales';
import { ${app_name_camel}${model_name}Model } from '#/models/${app_name}/${model_name_snake}';

import { useColumns } from './data';
import Form from './modules/form.vue';

const formModel = new ${app_name_camel}${model_name}Model();

const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,
  destroyOnClose: true,
});

/**
 * 编辑${verbose_name}
 */
function onEdit(row: ${app_name_camel}${model_name}Api.${app_name_camel}${model_name}) {
  formModalApi.setData(row).open();
}

/**
 * 创建新${verbose_name}
 */
function onCreate() {
  formModalApi.setData(null).open();
}

/**
 * 删除${verbose_name}
 */
function onDelete(row: ${app_name_camel}${model_name}Api.${app_name_camel}${model_name}) {
  const hideLoading = message.loading({
    content: '删除${verbose_name}',
    duration: 0,
    key: 'action_process_msg',
  });
  formModel
    .delete(row.id)
    .then(() => {
      message.success({
        content: '删除成功',
        key: 'action_process_msg',
      });
      refreshGrid();
    })
    .catch(() => {
      hideLoading();
    });
}

/**
 * 表格操作按钮的回调函数
 */
function onActionClick({
  code,
  row,
}: OnActionClickParams<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}>) {
  switch (code) {
    case 'delete': {
      onDelete(row);
      break;
    }
    case 'edit': {
      onEdit(row);
      break;
    }
  }
}

const [Grid, gridApi] = useVbenVxeGrid({
  gridEvents: {},
  gridOptions: {
    columns: useColumns(onActionClick),
    height: 'auto',
    keepSource: true,
    pagerConfig: {
      enabled: true,
    },
    proxyConfig: {
      ajax: {
        query: async ({ page }, formValues) => {
          return await formModel.list({
            page: page.currentPage,
            pageSize: page.pageSize,
            ...formValues,
          });
        },
      },
    },
    toolbarConfig: {
      custom: true,
      export: false,
      refresh: { code: 'query' },
      zoom: true,
    },
  } as VxeTableGridOptions,
});

/**
 * 刷新表格
 */
function refreshGrid() {
  gridApi.query();
}
</script>

<template>
  <Page auto-content-height>
    <FormModal @success="refreshGrid" />
    <Grid table-title="${verbose_name}">
      <template #toolbar-tools>
        <Button type="primary" @click="onCreate">
          <Plus class="size-5" />
            {{ $$t('ui.actionTitle.create', [$$t('${app_name}.${model_name_snake}.name')]) }}
        </Button>
      </template>
    </Grid>
  </Page>
</template>
