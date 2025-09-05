<script lang="ts" setup>
import type { ExternalPlatformAuthSessionApi } from '#/models/external_platform/auth_session';

import { computed, ref } from 'vue';

import { useVbenModal } from '@vben/common-ui';

import { Button } from 'ant-design-vue';

import { useVbenForm } from '#/adapter/form';
import { $t } from '#/locales';
import { ExternalPlatformAuthSessionModel } from '#/models/external_platform/auth_session';

import { useSchema } from '../data';

const emit = defineEmits(['success']);

const formModel = new ExternalPlatformAuthSessionModel();

const formData = ref<ExternalPlatformAuthSessionApi.ExternalPlatformAuthSession>();
const getTitle = computed(() => {
  return formData.value?.id
    ? $t('ui.actionTitle.edit', [$t('external_platform.auth_session.name')])
    : $t('ui.actionTitle.create', [$t('external_platform.auth_session.name')]);
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
      const data = modalApi.getData<ExternalPlatformAuthSessionApi.ExternalPlatformAuthSession>();
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
