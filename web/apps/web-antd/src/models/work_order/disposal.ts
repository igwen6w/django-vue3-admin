import { BaseModel } from '#/models/base';

export namespace WorkOrderDisposalApi {
  export interface WorkOrderDisposal {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    version: string;
    source_system: string;
    sync_task_name: string;
    sync_task_id: string;
    sync_status: boolean;
    sync_time: string;
    base: number;
    external_ps_caption: string;
    external_record_number: string;
    external_public_record: number;
    external_user_id_hide: string;
    external_co_di_ids: string;
    external_co_di_ids_hide: string;
    external_pss_status_attr: string;
    external_di_ids: string;
    external_di_ids_hide: string;
    external_psot_name: string;
    external_psot_attr: string;
    external_pso_caption: string;
    external_note1: string;
    external_distribute_way: string;
    external_note8: string;
    external_d_attachments: any;
    external_note3: string;
    external_note4: string;
    external_note5: string;
    external_note6: string;
    external_note11: string;
    external_note: string;
    external_note10: string;
    attachments_credentials: any;
    attachments_contact: any;
    attachments_handle: any;
  }
}

export class WorkOrderDisposalModel extends BaseModel<WorkOrderDisposalApi.WorkOrderDisposal> {
  constructor() {
    super('/work_order/disposal/');
  }
}
