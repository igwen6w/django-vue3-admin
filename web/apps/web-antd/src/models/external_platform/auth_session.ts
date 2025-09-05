import { BaseModel } from '#/models/base';

export namespace ExternalPlatformAuthSessionApi {
  export interface ExternalPlatformAuthSession {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    platform: number;
    account: string;
    auth: any;
    status: string;
    expire_time: string;
    login_time: string;
  }
}

export class ExternalPlatformAuthSessionModel extends BaseModel<ExternalPlatformAuthSessionApi.ExternalPlatformAuthSession> {
  constructor() {
    super('/external_platform/auth_session/');
  }
}
