import { BaseModel } from '#/models/base';

export namespace AiChatConversationApi {
  export interface AiChatConversation {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    title: string;
    pinned: boolean;
    pinned_time: string;
    user: number;
    role: number;
    model_id: number;
    model: string;
    system_message: string;
    temperature: any;
    max_tokens: number;
    max_contexts: number;
  }
}

export class AiChatConversationModel extends BaseModel<AiChatConversationApi.AiChatConversation> {
  constructor() {
    super('/ai/chat_conversation/');
  }
}
