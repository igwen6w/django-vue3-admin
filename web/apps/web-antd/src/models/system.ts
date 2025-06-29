import { BaseModel } from '#/models/base';

export namespace SystemDictTypeApi {
  export interface SystemDictType {
    [key: string]: any;
    id: string;
    name: string;
    type: string;
  }
}

export class SystemDictTypeModel extends BaseModel<SystemDictTypeApi.SystemDictType> {
  constructor() {
    super('/system/dict_type/');
  }
}
