import { BaseModel } from '#/models/base';

export namespace WorkOrderBaseApi {
  export interface WorkOrderBase {
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
    external_id: number;
    external_roll_number: string;
    external_handle_rel_expire_time: string;
    external_src_way: string;
    external_payroll_name: string;
    external_company_tel: string;
    external_addr: string;
    external_region_district_id: string;
    external_note14: string;
    external_distribute_way: string;
    external_payroll_type: string;
    external_event_type2_id: string;
    external_roll_content: string;
    external_note: string;
    external_product_ids: string;
    external_addr2: string;
    external_company_address: string;
    external_order_number: string;
    external_normal_payroll_title: string;
    external_addr3: string;
    external_note1: string;
    external_note15: string;
    external_attachments: any;
    external_note4: string;
    external_handling_quality: string;
    external_note12: string;
    external_note2: string;
    external_note3: string;
    external_note16: string;
    external_note17: string;
    current_node: string;
    work_flow: any;
  }
}

export class WorkOrderBaseModel extends BaseModel<WorkOrderBaseApi.WorkOrderBase> {
  constructor() {
    super('/work_order/base/');
  }
}
