<script setup lang="ts">
import { computed, h, reactive, ref } from 'vue';

import { Page } from '@vben/common-ui';

import {
  Button,
  Card,
  Col,
  Form,
  Input,
  message,
  Pagination,
  Row,
  Select,
} from 'ant-design-vue';

import { createImageTask } from '#/api/ai/drawing';

// 表单选项
const platforms = [
  { label: '通义千问', value: 'tongyi' },
  // { label: 'DeepSeek', value: 'deepseek' },
  // { label: 'OpenAI', value: 'openai' },
  // { label: 'Google GenAI', value: 'google-genai' },
];
const models = {
  tongyi: [{ label: 'wanx_v1', value: 'wanx_v1' }],
  // deepseek: [{ label: 'deepseek-img', value: 'deepseek-img' }],
  // openai: [{ label: 'dall-e-3', value: 'dall-e-3' }],
  // 'google-genai': [{ label: 'imagen', value: 'imagen' }],
};
const sizes = [
  { label: '1024x1024', value: '1024x1024' },
  { label: '720*1280', value: '720*1280' },
  { label: '768*1152', value: '768*1152' },
  { label: '1280*720', value: '1280*720' },
];
const styles = [
  { label: '默认（由模型随机输出风格）', value: 'auto' },
  { label: '摄影', value: 'photography' },
  { label: '人像写真', value: 'portrait' },
  { label: '3D卡通', value: '3d cartoon' },
  { label: '动画', value: 'anime' },
  { label: '油画', value: 'oil painting' },
  { label: '水彩', value: 'watercolor' },
  { label: '素描', value: 'sketch' },
  { label: '中国画', value: 'chinese painting' },
  { label: '扁平插画', value: 'flat illustration' },
];

// 表单数据
const form = reactive({
  prompt: '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。',
  platform: 'tongyi',
  model: 'wanx_v1',
  size: '1024x1024',
  style: 'watercolor',
});

// 图片数据与分页
const images = ref<string[]>([]);
const loading = ref(false);
const page = ref(1);
const pageSize = 12;
const total = computed(() => images.value.length);
const pagedImages = computed(() =>
  images.value.slice((page.value - 1) * pageSize, page.value * pageSize),
);

// 平台切换时自动切换模型
const onPlatformChange = (val: string) => {
  form.model = models[val][0].value;
};

// 提交表单，调用AI画图API
async function handleDraw() {
  loading.value = true;
  try {
    // 这里调用你的AI画图API，返回图片url数组
    const res = await createImageTask(form);
    // images.value = res.data.images;
    // DEMO用假数据
    // images.value = Array.from(
    //   { length: 30 },
    //   (_, i) => `https://picsum.photos/seed/${form.prompt}-${i}/300/300`,
    // );
    page.value = 1;
    message.success('生成成功');
  } catch {
    message.error('生成失败');
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <Page auto-content-height>
    <Row :gutter="24">
      <!-- 左侧表单 -->
      <Col :span="8">
        <Card title="AI画图" bordered>
          <Form layout="vertical" @submit.prevent="handleDraw">
            <Form.Item label="画画描述">
              <Input.TextArea
                v-model:value="form.prompt"
                :autosize="true"
                placeholder="请输入画面描述"
              />
            </Form.Item>
            <Form.Item label="平台选择">
              <Select v-model:value="form.platform" @change="onPlatformChange">
                <Select.Option
                  v-for="item in platforms"
                  :key="item.value"
                  :value="item.value"
                >
                  {{ item.label }}
                </Select.Option>
              </Select>
            </Form.Item>
            <Form.Item label="模型选择">
              <Select v-model:value="form.model">
                <Select.Option
                  v-for="item in models[form.platform]"
                  :key="item.value"
                  :value="item.value"
                >
                  {{ item.label }}
                </Select.Option>
              </Select>
            </Form.Item>
            <Form.Item label="图片尺寸">
              <Select v-model:value="form.size">
                <Select.Option
                  v-for="item in sizes"
                  :key="item.value"
                  :value="item.value"
                >
                  {{ item.label }}
                </Select.Option>
              </Select>
            </Form.Item>
            <Form.Item label="图像风格">
              <Select v-model:value="form.style">
                <Select.Option
                  v-for="item in styles"
                  :key="item.value"
                  :value="item.value"
                >
                  {{ item.label }}
                </Select.Option>
              </Select>
            </Form.Item>
            <Form.Item>
              <Button type="primary" html-type="submit" :loading="loading">
                生成图片
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </Col>
      <!-- 右侧图片展示 -->
      <Col :span="16">
        <Card title="生成结果" bordered>
          <Row :gutter="16">
            <Col
              v-for="(img, idx) in pagedImages"
              :key="img"
              :span="4"
              style="margin-bottom: 16px"
            >
              <Card
                hoverable
                :cover="
                  h('img', {
                    src: img,
                    style: 'width:100%;height:180px;object-fit:cover;',
                  })
                "
              />
            </Col>
          </Row>
          <Pagination
            v-if="total > pageSize"
            v-model:current="page"
            :total="total"
            :page-size="pageSize"
            style="margin-top: 16px; text-align: right"
          />
        </Card>
      </Col>
    </Row>
  </Page>
</template>

<style scoped>
/* 可根据需要自定义样式 */
</style>
