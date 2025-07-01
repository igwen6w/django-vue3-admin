import { BaseModel } from '#/models/base';

export namespace ${app_name_camel}${model_name}Api {
  export interface ${app_name_camel}${model_name} {
$interface_fields
  }
}

export class ${app_name_camel}${model_name}Model extends BaseModel<${app_name_camel}${model_name}Api.${app_name_camel}${model_name}> {
  constructor() {
    super('/$app_name/${model_name_lower}/');
  }
}
