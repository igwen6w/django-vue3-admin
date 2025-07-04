import { defineConfig } from '@vben/vite-config';
import { loadEnv } from 'vite';
import * as console from "node:console";

export default defineConfig(async ({ mode }) => {
  // eslint-disable-next-line n/prefer-global/process
  const env = loadEnv(mode, process.cwd());
  // 这样获取
  const backendUrl = env.VITE_BACKEND_URL;
  console.log(backendUrl)
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
    },
  };
});
