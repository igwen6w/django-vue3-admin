# 开发备注

## 工单流程

```API
GET /payroll3/sub_act.php
```

```json
[
  {
    "ps_caption": "受理",
    "pss_caption_start": "待受理",
    "pss_caption_end": "待补充",
    "ps_caption_current": "结案",
    "p_pss_caption_current": "已结案",
    "id": "140252281",
    "opper": "4120",
    "pso_caption": "提交",
    "date": "2025-09-11 09:24:15",
    "di_title_o": "二组",
    "di_title": "政府服务热线-受理组-二组",
    "payroll_resulttmp": "已受理"
  },
  {
    "ps_caption": "预审",
    "pss_caption_start": "待派遣",
    "pss_caption_end": "已派遣",
    "ps_caption_current": "结案",
    "p_pss_caption_current": "已结案",
    "id": "140257499",
    "opper": "1053",
    "pso_caption": "确定",
    "date": "2025-09-11 09:41:25",
    "di_title_o": "审核组",
    "di_title": "政府服务热线-审核组",
    "payroll_resulttmp": "已派遣"
  },
  {
    "ps_caption": "处置",
    "pss_caption_start": "待处置",
    "pss_caption_end": "已处置",
    "ps_caption_current": "结案",
    "p_pss_caption_current": "已结案",
    "id": "140299403",
    "opper": "tsq7",
    "pso_caption": "通过",
    "date": "2025-09-11 14:29:14",
    "di_title_o": "泰山区政府",
    "di_title": "联动单位-泰山区政府",
    "payroll_resulttmp": "已处置"
  },
  {
    "ps_caption": "回访",
    "pss_caption_start": "待回访",
    "pss_caption_end": "待督办",
    "ps_caption_current": "结案",
    "p_pss_caption_current": "已结案",
    "id": "140310367",
    "opper": "5044",
    "pso_caption": "结案",
    "date": "2025-09-11 15:14:09",
    "di_title_o": "回访组",
    "di_title": "政府服务热线-回访组",
    "payroll_resulttmp": "已回访"
  },
  {
    "ps_caption": "结案",
    "pss_caption_start": "待结案",
    "pss_caption_end": "已结案",
    "ps_caption_current": "结案",
    "p_pss_caption_current": "已结案",
    "id": "140310369",
    "opper": "5044",
    "pso_caption": "结案",
    "date": "2025-09-11 15:14:09",
    "di_title_o": "回访组",
    "di_title": "政府服务热线-回访组",
    "payroll_resulttmp": "已结案"
  }
]
```

## 处置工单

### url

```javascript
/payroll3/sub_act.php?act=self_submit&flag=99&module_name=处置
```

### payload

```json
{
  "ps_caption": "处置",
  "record_number": "250912101108115409",
  "public_record": 2,
  "user_id_hide": null,
  "co_di_ids": null,
  "co_di_ids_hide": null,
  "pss_status_attr": "待处置",
  "di_ids": null,
  "di_ids_hide": null,
  "psot_name": "处置",
  "psot_attr": "处置",
  // 诉求属实
  "note1": "是",
  // 超职责诉求
  "distribute_way": "否",
  // 申请类型
  "note8": "超出行政范围类",
  // 附件: 证件附件/联系证据/办理附件
  "d_attachments": [
    "file/2025-09-12/250912101108115409_1757645358_wechat_2025-09-10_162839_842.png",
    "file/2025-09-12/250912101108115409_1757645371_wechat_2025-09-10_162839_842.png",
    "file/2025-09-12/250912101108115409_1757645385_wechat_2025-09-10_162839_842.png"
  ],
  // 联系群众
  "note3": "已联系",
  // 联系号码
  "note4": "123",
  // 联系时间
  "note5": "123",
  // 是否解决
  "note6": "已解决",
  // 未解决原因
  "note11": "123123",
  // 办理情况
  "note": "123123",
  // 公开答复内容
  "note10": "123123123123123123123",
  "pso_caption": "确定"
}
```

## 下派工单

### 发起下派

#### URL

```API
POST /payroll3/sub_act.php?act=submit&flag=9&module_name=处置
```

#### Payload

```json
{
  "ps_caption": "处置",
  "record_number": "250912101108115409",
  "public_record": 2,
  "user_id_hide": null,
  "co_di_ids": null,
  "co_di_ids_hide": null,
  "pss_status_attr": "待处置",
  "pso_caption": "确定",
  "di_ids": "泰山区委政研室,泰山区委组织部",
  "di_ids_hide": "533,529",
  "psot_name": "加派",
  "psot_attr": "加派",
  "expires": 5,
  "note": "嗯杜甫草堂个疑惑不解那么快",
  "dept_send_msg": "533,529"
}
```

## 督办工单

### 请求

```API
POST /payroll3/sub_act.php?act=self_submit&flag=99&module_name=处置
```

```json
{
  "ps_caption": "处置",
  "record_number": "250912101108115409",
  "public_record": 2,
  "user_id_hide": null,
  "co_di_ids": null,
  "co_di_ids_hide": null,
  "pss_status_attr": "待处置",
  "di_ids": null,
  "di_ids_hide": null,
  "refuse_di_ids": "泰山区住建局",
  "refuse_di_ids_hide": "556",
  "psot_name": "督办",
  "psot_attr": "督办",
  "note": "123123",
  "pso_caption": "确定"
}
