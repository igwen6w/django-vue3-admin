<script lang="ts" setup>
import type { ${app_name_camel}${model_name}Api } from '#/models/$app_name/${model_name_snake}';

import { computed, ref } from 'vue';

import { useVbenModal } from '@vben/common-ui';

import { Button } from 'ant-design-vue';

import { useVbenForm } from '#/adapter/form';
import { $$t } from '#/locales';
import { ${app_name_camel}${model_name}Model } from '#/models/${app_name}/${model_name_snake}';

import { useSchema } from '../data';

const emit = defineEmits(['success']);

const formModel = new ${app_name_camel}${model_name}Model();

const formData = ref<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}>();
const getTitle = computed(() => {
  return formData.value?.id
    ? $$t('ui.actionTitle.edit', [$$t('${app_name}.${model_name_snake}.name')])
    : $$t('ui.actionTitle.create', [$$t('${app_name}.${model_name_snake}.name')]);
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
      const data = modalApi.getData<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}>();
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
          {{ $$t('common.reset') }}
        </Button>
      </div>
    </template>
  </Modal>
</template>
<style lang="css" scoped></style>
