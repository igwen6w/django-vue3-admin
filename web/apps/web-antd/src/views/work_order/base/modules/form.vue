<script lang="ts" setup>
import type { WorkOrderBaseApi } from '#/models/work_order/base';

import { computed, ref } from 'vue';

import { useVbenModal } from '@vben/common-ui';

import { Button } from 'ant-design-vue';

import { useVbenForm } from '#/adapter/form';
import { $t } from '#/locales';
import { WorkOrderBaseModel } from '#/models/work_order/base';

import { useSchema } from '../data';

const emit = defineEmits(['success']);

const formModel = new WorkOrderBaseModel();

const formData = ref<WorkOrderBaseApi.WorkOrderBase>();
const getTitle = computed(() => {
  return formData.value?.id
    ? $t('ui.actionTitle.edit', [$t('work_order.base.name')])
    : $t('ui.actionTitle.create', [$t('work_order.base.name')]);
});

const [Form, formApi] = useVbenForm({
  layout: 'horizontal',
  schema: useSchema(),
  showDefaultActions: false,
});

function resetForm() {
  formApi.resetForm();
  formApi.setValues(formData.value || {});
}

const [Modal, modalApi] = useVbenModal({
  async onConfirm() {
    const { valid } = await formApi.validate();
    if (valid) {
      modalApi.lock();
      const data = await formApi.getValues();
      try {
        await (formData.value?.id
          ? formModel.update(formData.value.id, data)
          : formModel.create(data));
        await modalApi.close();
        emit('success');
      } finally {
        modalApi.lock(false);
      }
    }
  },
  onOpenChange(isOpen) {
    if (isOpen) {
      const data = modalApi.getData<WorkOrderBaseApi.WorkOrderBase>();
      if (data) {
        formData.value = data;
        formApi.setValues(formData.value);
      }
    }
  },
});
</script>

<template>
  <Modal :title="getTitle">
    <Form />
    <template #prepend-footer>
      <div class="flex-auto">
        <Button type="primary" danger @click="resetForm">
          {{ $t('common.reset') }}
        </Button>
      </div>
    </template>
  </Modal>
</template>
<style lang="css" scoped></style>
