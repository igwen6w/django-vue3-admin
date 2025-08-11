import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace SystemDictTypeApi {
  export interface SystemDictType {
    [key: string]: any;
    id: string;
    name: string;
    type: string;
  }
}

/**
 * 获取字典类型列表数据
 */
async function getDictTypeList(params: Recordable<any>) {
  return requestClient.get<Array<SystemDictTypeApi.SystemDictType>>(
    '/system/dict_type/',
    {
      params,
    },
  );
}

/**
 * 创建字典类型
 * @param data 字典类型数据
 */
async function createDictType(
  data: Omit<SystemDictTypeApi.SystemDictType, 'id'>,
) {
  return requestClient.post('/system/dict_type/', data);
}

/**
 * 更新字典类型
 *
 * @param id 字典类型 ID
 * @param data 字典类型数据
 */
async function updateDictType(
  id: string,
  data: Omit<SystemDictTypeApi.SystemDictType, 'id'>,
) {
  return requestClient.put(`/system/dict_type/${id}/`, data);
}
/**
 * 更新字典类型
 *
 * @param id 字典类型 ID
 * @param data 字典类型数据
 */
async function patchDictType(
  id: string,
  data: Omit<SystemDictTypeApi.SystemDictType, 'id'>,
) {
  return requestClient.patch(`/system/dict_type/${id}/`, data);
}

/**
 * 删除字典类型
 * @param id 字典类型 ID
 */
async function deleteDictType(id: string) {
  return requestClient.delete(`/system/dict_type/${id}/`);
}

export {
  createDictType,
  deleteDictType,
  getDictTypeList,
  patchDictType,
  updateDictType,
};
