import { fetchWithAuth } from '#/utils/fetch-with-auth';

export interface CreateImageTaskParams {
  prompt: string;
  style?: string;
  size?: string;
  model?: string;
  platform?: string;
  n?: number;
}

export async function createImageTask(params: CreateImageTaskParams) {
  const res = await fetchWithAuth('drawing/', {
    method: 'POST',
    body: JSON.stringify(params),
  });
  if (!res.ok) {
    throw new Error('创建图片任务失败');
  }
  return await res.json();
}

export async function fetchImageTaskStatus(id: number) {
  const res = await fetchWithAuth(`drawing/${id}/`);
  if (!res.ok) {
    throw new Error('查询图片任务状态失败');
  }
  return await res.json();
}

export interface GetImagePageParams {
  page?: number;
  page_size?: number;
}

export async function getImagePage(params: GetImagePageParams = {}) {
  const query = new URLSearchParams();
  if (params.page) query.append('page', String(params.page));
  if (params.page_size) query.append('page_size', String(params.page_size));
  const res = await fetchWithAuth(
    `drawing${query.toString() ? `?${query.toString()}` : ''}`,
  );
  if (!res.ok) {
    throw new Error('获取图片分页失败');
  }
  return await res.json();
}
