<script lang="ts" setup>
import { nextTick, onMounted, ref, watch } from 'vue';

interface Message {
  type: 'ai' | 'system' | 'user' | string;
  content: string;
  isTyping?: boolean;
}

const input = ref<string>('');
const messages = ref<Message[]>([]);
const loading = ref<boolean>(false);
const isConnected = ref<boolean>(false);
let socket: null | WebSocket = null;
const messagesRef = ref<HTMLElement | null>(null);

onMounted(() => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  const wsUrl = `${protocol}//${host}/ws/chat/`;

  socket = new WebSocket(wsUrl);

  socket.addEventListener('open', () => {
    isConnected.value = true;
    messages.value.push({ type: 'system', content: '✅ WebSocket 连接成功' });
  });

  socket.addEventListener('message', (event: MessageEvent<string>) => {
    const data = JSON.parse(event.data);

    if (data.done) {
      loading.value = false;
      if (
        messages.value.length > 0 &&
        messages.value[messages.value.length - 1]?.type === 'ai'
      ) {
        const lastMsg = messages.value[messages.value.length - 1];
        if (lastMsg) {
          lastMsg.isTyping = false;
        }
      }
    } else if (data.is_streaming) {
      if (
        messages.value.length > 0 &&
        messages.value[messages.value.length - 1]?.type === 'ai'
      ) {
        const currentMessage = messages.value[messages.value.length - 1];
        if (currentMessage) {
          currentMessage.content += data.message;
          currentMessage.isTyping = true;
        }
      } else {
        messages.value.push({
          type: 'ai',
          content: data.message,
          isTyping: true,
        });
      }
    } else {
      const messageType = data.type || 'system';
      messages.value.push({ type: messageType, content: data.message });
    }
  });

  socket.addEventListener('close', (event: CloseEvent) => {
    isConnected.value = false;
    messages.value.push({
      type: 'system',
      content: `❌ WebSocket 连接已断开 (${event.code})`,
    });
  });

  socket.addEventListener('error', () => {
    isConnected.value = false;
    messages.value.push({ type: 'system', content: '❌ WebSocket 连接错误' });
  });
});

// 自动滚动到底
watch(
  messages,
  () => {
    nextTick(() => {
      if (messagesRef.value) {
        messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
      }
    });
  },
  { deep: true },
);

function send(): void {
  if (!input.value.trim()) return;
  if (socket && socket.readyState === WebSocket.OPEN) {
    loading.value = true;
    messages.value.push({ type: 'user', content: input.value });
    socket.send(JSON.stringify({ message: input.value }));
    input.value = '';
  } else {
    messages.value.push({
      type: 'system',
      content: '❌ WebSocket 未连接，无法发送消息',
    });
  }
}
</script>

<template>
  <div class="chat-box">
    <div class="messages" ref="messagesRef">
      <div class="message" v-for="(msg, index) in messages" :key="index">
        <span v-if="msg.type === 'user'" class="user-message"
          >🧑: {{ msg.content }}</span
        >
        <span v-else-if="msg.type === 'ai'" class="ai-message"
          >🤖: {{ msg.content }}</span
        >
      </div>
      <div v-if="loading" class="loading">AI 正在思考...</div>
    </div>
    <div class="input-box">
      <input v-model="input" @keyup.enter="send" placeholder="请输入问题..." />
      <button @click="send">发送</button>
    </div>
  </div>
</template>

<style scoped>
.chat-box {
  display: flex;
  flex-direction: column;
  height: 80vh;
  width: 400px;
  border: 1px solid #ddd;
}

.connection-status {
  padding: 8px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.history-controls {
  display: flex;
  gap: 4px;
}

.history-btn {
  padding: 2px 6px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 10px;
}

.history-btn:hover {
  background-color: #5a6268;
}

.status-connected {
  color: #28a745;
  font-weight: bold;
}

.status-connecting {
  color: #ffc107;
  font-weight: bold;
}

.status-disconnected {
  color: #dc3545;
  font-weight: bold;
}

.status-disconnecting {
  color: #6c757d;
  font-weight: bold;
}

.status-unknown {
  color: #6c757d;
  font-weight: bold;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.message {
  margin: 4px 0;
  word-wrap: break-word;
}

.user-message {
  color: #007bff;
  font-weight: bold;
}

.ai-message {
  color: #28a745;
}

.typing-text {
  display: inline;
}

.typing-cursor {
  color: #28a745;
  animation: blink 1s infinite;
  font-weight: bold;
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
}

.system-message {
  color: #6c757d;
  font-style: italic;
}

.history-message {
  color: #17a2b8;
  font-style: italic;
  white-space: pre-line;
}

.loading {
  color: gray;
  font-style: italic;
}

.input-box {
  display: flex;
  padding: 8px;
  border-top: 1px solid #ddd;
}

input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 8px;
}

input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>
