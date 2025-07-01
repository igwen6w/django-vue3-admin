import { request } from '#/utils/request';

export namespace ${model_name}Api {
  export interface ${model_name} {
    id: number;
    name: string;
    create_time: string;
    update_time: string;
    // 根据实际字段添加
  }

  export interface ${model_name}ListParams {
    page?: number;
    pageSize?: number;
    name?: string;
    // 根据实际字段添加
  }

  export interface ${model_name}ListResult {
    total: number;
    items: ${model_name}[];
  }
}

/**
 * 获取${verbose_name}列表
 */
export function get${model_name}List(params: ${model_name}Api.${model_name}ListParams) {
  return request<${model_name}Api.${model_name}ListResult>({
    url: '/$app_name/${model_name_lower}/',
    method: 'GET',
    params,
  });
}

/**
 * 获取${verbose_name}详情
 */
export function get${model_name}Detail(id: number) {
  return request<${model_name}Api.${model_name}>({
    url: `/$app_name/${model_name_lower}/${id}/`,
    method: 'GET',
  });
}

/**
 * 创建${verbose_name}
 */
export function create${model_name}(data: Partial<${model_name}Api.${model_name}>) {
  return request<${model_name}Api.${model_name}>({
    url: '/$app_name/${model_name_lower}/',
    method: 'POST',
    data,
  });
}

/**
 * 更新${verbose_name}
 */
export function update${model_name}(id: number, data: Partial<${model_name}Api.${model_name}>) {
  return request<${model_name}Api.${model_name}>({
    url: `/$app_name/${model_name_lower}/${id}/`,
    method: 'PUT',
    data,
  });
}

/**
 * 删除${verbose_name}
 */
export function delete${model_name}(id: number) {
  return request({
    url: `/$app_name/${model_name_lower}/${id}/`,
    method: 'DELETE',
  });
} 