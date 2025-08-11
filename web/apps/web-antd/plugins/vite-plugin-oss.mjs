import fs from 'node:fs';
import path from 'node:path';

import OSS from 'ali-oss';

export default function vitePluginOss(options = {}) {
  const {
    enabled = false,
    region,
    accessKeyId,
    accessKeySecret,
    bucket,
    prefix = '',
    deleteLocal = false,
  } = options;

  if (!enabled) {
    return {
      name: 'vite-plugin-oss',
      apply: 'build',
      closeBundle() {
        console.log('OSS upload disabled');
      },
    };
  }

  return {
    name: 'vite-plugin-oss',
    apply: 'build',
    async closeBundle() {
      console.log('Starting OSS upload...');

      const client = new OSS({
        region,
        accessKeyId,
        accessKeySecret,
        bucket,
      });

      const distPath = path.resolve(process.cwd(), 'dist');

      if (!fs.existsSync(distPath)) {
        console.error('Dist folder not found');
        return;
      }

      try {
        await uploadDirectory(client, distPath, prefix);
        console.log('OSS upload completed successfully');

        if (deleteLocal) {
          fs.rmSync(distPath, { recursive: true, force: true });
          console.log('Local dist folder deleted');
        }
      } catch (error) {
        console.error('OSS upload failed:', error);
      }
    },
  };
}

async function uploadDirectory(client, localPath, prefix) {
  const files = fs.readdirSync(localPath);

  for (const file of files) {
    const localFilePath = path.join(localPath, file);
    const stats = fs.statSync(localFilePath);

    if (stats.isDirectory()) {
      await uploadDirectory(client, localFilePath, `${prefix}${file}/`);
    } else {
      const ossKey = `${prefix}${file}`;
      await client.put(ossKey, localFilePath);
      console.log(`Uploaded: ${ossKey}`);
    }
  }
}
