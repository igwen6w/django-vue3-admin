import { BaseModel } from '#/models/base';

export namespace SystemUserApi {
  export interface SystemUser {
    id: number;
    password: string;
    last_login: string;
    is_superuser: boolean;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    is_staff: boolean;
    is_active: boolean;
    date_joined: string;
    remark: string;
    creator: string;
    modifier: string;
    update_time: string;
    create_time: string;
    is_deleted: boolean;
    mobile: string;
    nickname: string;
    gender: number;
    language: string;
    city: string;
    province: string;
    country: string;
    avatar_url: string;
    status: number;
    login_date: string;
    login_ip: any;
  }
}

export class SystemUserModel extends BaseModel<SystemUserApi.SystemUser> {
  constructor() {
    super('/system/user/');
  }
}
