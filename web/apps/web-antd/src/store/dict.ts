// src/store/dict.ts
import { defineStore } from 'pinia';

import { getDictDataSimple } from '#/api/system/dict_data'; // 根据实际路径调整

export const useDictStore = defineStore('dict', {
  state: () => ({
    dictData: [] as any[],
  }),
  actions: {
    async fetchDictData() {
      this.dictData = await getDictDataSimple(); // 根据接口返回结构调整
    },
    getOptionsByType(type: string) {
      return this.dictData.filter((item) => item.dict_type === type);
    },
  },
});
