import { BaseModel } from '#/models/base';

export namespace WorkOrderCategoryApi {
  export interface WorkOrderCategory {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    name: string;
    description: string;
    parent: number;
  }
}

export class WorkOrderCategoryModel extends BaseModel<WorkOrderCategoryApi.WorkOrderCategory> {
  constructor() {
    super('/work_order/category/');
  }
}
