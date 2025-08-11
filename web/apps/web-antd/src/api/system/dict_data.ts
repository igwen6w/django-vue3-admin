import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace SystemDictDataApi {
  export interface SystemDictData {
    [key: string]: any;
    id: string;
    name: string;
  }
}

/**
 * 获取字典数据列表数据
 */
async function getDictDataList(params: Recordable<any>) {
  return requestClient.get<Array<SystemDictDataApi.SystemDictData>>(
    '/system/dict_data/',
    {
      params,
    },
  );
}

/**
 * 创建字典数据
 * @param data 字典数据数据
 */
async function createDictData(
  data: Omit<SystemDictDataApi.SystemDictData, 'id'>,
) {
  return requestClient.post('/system/dict_data/', data);
}

/**
 * 更新字典数据
 *
 * @param id 字典数据 ID
 * @param data 字典数据数据
 */
async function updateDictData(
  id: string,
  data: Omit<SystemDictDataApi.SystemDictData, 'id'>,
) {
  return requestClient.put(`/system/dict_data/${id}/`, data);
}

/**
 * 获取字典数据select用
 */
async function getDictDataSimple() {
  return requestClient.get(`/system/dict_data/simple/`);
}

/**
 * 更新字典数据
 *
 * @param id 字典数据 ID
 * @param data 字典数据数据
 */
async function patchDictData(
  id: string,
  data: Omit<SystemDictDataApi.SystemDictData, 'id'>,
) {
  return requestClient.patch(`/system/dict_data/${id}/`, data);
}

/**
 * 删除字典数据
 * @param id 字典数据 ID
 */
async function deleteDictData(id: string) {
  return requestClient.delete(`/system/dict_data/${id}/`);
}

export {
  createDictData,
  deleteDictData,
  getDictDataList,
  getDictDataSimple,
  patchDictData,
  updateDictData,
};
