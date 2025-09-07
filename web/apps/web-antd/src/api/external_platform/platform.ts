import { requestClient } from '#/api/request';

interface PlatformLoginRequest {
    platform_sign: string;
    account: string;
    password: string;
}


/**
 * 平台登录
 * @param data 登录所需数据
 */
async function login(data: PlatformLoginRequest) {
    return requestClient.post(`/external_platform/login/`, data);
}

export {
    login
}