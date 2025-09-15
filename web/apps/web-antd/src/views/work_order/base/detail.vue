<template>
  <div class="container">
    <div class="left">
      <!-- <a-menu
    v-model:openKeys="openKeys"
    v-model:selectedKeys="selectedKeys"
    style="width: 100px;height: 100px;color: red;"
    mode="vertical"
    :items="items"
    @click="handleClick"
  /> -->
      <Button style="margin-top: 20px" type="primary">查看工单</Button>
    </div>
    <div class="center">
      <Card class="mb-4" title="查看工单">
        <div class="card">
          <div class="content">
            <div
              class="contentList"
              v-for="(item, index) in contentArray"
              :key="index"
              :style="[item.widthFlag == 1 ? 'min-width: 100%' : '']"
            >
              <div class="title">{{ item.title }}</div>
              <div class="contentView">
                <div class="contentText">{{ item.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
    <div class="right">
      <Card class="mb-4" title="">
        <div class="mt-2 flex flex-col gap-2">
        <VbenCheckButtonGroup
          v-model="radioValue"
          :options="options"
          v-bind="compProps"
        />
      </div>
        <Card class="mb-4" title=""></Card>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h, onMounted, ref,reactive } from 'vue';
import type { MenuProps } from 'ant-design-vue';
import { Button } from 'ant-design-vue';
import { login } from '#/api/work_order';
import { useRoute } from 'vue-router';
import { Card } from 'ant-design-vue';
import type { Recordable } from '@vben/types';
import {
  Page,
  VbenButton,
  VbenButtonGroup,
  VbenCheckButtonGroup,
} from '@vben/common-ui';
import { watch } from 'fs';

let radioValue = ref('a') as any

function resetValues() {
  radioValue.value = undefined;
//   checkValue.value = [];
}

const options = [
  { label: '处置', value: 'a' },
  { label: '下派', value: 'b'},
];

const compProps = reactive({
  beforeChange: undefined,
  disabled: false,
  gap: 0,
  showIcon: true,
  size: 'middle',
  allowClear: false,
} as Recordable<any>);

watch(radioValue, (newVal, oldVal) => {
  console.log(newVal, oldVal);
})


let detailModel = ref({}) as any;
const route = useRoute();
let contentArray = ref([
  {
    key: 'external_roll_number',
    title: '工单编号',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_handle_rel_expire_time',
    title: '处置实际到期时间',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_src_way',
    title: '受理方式',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_payroll_name',
    title: '姓名',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_company_tel',
    title: '联系方式',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_addr',
    title: '地址',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_region_district_id',
    title: '区域',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_note14',
    title: '是否回访',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_distribute_way',
    title: '企业名称',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_payroll_type',
    title: '业务类别',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_event_type2_id',
    title: '事件类型',
    content: '',
    widthFlag: 1,
  },
  {
    key: 'external_roll_content',
    title: '事件描述',
    content: '',
    widthFlag: 1,
  },
  {
    key: 'external_note',
    title: '备注',
    content: '',
    widthFlag: 1,
  },
  {
    key: 'external_product_ids',
    title: '三级复核',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_addr2',
    title: '区县复核',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_company_address',
    title: '满意研判',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_order_number',
    title: '解决研判',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_normal_payroll_title',
    title: '复核原因',
    content: '',
    widthFlag: 1,
  },
  {
    key: 'external_addr3',
    title: '满意复核',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_note1',
    title: '解决复核',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_note15',
    title: '市复核意见',
    content: '',
    widthFlag: 1,
  },
  {
    key: 'external_attachments',
    title: '附件',
    content: '',
    widthFlag: 1,
  },
  {
    key: 'external_note4',
    title: '是否考核',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_handling_quality',
    title: '办理满意',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_note12',
    title: '过程满意',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_note2',
    title: '是否解决',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_note3',
    title: '办理回复',
    content: '',
    widthFlag: 4,
  },
  {
    key: 'external_note16',
    title: '自主研判',
    content: '',
    widthFlag: 1,
  },
  {
    key: 'external_note17',
    title: '研判原因',
    content: '',
    widthFlag: 1,
  },
]);
const handleClick: MenuProps['onClick'] = (menuInfo) => {
  console.log('click ', menuInfo);
};
onMounted(async () => {
  const res = await login({
    id: route.params.id,
  });
  if (res.length > 0) {
    detailModel.value = res[0];
    contentArray.value.forEach((item) => {
      item.content = detailModel.value[item.key];
    });
  }

  //   console.log(JSON.stringify(res));
});
// 可在此处添加逻辑
</script>

<style scoped>
@media (min-width: 1400px) {
  .container {
    max-width: 2400px;
  }
}
.container {
  display: flex;
  height: 100vh;
  /* background: #fff; */
}
.left {
  width: 100px;
  /* background: #f5f5f5;
  border-right: 1px solid #eee;
  padding: 16px 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center; */
}
.center,
.right {
  flex: 1;
  padding: 16px;
  box-sizing: border-box;
  min-width: 0;
}
.center {
  border-right: 1px solid #eee;
  overflow-y: auto;
  padding: 24px;
  /* background: #f0f2f5; */
  min-height: 100vh;
}
.card {
  /* background: #fafbfc; */
  border-radius: 6px;
  /* box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04); */
  /* padding: 24px; */
  margin: 0 auto;
  .head {
    display: flex;
    justify-content: space-between;
    .title {
      font-size: 20px;
      font-weight: 600;
      /* color: #333; */
      margin-bottom: 16px;
    }
  }
  .content {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    .contentList {
      /* flex: 0 0 calc(50% - 8px); */
      display: flex;
      width: 200px;
      .title {
        /* flex: 0 0 40%; */
        /* color: #333; */
        text-align: right;
        width: 70px;
        margin-right: 10px;
      }
      .contentView {
        flex: 1;
        /* border-bottom: 1px solid #d9d9d9; */
        .contentText {
          word-break: break-word;
          /* color: #333; */
          border-bottom: 1px solid #d9d9d9;
          min-height: 20px;
        }
      }
    }
  }
}
</style>
