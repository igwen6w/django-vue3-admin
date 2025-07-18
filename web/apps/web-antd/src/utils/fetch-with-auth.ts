import { formatToken } from '#/utils/auth';
import { useAccessStore } from '@vben/stores';

export function fetchWithAuth(input: RequestInfo, init: RequestInit = {}) {
  const accessStore = useAccessStore();
  const token = accessStore.accessToken;
  const headers = new Headers(init.headers || {});
  headers.append('Content-Type', 'application/json');
  headers.append('Authorization', formatToken(token) as string);
  return fetch(input, { ...init, headers });
}
