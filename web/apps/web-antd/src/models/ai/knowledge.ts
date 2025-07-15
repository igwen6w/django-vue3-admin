import { BaseModel } from '#/models/base';

export namespace AiKnowledgeApi {
  export interface AiKnowledge {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    name: string;
    description: string;
    embedding_model_id: number;
    embedding_model: string;
    top_k: number;
    similarity_threshold: any;
    status: number;
  }
}

export class AiKnowledgeModel extends BaseModel<AiKnowledgeApi.AiKnowledge> {
  constructor() {
    super('/ai/knowledge/');
  }
}
