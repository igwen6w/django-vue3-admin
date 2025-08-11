import { BaseModel } from '#/models/base';

export namespace AiAIModelApi {
  export interface AiAIModel {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    name: string;
    sort: number;
    status: number;
    key: number;
    platform: string;
    model: string;
    temperature: any;
    max_tokens: number;
    max_contexts: number;
  }
}

export class AiAIModelModel extends BaseModel<AiAIModelApi.AiAIModel> {
  constructor() {
    super('/ai/ai_model/');
  }
}
