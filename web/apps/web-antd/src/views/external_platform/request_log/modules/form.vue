<script lang="ts" setup>
import type { ExternalPlatformRequestLogApi } from '#/models/external_platform/request_log';

import { computed, ref } from 'vue';

import { useVbenModal } from '@vben/common-ui';

import { Button } from 'ant-design-vue';

import { useVbenForm } from '#/adapter/form';
import { $t } from '#/locales';
import { ExternalPlatformRequestLogModel } from '#/models/external_platform/request_log';

import { useSchema } from '../data';

const emit = defineEmits(['success']);

const formModel = new ExternalPlatformRequestLogModel();

const formData = ref<ExternalPlatformRequestLogApi.ExternalPlatformRequestLog>();
const getTitle = computed(() => {
  return formData.value?.id
    ? $t('ui.actionTitle.edit', [$t('external_platform.request_log.name')])
    : $t('ui.actionTitle.create', [$t('external_platform.request_log.name')]);
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
      const data = modalApi.getData<ExternalPlatformRequestLogApi.ExternalPlatformRequestLog>();
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
