<script setup lang="ts">
import { computed, nextTick, ref } from 'vue';

import { Page } from '@vben/common-ui';

import {
  Button,
  Col,
  Input,
  InputSearch,
  List,
  ListItemMeta,
  Row,
  Select,
} from 'ant-design-vue';

import { fetchAIStream } from '#/api/ai/chat';

interface Message {
  id: number;
  role: 'ai' | 'user';
  content: string;
}

interface ChatItem {
  id: number;
  title: string;
  lastMessage: string;
}

// mock 历史对话
const chatList = ref<ChatItem[]>([]);

// mock 聊天消息
const messages = ref<Message[]>([]);

// mock 模型列表
const modelOptions = [
  { label: 'deepseek', value: 'deepseek' },
  { label: 'GPT-4', value: 'gpt-4' },
];

const selectedChatId = ref<null | number>(chatList.value[0]?.id ?? null);
const selectedModel = ref(modelOptions[0]?.value);
const search = ref('');
const input = ref('');
const messagesRef = ref<HTMLElement | null>(null);
const currentAiMessage = ref<Message | null>(null);
const isAiTyping = ref(false);

const filteredChats = computed(() => {
  if (!search.value) return chatList.value;
  return chatList.value.filter((chat) => chat.title.includes(search.value));
});

// 直接用conversationId过滤
const currentMessages = computed(() => {
  if (!selectedChatId.value) return [];
  return [];
  // return messages.value.filter(
  //   (msg) => msg.conversationId === selectedChatId.value,
  // );
});

function selectChat(id: number) {
  selectedChatId.value = id;
  nextTick(scrollToBottom);
}

function handleNewChat() {
  const newId = Date.now();
  chatList.value.unshift({
    id: newId,
    title: `新对话${chatList.value.length + 1}`,
    lastMessage: '',
  });
  selectedChatId.value = newId;
  nextTick(scrollToBottom);
}

async function handleSend() {
  console.log(111);
  const msg: Message = {
    id: Date.now(),
    role: 'user',
    content: input.value,
  };
  messages.value.push(msg);

  // 预留AI消息
  const aiMsgObj: Message = {
    id: Date.now() + 1,
    role: 'ai',
    content: '',
  };
  messages.value.push(aiMsgObj);
  currentAiMessage.value = aiMsgObj;
  isAiTyping.value = true;

  const stream = await fetchAIStream({
    content: input.value,
    conversation_id: selectedChatId.value, // 新增
  });

  for await (const chunk of stream) {
    for (const char of chunk) {
      aiMsgObj.content += char;
      // 保证messages数组响应式更新
      const idx = messages.value.indexOf(aiMsgObj);
      if (idx !== -1) {
        messages.value.splice(idx, 1, { ...aiMsgObj });
      }
      currentAiMessage.value = { ...aiMsgObj };
      await nextTick();
      scrollToBottom();
      await new Promise((resolve) => setTimeout(resolve, 15));
    }
  }
  isAiTyping.value = false;
  input.value = '';
  nextTick(scrollToBottom);
}

function scrollToBottom() {
  if (messagesRef.value && messagesRef.value.scrollHeight !== undefined) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
  }
}
</script>

<template>
  <Page auto-content-height>
    <Row style="height: 100%">
      <!-- 左侧历史对话 -->
      <Col :span="6" class="chat-sider">
        <div class="sider-header">
          <Button type="primary" @click="handleNewChat">新建对话</Button>
          <Input
            v-model:value="search"
            placeholder="搜索历史对话"
            allow-clear
            style="margin: 12px 0 8px 0"
          />
        </div>
        <List style="flex: 1; overflow-y: auto; padding-bottom: 12px">
          <template #default>
            <ListItemMeta
              v-for="item in filteredChats"
              :key="item.id"
              class="chat-list-item"
              :class="[{ selected: item.id === selectedChatId }]"
              @click="selectChat(item.id)"
            >
              <ListItemMeta>
                <template #title>
                  <span class="chat-title" :title="item.title">{{
                    item.title
                  }}</span>
                </template>
                <template #description>
                  <span class="chat-desc">{{ item.lastMessage }}</span>
                </template>
              </ListItemMeta>
            </ListItemMeta>
          </template>
        </List>
      </Col>
      <!-- 右侧聊天区 -->
      <Col :span="18" class="chat-content">
        <div class="content-header">
          <div class="model-select-wrap">
            <Select
              v-model:value="selectedModel"
              style="width: 220px"
              :options="modelOptions"
              placeholder="选择AI模型"
            />
          </div>
        </div>
        <div class="chat-messages" ref="messagesRef">
          <div
            v-for="msg in currentMessages"
            :key="msg.id"
            class="chat-message"
            :class="[msg.role]"
          >
            <div class="bubble" :class="[msg.role]">
              <span class="role">{{ msg.role === 'user' ? '我' : 'AI' }}</span>
              <span class="bubble-content">
                {{ msg.content }}
                <span
                  v-if="
                    msg.role === 'ai' && isAiTyping && msg === currentAiMessage
                  "
                  class="typing-cursor"
                ></span>
              </span>
            </div>
          </div>
        </div>
        <div class="chat-input-wrap">
          <InputSearch
            v-model:value="input"
            enter-button="发送"
            @search="handleSend"
            placeholder="请输入内容..."
          />
        </div>
      </Col>
    </Row>
  </Page>
