import { BaseModel } from '#/models/base';

export namespace SystemPostApi {
  export interface SystemPost {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    code: string;
    name: string;
    sort: number;
    status: number;
  }
}

export class SystemPostModel extends BaseModel<SystemPostApi.SystemPost> {
  constructor() {
    super('/system/post/');
  }
}
