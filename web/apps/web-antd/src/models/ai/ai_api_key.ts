import { BaseModel } from '#/models/base';

export namespace AiAIApiKeyApi {
  export interface AiAIApiKey {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    name: string;
    platform: string;
    model_type: string;
    api_key: string;
    url: string;
    status: number;
  }
}

export class AiAIApiKeyModel extends BaseModel<AiAIApiKeyApi.AiAIApiKey> {
  constructor() {
    super('/ai/api_key/');
  }
}
