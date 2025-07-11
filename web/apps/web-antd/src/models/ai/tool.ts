import { BaseModel } from '#/models/base';

export namespace AiToolApi {
  export interface AiTool {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    name: string;
    description: string;
    status: number;
  }
}

export class AiToolModel extends BaseModel<AiToolApi.AiTool> {
  constructor() {
    super('/ai/tool/');
  }
}
