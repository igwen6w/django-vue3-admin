import { BaseModel } from '#/models/base';

export namespace ExternalPlatformExternalDistrictNodeApi {
  export interface ExternalPlatformExternalDistrictNode {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    name: string;
    code: string;
    parent: number;
  }
}

export class ExternalPlatformExternalDistrictNodeModel extends BaseModel<ExternalPlatformExternalDistrictNodeApi.ExternalPlatformExternalDistrictNode> {
  constructor() {
    super('/external_platform/external_district_node/');
  }
}
