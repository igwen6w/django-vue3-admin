<script lang="ts" setup>
import type { VxeTableGridOptions } from '#/adapter/vxe-table';

import { Page } from '@vben/common-ui';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { SystemLoginLogModel } from '#/models/system/login_log';

import { useColumns, useGridFormSchema } from './data';

const formModel = new SystemLoginLogModel();

const [Grid] = useVbenVxeGrid({
  formOptions: {
    schema: useGridFormSchema(),
    submitOnChange: true,
  },
  gridEvents: {},
  gridOptions: {
    columns: useColumns(),
    height: 'auto',
    keepSource: true,
    pagerConfig: {
      enabled: true,
    },
    proxyConfig: {
      ajax: {
        query: async ({ page }, formValues) => {
          const { create_time, ...rest } = formValues;
          const params = {
            page: page.currentPage,
            pageSize: page.pageSize,
            ...rest,
          };
          if (Array.isArray(create_time) && create_time.length === 2) {
            params.create_time_after = create_time[0];
            params.create_time_before = create_time[1];
          }
          return await formModel.list(params);
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
</script>

<template>
  <Page auto-content-height>
    <Grid table-title="系统访问记录" />
  </Page>
</template>
