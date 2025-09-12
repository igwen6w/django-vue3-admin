import { BaseModel } from '#/models/base';

export namespace WorkOrderDistributeOpinionPresetApi {
  export interface WorkOrderDistributeOpinionPreset {
    id: number;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    dept: number;
    category: number;
    description: string;
    title: string;
  }
}

export class WorkOrderDistributeOpinionPresetModel extends BaseModel<WorkOrderDistributeOpinionPresetApi.WorkOrderDistributeOpinionPreset> {
  constructor() {
    super('/work_order/distribute_opinion_preset/');
  }
}
