import { BaseModel } from '#/models/base';

export namespace WorkOrderSuperviseApi {
  export interface WorkOrderSupervise {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    base: number;
    external_ps_caption: string;
    external_record_number: string;
    external_public_record: number;
    external_user_id_hide: string;
    external_co_di_ids: any;
    external_co_di_ids_hide: any;
    external_pss_status_attr: string;
    external_di_ids: any;
    external_di_ids_hide: any;
    external_psot_name: string;
    external_psot_attr: string;
    external_pso_caption: string;
    external_note: string;
    external_refuse_di_ids: any;
    external_refuse_di_ids_hide: any;
  }
}

export class WorkOrderSuperviseModel extends BaseModel<WorkOrderSuperviseApi.WorkOrderSupervise> {
  constructor() {
    super('/work_order/supervise/');
  }
}
