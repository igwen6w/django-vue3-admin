import { BaseModel } from '#/models/base';

export namespace SystemLoginLogApi {
  export interface SystemLoginLog {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    username: string;
    result: number;
    user_ip: string;
    user_agent: string;
  }
}

export class SystemLoginLogModel extends BaseModel<SystemLoginLogApi.SystemLoginLog> {
  constructor() {
    super('/system/login_log/');
  }
}
