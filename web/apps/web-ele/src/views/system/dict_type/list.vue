<script lang="ts" setup>
import type {
  OnActionClickParams,
  VxeTableGridOptions,
} from '#/adapter/vxe-table';
import type { SystemDictTypeApi } from '#/api/system/dict_type';

import { useRouter } from 'vue-router';

import { Page, useVbenModal } from '@vben/common-ui';
import { Plus } from '@vben/icons';

import { Button, message } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { deleteDictType, getDictTypeList } from '#/api/system/dict_type';
import { $t } from '#/locales';

import { useColumns } from './data';
import Form from './modules/form.vue';

const router = useRouter();
const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,
  destroyOnClose: true,
});

/**
 * 编辑字典
 * @param row
 */
function onEdit(row: SystemDictTypeApi.SystemDictType) {
  if (row.menu_ids) {
    row.menu_ids = row.menu_ids.split(',').map(Number);
  }
  formModalApi.setData(row).open();
}

/**
 * 创建新字典
 */
function onCreate() {
  formModalApi.setData(null).open();
}

/**
 * 删除字典
 * @param row
 */
function onDelete(row: SystemDictTypeApi.SystemDictType) {
  const hideLoading = message.loading({
    content: $t('ui.actionMessage.deleting', [row.name]),
    duration: 0,
    key: 'action_process_msg',
  });
  deleteDictType(row.id)
    .then(() => {
      message.success({
        content: $t('ui.actionMessage.deleteSuccess', [row.name]),
        key: 'action_process_msg',
      });
      refreshGrid();
    })
    .catch(() => {
      hideLoading();
    });
}
const handleViewDetail = (row: SystemDictTypeApi.SystemDictType) => {
  router.push({
    path: '/system/dict_data/', // 目标页面路径
    query: { dict_type: row.id }, // 传递查询参数
  });
};
/**
 * 表格操作按钮的回调函数
 */
function onActionClick({
  code,
  row,
}: OnActionClickParams<SystemDictTypeApi.SystemDictType>) {
  switch (code) {
    case 'delete': {
      onDelete(row);
      break;
    }
    case 'edit': {
      onEdit(row);
      break;
    }
    case 'view': {
      handleViewDetail(row);
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
          return await getDictTypeList({
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
    treeConfig: {
      parentField: 'pid',
      rowField: 'id',
      transform: false,
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
    <Grid table-title="字典列表">
      <template #toolbar-tools>
        <Button type="primary" @click="onCreate">
          <Plus class="size-5" />
          {{ $t('ui.actionTitle.create', [$t('system.dict_type.name')]) }}
        </Button>
      </template>
    </Grid>
  </Page>
</template>
