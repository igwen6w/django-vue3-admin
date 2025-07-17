import { useAccessStore } from '@vben/stores';

import { formatToken } from '#/utils/auth';

export interface FetchAIStreamParams {
  content: string;
}

export async function fetchAIStream({ content }: FetchAIStreamParams) {
  const accessStore = useAccessStore();
  const token = accessStore.accessToken;
  const headers = new Headers();

  headers.append('Content-Type', 'application/json');
  headers.append('Authorization', <string>formatToken(token));

  const response = await fetch('/chat/api/v1/stream', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      content,
    }),
  });

  if (!response.body) throw new Error('No stream body');

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf8');
  let buffer = '';

  return {
    async *[Symbol.asyncIterator]() {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split('\n\n');
        buffer = parts.pop() || '';
        for (const part of parts) {
          if (part.startsWith('data: ')) {
            yield part.replace('data: ', '');
          }
        }
      }
    },
  };
}
