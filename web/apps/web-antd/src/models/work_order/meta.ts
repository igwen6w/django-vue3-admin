import { BaseModel } from '#/models/base';

export namespace WorkOrderMetaApi {
  export interface WorkOrderMeta {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    version: string;
    source_system: string;
    sync_task_id: number;
    sync_status: boolean;
    sync_time: string;
    raw_data: any;
    pull_task_id: number;
  }
}

export class WorkOrderMetaModel extends BaseModel<WorkOrderMetaApi.WorkOrderMeta> {
  constructor() {
    super('/work_order/meta/');
  }
}
