import { BaseModel } from '#/models/base';

export namespace ExternalPlatformRequestLogApi {
  export interface ExternalPlatformRequestLog {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    platform: number;
    platform_endpoint: number;
    account: string;
    endpoint_path: string;
    method: string;
    payload: any;
    status_code: number;
    response_time_ms: number;
    response_body: any;
    hook: any;
    hook_result: any;
    error_message: string;
    tag: any;
  }
}

export class ExternalPlatformRequestLogModel extends BaseModel<ExternalPlatformRequestLogApi.ExternalPlatformRequestLog> {
  constructor() {
    super('/external_platform/request_log/');
  }
}
