import { BaseModel } from '#/models/base';

export namespace WorkOrderDistributeApi {
  export interface WorkOrderDistribute {
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
    external_dept_send_msg: string;
    external_note: string;
    external_expires: number;
  }
}

export class WorkOrderDistributeModel extends BaseModel<WorkOrderDistributeApi.WorkOrderDistribute> {
  constructor() {
    super('/work_order/distribute/');
  }
}
