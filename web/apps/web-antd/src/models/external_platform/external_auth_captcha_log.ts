import { BaseModel } from '#/models/base';

export namespace ExternalPlatformExternalAuthCaptchaLogApi {
  export interface ExternalPlatformExternalAuthCaptchaLog {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    request_log: number;
  }
}

export class ExternalPlatformExternalAuthCaptchaLogModel extends BaseModel<ExternalPlatformExternalAuthCaptchaLogApi.ExternalPlatformExternalAuthCaptchaLog> {
  constructor() {
    super('/external_platform/external_auth_captcha_log/');
  }
}
