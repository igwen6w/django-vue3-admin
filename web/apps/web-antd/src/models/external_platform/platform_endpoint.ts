import { BaseModel } from '#/models/base';

export namespace ExternalPlatformPlatformEndpointApi {
  export interface ExternalPlatformPlatformEndpoint {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    platform: number;
    endpoint_type: string;
    name: string;
    path: string;
    http_method: string;
    require_auth: boolean;
    description: string;
  }
}

export class ExternalPlatformPlatformEndpointModel extends BaseModel<ExternalPlatformPlatformEndpointApi.ExternalPlatformPlatformEndpoint> {
  constructor() {
    super('/external_platform/platform_endpoint/');
  }
}