</template>

<style scoped lang="css">
.chat-sider {
  background: #fafbfc;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #eee;
  padding: 16px 8px 8px 8px;
}
.sider-header {
  margin-bottom: 8px;
}
.chat-list-item {
  border-radius: 6px;
  margin-bottom: 4px;
  transition:
    box-shadow 0.2s,
    background 0.2s;
  cursor: pointer;
}
.chat-list-item.selected {
  background: #e6f7ff;
  box-shadow: 0 2px 8px #1677ff22;
  border: 1.5px solid #1677ff;
}
.chat-list-item:hover {
  background: #f0f5ff;
  box-shadow: 0 2px 8px #1677ff11;
}
.chat-title {
  font-weight: 500;
  font-size: 15px;
  max-width: 140px;
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chat-desc {
  color: #888;
  font-size: 12px;
  max-width: 140px;
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chat-content {
  display: flex;
  flex-direction: column;
  padding: 16px 24px 8px 24px;
  background: #f6f8fa;
}
.content-header {
  margin-bottom: 12px;
  display: flex;
  justify-content: flex-end;
}
.model-select-wrap {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  background: #fff;
  border-radius: 8px;
  padding: 24px 16px 80px 16px;
  margin-bottom: 0;
  min-height: 300px;
  box-shadow: 0 2px 8px #0001;
  transition: box-shadow 0.2s;
  scrollbar-width: thin;
  scrollbar-color: #d6dee1 #f6f8fa;
}
.chat-messages::-webkit-scrollbar {
  width: 6px;
}
.chat-messages::-webkit-scrollbar-thumb {
  background: #d6dee1;
  border-radius: 4px;
}
.chat-messages::-webkit-scrollbar-track {
  background: #f6f8fa;
}
.chat-message {
  display: flex;
  margin-bottom: 16px;
}
.chat-message.user {
  justify-content: flex-end;
}
.chat-message.ai {
  justify-content: flex-start;
}
.bubble {
  max-width: 70%;
  padding: 10px 16px;
  border-radius: 18px;
  font-size: 15px;
  line-height: 1.7;
  box-shadow: 0 1px 4px #0001;
  display: flex;
  align-items: center;
  word-break: break-all;
}
.bubble.user {
  background: linear-gradient(90deg, #1677ff 0%, #69b1ff 100%);
  color: #fff;
  border-bottom-right-radius: 4px;
}
.bubble.ai {
  background: #f0f5ff;
  color: #333;
  border-bottom-left-radius: 4px;
}
.role {
  font-weight: bold;
  margin-right: 8px;
  font-size: 13px;
  opacity: 0.7;
}
.bubble-content {
  flex: 1;
}
.chat-input-wrap {
  position: absolute;
  left: 24%;
  right: 24px;
  bottom: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px #0001;
  padding: 12px 16px 8px 16px;
  z-index: 10;
}
@media (max-width: 1200px) {
  .chat-input-wrap {
    left: 6%;
    right: 6px;
  }
  .chat-content {
    padding: 8px 4px 8px 4px;
  }
}
.typing-cursor {
  display: inline-block;
  width: 8px;
  height: 1.2em;
  background: #1677ff;
  margin-left: 2px;
  animation: blink-cursor 1s steps(1) infinite;
  vertical-align: bottom;
  border-radius: 2px;
}
@keyframes blink-cursor {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
}
</style>
