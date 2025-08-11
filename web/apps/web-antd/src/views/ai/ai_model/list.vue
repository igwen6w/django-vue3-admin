<script lang="ts" setup>
import type {
  OnActionClickParams,
  VxeTableGridOptions,
} from '#/adapter/vxe-table';
import type { AiAIModelApi } from '#/models/ai/ai_model';

import { Page, useVbenModal } from '@vben/common-ui';
import { Plus } from '@vben/icons';

import { Button, message } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { $t } from '#/locales';
import { AiAIModelModel } from '#/models/ai/ai_model';

import { useColumns, useGridFormSchema } from './data';
import Form from './modules/form.vue';

const formModel = new AiAIModelModel();

const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,
  destroyOnClose: true,
});

/**
 * 编辑AI 模型
 */
function onEdit(row: AiAIModelApi.AiAIModel) {
  formModalApi.setData(row).open();
}

/**
 * 创建新AI 模型
 */
function onCreate() {
  formModalApi.setData(null).open();
}

/**
 * 删除AI 模型
 */
function onDelete(row: AiAIModelApi.AiAIModel) {
  const hideLoading = message.loading({
    content: '删除AI 模型',
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
}: OnActionClickParams<AiAIModelApi.AiAIModel>) {
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
  formOptions: {
    schema: useGridFormSchema(),
    submitOnChange: true,
  },
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
      search: true,
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
    <Grid table-title="AI 模型">
      <template #toolbar-tools>
        <Button
          type="primary"
          @click="onCreate"
          v-permission="'ai:ai_model:create'"
        >
          <Plus class="size-5" />
          {{ $t('ui.actionTitle.create') }}
        </Button>
      </template>
    </Grid>
  </Page>
</template>
