import { BaseModel } from '#/models/base';

export namespace AiChatMessageApi {
  export interface AiChatMessage {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    conversation_id: number;
    user: number;
    role: number;
    model: string;
    model_id: number;
    type: string;
    reply_id: number;
    content: string;
    use_context: boolean;
    segment_ids: string;
  }
}

export class AiChatMessageModel extends BaseModel<AiChatMessageApi.AiChatMessage> {
  constructor() {
    super('/ai/chat_message/');
  }
}
