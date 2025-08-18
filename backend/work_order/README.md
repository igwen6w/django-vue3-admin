# 工单系统

## 获取市中心工单系统登录状态

### 数据模型

```sql
-- 外部会话授权信息表
CREATE TABLE external_auth_session (
    id BIGSERIAL PRIMARY KEY,
    system_name VARCHAR(100) NOT NULL,        -- 外部系统标识
    account VARCHAR(100) NOT NULL,            -- 登录账号
    cookie JSONB NOT NULL,                    -- Cookie/Token 信息 (结构化存储)
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- 状态: active / expired / failed
    expire_at TIMESTAMP WITH TIME ZONE,       -- 登录态过期时间
    last_login_at TIMESTAMP WITH TIME ZONE,   -- 最近一次登录时间
    update_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    create_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 确保 (system_name, account) 唯一，避免重复
CREATE UNIQUE INDEX idx_auth_session_unique 
ON auth_session(system_name, account);

-- 外部 API 请求记录表
CREATE TABLE external_api_log (
    -- 公共字段已隐藏
    system_name VARCHAR(100) NOT NULL,          -- 外部系统标识
    account VARCHAR(100),                       -- 使用的账号(有些接口可能不需要账号)
    api_endpoint VARCHAR(255) NOT NULL,         -- 请求的接口路径或功能标识
    request_method VARCHAR(10) NOT NULL,        -- 请求方法: GET / POST / PUT / DELETE
    request_payload JSONB,                      -- 请求参数/Body
    response_status INT,                        -- 响应状态码 (如 200, 403, 500)
    response_time_ms INT,                       -- 响应耗时(毫秒)
    response_body JSONB,                        -- 响应内容(存储结构化结果,二进制文件存储文件路径)
    hook JSONB,                                 -- 请求后需要执行的 hook
    hook_result JSONB,                          -- hook 结果, 例如验证码解析结果
    success BOOLEAN NOT NULL,                   -- 是否调用成功
    error_message TEXT,                         -- 错误原因(解析失败/异常栈)
);

-- 建立索引
CREATE INDEX idx_external_api_log_system 
ON external_api_log(system_name, created_time DESC);

CREATE INDEX idx_external_api_log_success 
ON external_api_log(success);


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