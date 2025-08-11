import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace SystemTenantsApi {
  export interface SystemTenants {
    [key: string]: any;
    id: string;
    name: string;
  }
}

/**
 * 获取租户列表数据
 */
async function getTenantsList(params: Recordable<any>) {
  return requestClient.get<Array<SystemTenantsApi.SystemTenants>>(
    '/system/tenants/',
    {
    params,
  });
}

/**
 * 创建租户
 * @param data 租户数据
 */
async function createTenants(data: Omit<SystemTenantsApi.SystemTenants, 'id'>) {
  return requestClient.post('/system/tenants/', data);
}

/**
 * 更新租户
 *
 * @param id 租户 ID
 * @param data 租户数据
 */
async function updateTenants(
  id: string,
  data: Omit<SystemTenantsApi.SystemTenants, 'id'>,
) {
  return requestClient.put(`/system/tenants/${id}/`, data);
}
/**
 * 更新租户
 *
 * @param id 租户 ID
 * @param data 租户数据
 */
async function patchTenants(
  id: string,
  data: Omit<SystemTenantsApi.SystemTenants, 'id'>,
) {
  return requestClient.patch(`/system/tenants/${id}/`, data);
}

/**
 * 删除租户
 * @param id 租户 ID
 */
async function deleteTenants(id: string) {
  return requestClient.delete(`/system/tenants/${id}/`);
}

export {
  createTenants,
  deleteTenants,
  getTenantsList,
  patchTenants,
  updateTenants,
};
