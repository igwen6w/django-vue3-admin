# 工单系统

## 获取市中心工单系统登录状态

### 数据模型

```sql


-- API 端点
CREATE TABLE external_api_endpoint (
    -- 公共字段已隐藏
    system_name VARCHAR(100) NOT NULL,       -- 外部系统标识
    name VARCHAR(100) NOT NULL,              -- 接口名称(如: 登录、获取验证码)
    endpoint VARCHAR(255) NOT NULL,          -- 相对路径 (如 /login, /captcha)
    http_method VARCHAR(10) NOT NULL,        -- 请求方法: GET / POST / PUT / DELETE
    require_auth BOOLEAN NOT NULL DEFAULT FALSE, -- 是否需要携带登录态
    description TEXT                        -- 接口说明
);

-- 一个系统里 (接口路径 + method) 唯一
CREATE UNIQUE INDEX idx_external_api_endpoint_unique
ON external_api_endpoint(system_name, endpoint, http_method);


```

### 工作流程图

flowchart TD
    A{检查本地登录态是否有效?} -->|有效| B[返回登录态给调用方]
    A -->|无效或过期| C[请求验证码URL<br>获取验证码图片和初始Cookie]
    C --> D[保存初始Cookie<br>解码验证码]
    D --> E[携带Cookie + 账号 + 验证码<br>发送登录请求]
    E --> F{登录成功?}
    F -->|是| G[保存最新Cookie<br>持久化到Redis/DB]
    G --> H[返回登录态给调用方]
    F -->|否| I[登录失败<br>重试登录,有限次数]
    I --> E

## 市中心工单系统登录状态定时检查



## 拉取工单