import * as console from 'node:console';

import { defineConfig } from '@vben/vite-config';

import { loadEnv } from 'vite';

import vitePluginOss from './plugins/vite-plugin-oss.mjs';

export default defineConfig(async ({ mode }) => {
  // eslint-disable-next-line n/prefer-global/process
  const env = loadEnv(mode, process.cwd());
  // 这样获取
  const backendUrl = env.VITE_BACKEND_URL;
  console.log(backendUrl);
  return {
    application: {},
    vite: {
      server: {
        host: '0.0.0.0', // 保证 docker 内外都能访问
        port: 5678,
        proxy: {
          '/api': {
            target: backendUrl,
            changeOrigin: true,
          },
        },
      },
      plugins: [
        vitePluginOss({
          enabled: env.VITE_OSS_ENABLED === 'true',
          region: env.VITE_OSS_REGION,
          accessKeyId: env.VITE_OSS_ACCESS_KEY_ID,
          accessKeySecret: env.VITE_OSS_ACCESS_KEY_SECRET,
          bucket: env.VITE_OSS_BUCKET,
          prefix: env.VITE_OSS_PREFIX || '',
          deleteLocal: env.VITE_OSS_DELETE_LOCAL === 'true',
        }),
      ],
    },
  };
});
