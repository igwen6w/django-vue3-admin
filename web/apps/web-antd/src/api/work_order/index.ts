import { requestClient } from '#/api/request';

// interface PlatformLoginRequest {
//     platform_sign: string;
//     account: string;
//     password: string;
// }


/**
 * 工单详情
 * @param data 所需数据
 */
async function login(params: any) {
    return requestClient.get(`/work_order/base/`, {
    params,
  });
}

export {
    login
}