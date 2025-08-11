<script lang="ts" setup>
import type { SystemDictDataApi } from '#/api/system/dict_data';

import { computed, ref } from 'vue';
import { useRoute } from "vue-router";

import { useVbenModal } from '@vben/common-ui';

import { Button } from 'ant-design-vue';

import { useVbenForm } from '#/adapter/form';
import { createDictData, updateDictData } from '#/api/system/dict_data';
import { $t } from '#/locales';

import { useSchema } from '../data';

const emit = defineEmits(['success']);
const formData = ref<SystemDictDataApi.SystemDictData>();
const getTitle = computed(() => {
  return formData.value?.id
    ? $t('ui.actionTitle.edit', [$t('system.dict_data.name')])
    : $t('ui.actionTitle.create', [$t('system.dict_data.name')]);
});
const route = useRoute();
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
      const { dict_type } = route.query;
      data.dict_type = dict_type;
      try {
        await (formData.value?.id
          ? updateDictData(formData.value.id, data)
          : createDictData(data));
        await modalApi.close();
        emit('success');
      } finally {
        modalApi.lock(false);
      }
    }
  },
  onOpenChange(isOpen) {
    if (isOpen) {
      const data = modalApi.getData<SystemDictDataApi.SystemDictData>();
      if (data) {
        if (data.pid === 0) {
          data.pid = undefined;
        }
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
