import { defineConfig } from '@vben/vite-config';

import { loadEnv } from 'vite';

import vitePluginOss from './plugins/vite-plugin-oss.mjs';

export default defineConfig(async ({ mode }) => {
  // eslint-disable-next-line n/prefer-global/process
  const env = loadEnv(mode, process.cwd());
  // 这样获取，提供默认值
  const backendUrl = env.VITE_BACKEND_URL || 'http://localhost:8000';
  const aiUrl = env.VITE_AI_URL || 'http://localhost:8010';

  // 判断是否为构建模式
  const isBuild = mode === 'production';
  const isOssEnabled = env.VITE_OSS_ENABLED === 'true';

  return {
    application: {},
    vite: {
      base: isBuild && isOssEnabled ? env.VITE_BASE_URL_PROD : '',
      server: {
        host: '0.0.0.0', // 保证 docker 内外都能访问
        port: 5678,
        proxy: {
          '/api/ai': {
            target: aiUrl,
            changeOrigin: true,
          },
          '/api/admin': {
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
