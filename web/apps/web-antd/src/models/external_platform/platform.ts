import { BaseModel } from '#/models/base';

export namespace ExternalPlatformPlatformApi {
  export interface ExternalPlatformPlatform {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    name: string;
    sign: string;
    base_url: string;
    captcha_type: number;
    session_timeout_hours: number;
    retry_limit: number;
    is_active: boolean;
    description: string;
    login_condifg: string;
  }
}

export class ExternalPlatformPlatformModel extends BaseModel<ExternalPlatformPlatformApi.ExternalPlatformPlatform> {
  constructor() {
    super('/external_platform/platform/');
  }
}
