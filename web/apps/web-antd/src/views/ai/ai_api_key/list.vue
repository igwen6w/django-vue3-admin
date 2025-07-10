<script lang="ts" setup>
import type {
  OnActionClickParams,
  VxeTableGridOptions,
} from '#/adapter/vxe-table';
import type { AiAIApiKeyApi } from '#/models/ai/ai_api_key';

import { Page, useVbenModal } from '@vben/common-ui';
import { Plus } from '@vben/icons';

import { Button, message } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { $t } from '#/locales';
import { AiAIApiKeyModel } from '#/models/ai/ai_api_key';

import { useColumns, useGridFormSchema } from './data';
import Form from './modules/form.vue';

const formModel = new AiAIApiKeyModel();

const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,
  destroyOnClose: true,
});

/**
 * 编辑AI API 密钥
 */
function onEdit(row: AiAIApiKeyApi.AiAIApiKey) {
  formModalApi.setData(row).open();
}

/**
 * 创建新AI API 密钥
 */
function onCreate() {
  formModalApi.setData(null).open();
}

/**
 * 删除AI API 密钥
 */
function onDelete(row: AiAIApiKeyApi.AiAIApiKey) {
  const hideLoading = message.loading({
    content: '删除AI API 密钥',
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
}: OnActionClickParams<AiAIApiKeyApi.AiAIApiKey>) {
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
    <Grid table-title="AI API 密钥">
      <template #toolbar-tools>
        <Button
          type="primary"
          @click="onCreate"
          v-permission="'ai:ai_api_key:create'"
        >
          <Plus class="size-5" />
          {{ $t('ui.actionTitle.create', [$t('ai.ai_api_key.name')]) }}
        </Button>
      </template>
    </Grid>
  </Page>
</template>
