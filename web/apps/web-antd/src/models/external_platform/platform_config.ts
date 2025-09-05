import { BaseModel } from '#/models/base';

export namespace ExternalPlatformPlatformConfigApi {
  export interface ExternalPlatformPlatformConfig {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    platform: number;
    config_key: string;
    config_value: any;
    description: string;
  }
}

export class ExternalPlatformPlatformConfigModel extends BaseModel<ExternalPlatformPlatformConfigApi.ExternalPlatformPlatformConfig> {
  constructor() {
    super('/external_platform/platform_config/');
  }
}
