import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace SystemTenantPackageApi {
  export interface SystemTenantPackage {
    [key: string]: any;
    id: string;
    name: string;
  }
}

/**
 * 获取租户列表数据
 */
async function getTenantPackageList(params: Recordable<any>) {
  return requestClient.get<Array<SystemTenantPackageApi.SystemTenantPackage>>(
    '/system/tenant_package/',
    {
      params,
    },
  );
}

/**
 * 创建租户
 * @param data 租户数据
 */
async function createTenantPackage(
  data: Omit<SystemTenantPackageApi.SystemTenantPackage, 'id'>,
) {
  return requestClient.post('/system/tenant_package/', data);
}

/**
 * 更新租户
 *
 * @param id 租户 ID
 * @param data 租户数据
 */
async function updateTenantPackage(
  id: string,
  data: Omit<SystemTenantPackageApi.SystemTenantPackage, 'id'>,
) {
  return requestClient.put(`/system/tenant_package/${id}/`, data);
}
/**
 * 更新租户
 *
 * @param id 租户 ID
 * @param data 租户数据
 */
async function patchTenantPackage(
  id: string,
  data: Omit<SystemTenantPackageApi.SystemTenantPackage, 'id'>,
) {
  return requestClient.patch(`/system/tenant_package/${id}/`, data);
}

/**
 * 删除租户
 * @param id 租户 ID
 */
async function deleteTenantPackage(id: string) {
  return requestClient.delete(`/system/tenant_package/${id}/`);
}

export {
  createTenantPackage,
  deleteTenantPackage,
  getTenantPackageList,
  patchTenantPackage,
  updateTenantPackage,
};
