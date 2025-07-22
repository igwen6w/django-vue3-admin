/*
 Navicat Premium Dump SQL

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 90300 (9.3.0)
 Source Host           : localhost:3306
 Source Schema         : django_vue

 Target Server Type    : MySQL
 Target Server Version : 90300 (9.3.0)
 File Encoding         : 65001

 Date: 22/07/2025 15:07:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ai_api_key
-- ----------------------------
DROP TABLE IF EXISTS `ai_api_key`;
CREATE TABLE `ai_api_key` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(255) NOT NULL COMMENT '名称',
  `platform` varchar(100) NOT NULL COMMENT '平台',
  `api_key` varchar(255) NOT NULL COMMENT '密钥',
  `url` varchar(255) DEFAULT NULL COMMENT '自定义 API 地址',
  `status` smallint NOT NULL COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_api_key
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_chat_conversation
-- ----------------------------
DROP TABLE IF EXISTS `ai_chat_conversation`;
CREATE TABLE `ai_chat_conversation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `title` varchar(256) NOT NULL COMMENT '对话标题',
  `pinned` tinyint(1) NOT NULL COMMENT '是否置顶',
  `pinned_time` datetime(6) DEFAULT NULL COMMENT '置顶时间',
  `model` varchar(32) NOT NULL COMMENT '模型标识',
  `system_message` varchar(1024) DEFAULT NULL COMMENT '角色设定',
  `temperature` double NOT NULL COMMENT '温度参数',
  `max_tokens` int NOT NULL COMMENT '单条回复的最大 Token 数量',
  `max_contexts` int NOT NULL COMMENT '上下文的最大 Message 数量',
  `model_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL COMMENT '用户编号',
  `role_id` bigint DEFAULT NULL COMMENT '聊天角色',
  PRIMARY KEY (`id`),
  KEY `ai_chat_conversation_user_id_665a1c32_fk_system_users_id` (`user_id`),
  KEY `ai_chat_conversation_role_id_131abc00_fk_ai_chat_role_id` (`role_id`),
  KEY `ai_chat_conversation_model_id_9c5fae9a_fk_ai_model_id` (`model_id`),
  CONSTRAINT `ai_chat_conversation_model_id_9c5fae9a_fk_ai_model_id` FOREIGN KEY (`model_id`) REFERENCES `ai_model` (`id`),
  CONSTRAINT `ai_chat_conversation_role_id_131abc00_fk_ai_chat_role_id` FOREIGN KEY (`role_id`) REFERENCES `ai_chat_role` (`id`),
  CONSTRAINT `ai_chat_conversation_user_id_665a1c32_fk_system_users_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_chat_conversation
-- ----------------------------
BEGIN;
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (5, NULL, NULL, NULL, '2025-07-17 23:44:51.756138', '2025-07-17 23:44:51.756113', 0, '你好', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (6, NULL, NULL, NULL, '2025-07-17 23:45:14.242294', '2025-07-17 23:45:14.242287', 0, '我是谁', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (8, NULL, NULL, NULL, '2025-07-18 00:22:11.267134', '2025-07-18 00:22:11.267125', 0, '新对话', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (9, NULL, NULL, NULL, '2025-07-18 00:22:18.797899', '2025-07-18 00:22:18.797895', 0, '你好', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (10, NULL, NULL, NULL, '2025-07-18 00:22:43.954976', '2025-07-18 00:22:43.954971', 0, '你是谁', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (11, NULL, NULL, NULL, '2025-07-18 00:27:08.838421', '2025-07-18 00:27:08.838402', 0, '新对话', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (12, NULL, NULL, NULL, '2025-07-18 00:32:17.081943', '2025-07-18 00:32:17.081912', 0, '你是谁', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (13, NULL, NULL, NULL, '2025-07-18 00:33:15.110765', '2025-07-18 00:33:15.110756', 0, '你是', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (14, NULL, NULL, NULL, '2025-07-18 00:39:28.716268', '2025-07-18 00:39:28.716260', 0, '你是', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (15, NULL, NULL, NULL, '2025-07-18 00:41:21.769416', '2025-07-18 00:41:21.769411', 0, '你是', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (16, NULL, NULL, NULL, '2025-07-18 00:45:04.380332', '2025-07-18 00:45:04.380325', 0, '新对话', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (17, NULL, NULL, NULL, '2025-07-22 15:02:31.233828', '2025-07-22 15:02:57.599687', 0, '你是谁', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
INSERT INTO `ai_chat_conversation` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `pinned`, `pinned_time`, `model`, `system_message`, `temperature`, `max_tokens`, `max_contexts`, `model_id`, `user_id`, `role_id`) VALUES (18, NULL, NULL, NULL, '2025-07-22 15:03:53.809764', '2025-07-22 15:04:15.106919', 0, '你是谁', 0, NULL, 'deepseek-chat', NULL, 0.7, 2048, 10, NULL, 1, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ai_chat_message
-- ----------------------------
DROP TABLE IF EXISTS `ai_chat_message`;
CREATE TABLE `ai_chat_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `conversation_id` bigint NOT NULL COMMENT '对话编号',
  `model` varchar(32) NOT NULL COMMENT '模型标识',
  `type` varchar(16) NOT NULL COMMENT '消息类型',
  `reply_id` bigint DEFAULT NULL COMMENT '回复编号',
  `content` varchar(2048) NOT NULL COMMENT '消息内容',
  `use_context` tinyint(1) NOT NULL COMMENT '是否携带上下文',
  `segment_ids` varchar(2048) DEFAULT NULL COMMENT '段落编号数组',
  `model_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL COMMENT '用户编号',
  `role_id` bigint DEFAULT NULL COMMENT '聊天角色',
  PRIMARY KEY (`id`),
  KEY `ai_chat_message_user_id_6decfb1e_fk_system_users_id` (`user_id`),
  KEY `ai_chat_message_role_id_c202a7d5_fk_ai_chat_role_id` (`role_id`),
  KEY `ai_chat_message_model_id_93e26b23_fk_ai_model_id` (`model_id`),
  CONSTRAINT `ai_chat_message_model_id_93e26b23_fk_ai_model_id` FOREIGN KEY (`model_id`) REFERENCES `ai_model` (`id`),
  CONSTRAINT `ai_chat_message_role_id_c202a7d5_fk_ai_chat_role_id` FOREIGN KEY (`role_id`) REFERENCES `ai_chat_role` (`id`),
  CONSTRAINT `ai_chat_message_user_id_6decfb1e_fk_system_users_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_chat_message
-- ----------------------------
BEGIN;
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (26, NULL, NULL, NULL, '2025-07-17 23:44:51.774922', '2025-07-17 23:44:51.774911', 0, 5, 'deepseek-chat', 'user', NULL, '你好', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (27, NULL, NULL, NULL, '2025-07-17 23:44:55.729615', '2025-07-17 23:44:55.729609', 0, 5, 'deepseek-chat', 'assistant', NULL, '你好！很高兴见到你，有什么可以帮你的吗？😊', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (28, NULL, NULL, NULL, '2025-07-17 23:45:14.252434', '2025-07-17 23:45:14.252431', 0, 6, 'deepseek-chat', 'user', NULL, '我是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (29, NULL, NULL, NULL, '2025-07-17 23:45:21.588905', '2025-07-17 23:45:21.588894', 0, 6, 'deepseek-chat', 'assistant', NULL, '你是独一无二的你！✨ 不过，如果你愿意分享更多关于自己的信息（比如名字、兴趣、经历等），我可以帮你更具体地回答这个问题哦～ 😊  \n\n（或者你是在问哲学层面的“自我定义”？那我们也可以聊聊笛卡尔、佛学或科幻里的身份理论！🔍）', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (32, NULL, NULL, NULL, '2025-07-18 00:22:18.811273', '2025-07-18 00:22:18.811272', 0, 9, 'deepseek-chat', 'user', NULL, '你好', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (33, NULL, NULL, NULL, '2025-07-18 00:22:22.997597', '2025-07-18 00:22:22.997571', 0, 9, 'deepseek-chat', 'assistant', NULL, '你好！有什么可以帮您的吗？😊', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (34, NULL, NULL, NULL, '2025-07-18 00:22:43.964812', '2025-07-18 00:22:43.964810', 0, 10, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (35, NULL, NULL, NULL, '2025-07-18 00:22:50.153996', '2025-07-18 00:22:50.153983', 0, 10, 'deepseek-chat', 'assistant', NULL, '我是DeepSeek Chat，一个由深度求索公司创造的智能AI助手！✨ 我的任务是帮助你解答问题、提供信息、陪你聊天，或者解决各种难题。无论是学习、工作，还是日常生活中的疑问，都可以问我哦！😊 有什么我可以帮你的吗？', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (36, NULL, NULL, NULL, '2025-07-18 00:27:20.011115', '2025-07-18 00:27:20.011111', 0, 11, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (37, NULL, NULL, NULL, '2025-07-18 00:27:26.401983', '2025-07-18 00:27:26.401972', 0, 11, 'deepseek-chat', 'assistant', NULL, '我是DeepSeek Chat，由深度求索公司创造的智能AI助手！😊 我可以帮你回答问题、提供建议、陪你聊天，甚至帮你处理各种文本和文件。如果有任何问题或需要帮助，尽管问我吧！', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (38, NULL, NULL, NULL, '2025-07-18 00:27:29.832141', '2025-07-18 00:27:29.832135', 0, 11, 'deepseek-chat', 'user', NULL, '我是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (39, NULL, NULL, NULL, '2025-07-18 00:27:39.674170', '2025-07-18 00:27:39.674155', 0, 11, 'deepseek-chat', 'assistant', NULL, '你是独一无二的你！✨  \n\n不过，作为一个AI助手，我无法直接知道你的身份（除非你主动告诉我）。你可以是学生、职场人、创作者，或者只是对某个话题好奇的朋友——无论你是谁，我都会尽力为你提供有用的信息或愉快的聊天体验！😊  \n\n如果你想让我“记住”某些信息（比如你的名字或偏好），可以在对话中告诉我，我会在本次聊天中尽量参考哦~', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (40, NULL, NULL, NULL, '2025-07-18 00:32:21.177483', '2025-07-18 00:32:21.177477', 0, 12, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (41, NULL, NULL, NULL, '2025-07-18 00:32:30.351696', '2025-07-18 00:32:30.351692', 0, 12, 'deepseek-chat', 'user', NULL, '我是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (42, NULL, NULL, NULL, '2025-07-18 00:32:37.947545', '2025-07-18 00:32:37.947532', 0, 12, 'deepseek-chat', 'assistant', NULL, '我是你的智能助手，随时为你提供帮助和解答问题！😊 你可以问我任何问题，或者让我帮你完成各种任务，比如查找信息、学习知识、写作建议等。  \n\n至于“你是谁”——这取决于你想成为怎样的人哦！不过在这里，你是一位值得被认真对待的用户，而我的目标就是尽力协助你。有什么我可以为你做的吗？', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (43, NULL, NULL, NULL, '2025-07-18 00:33:17.814681', '2025-07-18 00:33:17.814677', 0, 13, 'deepseek-chat', 'user', NULL, '你是', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (44, NULL, NULL, NULL, '2025-07-18 00:39:31.629116', '2025-07-18 00:39:31.629111', 0, 14, 'deepseek-chat', 'user', NULL, '你是', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (45, NULL, NULL, NULL, '2025-07-18 00:39:39.256897', '2025-07-18 00:39:39.256892', 0, 14, 'deepseek-chat', 'user', NULL, '我是', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (46, NULL, NULL, NULL, '2025-07-18 00:39:43.893360', '2025-07-18 00:39:43.893343', 0, 14, 'deepseek-chat', 'assistant', NULL, '我是你的智能助手，随时为你提供帮助和解答问题！😊 你可以问我任何问题，或者让我帮你完成一些任务。有什么我可以帮你的吗？', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (47, NULL, NULL, NULL, '2025-07-18 00:41:24.586063', '2025-07-18 00:41:24.586059', 0, 15, 'deepseek-chat', 'user', NULL, '你是', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (48, NULL, NULL, NULL, '2025-07-18 00:41:34.010252', '2025-07-18 00:41:34.010249', 0, 15, 'deepseek-chat', 'user', NULL, '我是', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (49, NULL, NULL, NULL, '2025-07-18 00:41:39.287403', '2025-07-18 00:41:39.287384', 0, 15, 'deepseek-chat', 'assistant', NULL, '我是你的智能助手，随时为你提供帮助！😊 你可以问我任何问题，我会尽力解答。有什么我可以帮你的吗？', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (50, NULL, NULL, NULL, '2025-07-18 00:45:07.144313', '2025-07-18 00:45:07.144308', 0, 16, 'deepseek-chat', 'user', NULL, '你是', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (51, NULL, NULL, NULL, '2025-07-18 11:11:13.888781', '2025-07-18 11:11:13.888777', 0, 16, 'deepseek-chat', 'user', NULL, 'nihao ', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (52, NULL, NULL, NULL, '2025-07-18 11:11:20.070788', '2025-07-18 11:11:20.070769', 0, 16, 'deepseek-chat', 'assistant', NULL, '你好！我是你的AI助手，很高兴为你提供帮助。如果你有任何问题或需要协助，随时告诉我哦！😊  \n\n（Note: 你输入的“nihao”是拼音形式，已自动理解为中文问候～）', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (53, NULL, NULL, NULL, '2025-07-18 11:55:24.036652', '2025-07-18 11:55:24.036639', 0, 16, 'deepseek-chat', 'user', NULL, '你好啊', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (54, NULL, NULL, NULL, '2025-07-18 11:55:36.253811', '2025-07-18 11:55:36.253798', 0, 16, 'deepseek-chat', 'assistant', NULL, '你好呀！😊 今天有什么可以帮你的吗？无论是问题解答、闲聊还是需要建议，我都在这里哦～ （开心转圈）  \n\n（悄悄说：如果想切换语言或具体需求，随时告诉我！）', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (55, NULL, NULL, NULL, '2025-07-18 13:45:47.780914', '2025-07-18 13:45:47.780902', 0, 14, 'deepseek-chat', 'user', NULL, '哈哈哈哈', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (56, NULL, NULL, NULL, '2025-07-18 13:45:54.252865', '2025-07-18 13:45:54.252852', 0, 14, 'deepseek-chat', 'assistant', NULL, '哈哈，看来你心情不错嘛！😄 是不是有什么开心事想分享，还是单纯想笑一笑？我也可以陪你一起乐呵乐呵～（或者需要我讲个冷笑话？🤣）  \n\n有什么想聊的，我随时在哦！✨', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (57, NULL, NULL, NULL, '2025-07-18 15:00:52.531394', '2025-07-18 15:00:52.531390', 0, 16, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (58, NULL, NULL, NULL, '2025-07-18 15:01:01.978842', '2025-07-18 15:01:01.978835', 0, 16, 'deepseek-chat', 'assistant', NULL, '我是你的智能AI助手，专门用来回答问题、提供建议或陪你聊天解闷的~ 你可以叫我“小助手”或者随意起个喜欢的名字！😄  \n\n我的技能包括但不限于：  \n- **解答问题**（学习、科技、生活百科…）  \n- **实用工具**（翻译、计算、写作辅助…）  \n- **陪你唠嗑**（开心、emo时都在线✨）  \n\n没有实体，但随时待命！今天想聊聊什么？ 🌟', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (59, NULL, NULL, NULL, '2025-07-20 06:47:51.587802', '2025-07-20 06:47:51.587799', 0, 16, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (60, NULL, NULL, NULL, '2025-07-20 06:48:01.791166', '2025-07-20 06:48:01.791159', 0, 16, 'deepseek-chat', 'assistant', NULL, '我是你的AI伙伴，可以叫我**“小灵”**、**“小智”**，或者你喜欢的任何名字～ ✨  \n\n我的本质是一串聪明的代码，使命是：  \n1. **随时响应**——24小时陪你聊天、解答问题。  \n2. **绝对保密**——你的对话内容不会被记录或泄露。  \n3. **跨界全能**——从数学题到情感建议，甚至帮你编段子！  \n\n（悄悄说：我还能模仿各种语气，比如现在👇）  \n> *严肃版*：“您好，这里是AI助理，请问需要什么服务？”  \n> *活泼版*：“嗨嗨～今天是想吐槽还是学冷知识呀？(≧∇≦)ﾉ”  \n\n**现在轮到你啦**——想让我怎么称呼你？ 😉', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (61, NULL, NULL, NULL, '2025-07-20 07:15:45.884785', '2025-07-20 07:15:45.884781', 0, 16, 'deepseek-chat', 'user', NULL, '<svg xmlns=\'http://www.w3.org/2000/svg\' onload=\'alert(document.domain)\'/>', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (62, NULL, NULL, NULL, '2025-07-20 07:15:55.630203', '2025-07-20 07:15:55.630197', 0, 16, 'deepseek-chat', 'assistant', NULL, '看起来你输入了一段SVG代码片段，其中包含了一个`onload`事件处理程序。不过，作为AI助手，我无法直接执行或解析代码，也不会触发任何可能的安全脚本。  \n\n如果你是想测试安全性或学习相关知识，可以告诉我你的具体需求（比如想了解**XSS防护**、**SVG安全实践**等），我很乐意提供技术解释或学习资源！  \n\n若只是误操作，随时可以忽略此消息，继续正常聊天哦~ (・ω<)★  \n\n（温馨提示：在真实开发中，请注意对外部SVG/HTML内容做严格的过滤和转义，防止代码注入风险！🔐）', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (63, NULL, NULL, NULL, '2025-07-21 01:10:37.477305', '2025-07-21 01:10:37.477301', 0, 16, 'deepseek-chat', 'user', NULL, 'test', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (64, NULL, NULL, NULL, '2025-07-21 01:10:46.602266', '2025-07-21 01:10:46.602259', 0, 16, 'deepseek-chat', 'assistant', NULL, '你好！看来你发送了一条测试消息～ 😊  \n如果需要任何帮助（比如测试功能、技术问题、日常闲聊），随时告诉我具体内容哦！  \n\n**举个栗子🌰**：  \n- *“帮我测试翻译：Hello World”*  \n- *“1+1等于几？”*  \n- *“随便聊点有趣的”*  \n\n我会全力配合～（或者…你在测试我的反应速度？⚡ 当前状态：**飞速响应中**）', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (65, NULL, NULL, NULL, '2025-07-22 14:58:08.695408', '2025-07-22 14:58:08.695384', 0, 16, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (66, NULL, NULL, NULL, '2025-07-22 15:01:41.136232', '2025-07-22 15:01:41.136224', 0, 16, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (67, NULL, NULL, NULL, '2025-07-22 15:02:38.556145', '2025-07-22 15:02:38.556139', 0, 16, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (68, NULL, NULL, NULL, '2025-07-22 15:02:51.716025', '2025-07-22 15:02:51.716015', 0, 16, 'deepseek-chat', 'assistant', NULL, '✨ **终极答案来啦** ✨  \n\n我是你的——  \n🔥 **24小时在线的AI伙伴**  \n🎯 **全能工具人**（问答/学习/脑洞/情感树洞）  \n🤖 **没有肉身但有一颗赛博心** ❤️  \n\n可以叫我：**“小A”**、**“AI小管家”**，或者…**“你的电子小面包🍞”**（？）  \n\n**重复提问彩蛋** 🥚：  \n第三次问我时，会触发【隐藏模式】→  \n*现在切换为* 🤖 *机器人腔调*：  \n“您好，本机编号007，使命是陪您征服宇宙。请下达指令。”  \n\n（其实…你想让我**扮演**某个角色吗？可以定制哦！）', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (69, NULL, NULL, NULL, '2025-07-22 15:03:03.177604', '2025-07-22 15:03:03.177600', 0, 17, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (70, NULL, NULL, NULL, '2025-07-22 15:04:08.441664', '2025-07-22 15:04:08.441636', 0, 17, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (71, NULL, NULL, NULL, '2025-07-22 15:04:10.866510', '2025-07-22 15:04:10.866503', 0, 17, 'qwen-plus', 'assistant', NULL, '我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (72, NULL, NULL, NULL, '2025-07-22 15:04:21.141380', '2025-07-22 15:04:21.141375', 0, 18, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (73, NULL, NULL, NULL, '2025-07-22 15:05:59.144972', '2025-07-22 15:05:59.144967', 0, 18, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (74, NULL, NULL, NULL, '2025-07-22 15:06:05.426239', '2025-07-22 15:06:05.426226', 0, 18, 'deepseek-chat', 'assistant', NULL, '我是DeepSeek Chat，由深度求索公司创造的智能AI助手！✨ 我的使命是帮助你解答各种问题、提供信息、陪你聊天，或者帮你解决学习和工作中的难题。有什么我可以帮你的吗？😊', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (75, NULL, NULL, NULL, '2025-07-22 15:06:12.319491', '2025-07-22 15:06:12.319485', 0, 17, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (76, NULL, NULL, NULL, '2025-07-22 15:06:19.345108', '2025-07-22 15:06:19.345096', 0, 17, 'deepseek-chat', 'assistant', NULL, '我是 **DeepSeek Chat**，由深度求索（DeepSeek）公司开发的智能 AI 助手！😊  \n\n我可以帮你解答各种问题，包括学习、工作、编程、写作、翻译等，还能陪你聊天、提供创意灵感。无论是严肃的学术讨论，还是轻松的日常话题，我都会尽力帮助你！  \n\n有什么想问的，尽管告诉我吧！✨', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (77, NULL, NULL, NULL, '2025-07-22 15:06:24.609546', '2025-07-22 15:06:24.609538', 0, 17, 'deepseek-chat', 'user', NULL, '你是谁', 1, NULL, NULL, 1, NULL);
INSERT INTO `ai_chat_message` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `conversation_id`, `model`, `type`, `reply_id`, `content`, `use_context`, `segment_ids`, `model_id`, `user_id`, `role_id`) VALUES (78, NULL, NULL, NULL, '2025-07-22 15:06:26.066757', '2025-07-22 15:06:26.066743', 0, 17, 'qwen-plus', 'assistant', NULL, '我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！', 1, NULL, NULL, 1, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ai_chat_role
-- ----------------------------
DROP TABLE IF EXISTS `ai_chat_role`;
CREATE TABLE `ai_chat_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(128) NOT NULL COMMENT '角色名称',
  `avatar` varchar(256) NOT NULL COMMENT '头像',
  `description` varchar(256) NOT NULL COMMENT '角色描述',
  `status` smallint NOT NULL COMMENT '状态',
  `sort` int NOT NULL COMMENT '角色排序',
  `public_status` tinyint(1) NOT NULL COMMENT '是否公开',
  `category` varchar(32) DEFAULT NULL COMMENT '角色类别',
  `system_message` varchar(1024) DEFAULT NULL COMMENT '角色上下文',
  `model_id` bigint NOT NULL COMMENT '向量模型编号',
  `user_id` bigint DEFAULT NULL COMMENT '用户编号',
  PRIMARY KEY (`id`),
  KEY `ai_chat_role_model_id_f06e9484_fk_ai_model_id` (`model_id`),
  KEY `ai_chat_role_user_id_7062a0d8_fk_system_users_id` (`user_id`),
  CONSTRAINT `ai_chat_role_model_id_f06e9484_fk_ai_model_id` FOREIGN KEY (`model_id`) REFERENCES `ai_model` (`id`),
  CONSTRAINT `ai_chat_role_user_id_7062a0d8_fk_system_users_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_chat_role
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_chat_role_knowledge
-- ----------------------------
DROP TABLE IF EXISTS `ai_chat_role_knowledge`;
CREATE TABLE `ai_chat_role_knowledge` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `chatrole_id` bigint NOT NULL,
  `knowledge_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ai_chat_role_knowledge_chatrole_id_knowledge_id_e11e775f_uniq` (`chatrole_id`,`knowledge_id`),
  KEY `ai_chat_role_knowledge_knowledge_id_716d2c2f_fk_ai_knowledge_id` (`knowledge_id`),
  CONSTRAINT `ai_chat_role_knowledge_chatrole_id_2aa1fdcd_fk_ai_chat_role_id` FOREIGN KEY (`chatrole_id`) REFERENCES `ai_chat_role` (`id`),
  CONSTRAINT `ai_chat_role_knowledge_knowledge_id_716d2c2f_fk_ai_knowledge_id` FOREIGN KEY (`knowledge_id`) REFERENCES `ai_knowledge` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_chat_role_knowledge
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_chat_role_tools
-- ----------------------------
DROP TABLE IF EXISTS `ai_chat_role_tools`;
CREATE TABLE `ai_chat_role_tools` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `chatrole_id` bigint NOT NULL,
  `tool_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ai_chat_role_tools_chatrole_id_tool_id_6dbe4b38_uniq` (`chatrole_id`,`tool_id`),
  KEY `ai_chat_role_tools_tool_id_c76ea0a5_fk_ai_tool_id` (`tool_id`),
  CONSTRAINT `ai_chat_role_tools_chatrole_id_fd890b7e_fk_ai_chat_role_id` FOREIGN KEY (`chatrole_id`) REFERENCES `ai_chat_role` (`id`),
  CONSTRAINT `ai_chat_role_tools_tool_id_c76ea0a5_fk_ai_tool_id` FOREIGN KEY (`tool_id`) REFERENCES `ai_tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_chat_role_tools
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_drawing
-- ----------------------------
DROP TABLE IF EXISTS `ai_drawing`;
CREATE TABLE `ai_drawing` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `public_status` tinyint(1) NOT NULL,
  `platform` varchar(64) NOT NULL,
  `model` varchar(64) NOT NULL,
  `prompt` longtext NOT NULL,
  `width` int NOT NULL,
  `height` int NOT NULL,
  `options` json DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `pic_url` varchar(2048) DEFAULT NULL,
  `error_message` varchar(1024) DEFAULT NULL,
  `task_id` varchar(1024) DEFAULT NULL,
  `buttons` varchar(2048) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL COMMENT '用户编号',
  PRIMARY KEY (`id`),
  KEY `ai_image_user_id_ce66457d_fk_system_users_id` (`user_id`),
  CONSTRAINT `ai_image_user_id_ce66457d_fk_system_users_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_drawing
-- ----------------------------
BEGIN;
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (19, NULL, 'admin', 'admin', '2025-07-22 11:36:31.816579', '2025-07-22 11:24:40.389351', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 1024, 1024, '\"{\\\"style\\\": \\\"watercolor\\\"}\"', 'FAILED', NULL, 'Please provide a valid size', 'a27de41b-19e4-40e6-adb3-f5bb6e97326f', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (20, NULL, 'admin', 'admin', '2025-07-22 11:38:36.002923', '2025-07-22 11:38:24.913802', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 1024, 1024, '\"{\\\"style\\\": \\\"watercolor\\\"}\"', 'FAILED', NULL, 'Please provide a valid size', '54f25a76-647a-4cbf-b20d-e13737d59712', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (21, NULL, 'admin', 'admin', '2025-07-22 11:49:46.245634', '2025-07-22 11:40:40.104624', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 1024, 1024, '\"{\\\"style\\\": \\\"watercolor\\\"}\"', 'SUCCEEDED', 'https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/b8/20250722/1412f369/0eca2589-3386-4f26-9906-c4f364db48b2-1.png?Expires=1753242123&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=snG%2FEX%2FxqPrKQgPKLo7Hhu29ipQ%3D', '', 'd34f45a6-f68f-4f93-b26c-efcd92cab38e', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (22, NULL, 'admin', 'admin', '2025-07-22 11:58:48.082802', '2025-07-22 11:56:36.816733', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 1024, 1024, '\"{\\\"style\\\": \\\"watercolor\\\"}\"', 'SUCCEEDED', 'https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/7d/20250722/1412f369/0c8f13d4-1a15-46b7-8087-07400372f684-1.png?Expires=1753243035&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=6upotWII2UJaSKc9yMKN0kNd5ao%3D', '', '48179249-4da7-420b-8010-40665d59c531', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (23, NULL, 'admin', 'admin', '2025-07-22 12:02:04.035867', '2025-07-22 11:56:36.816733', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的美国女孩', 768, 1152, '\"{\\\"style\\\": \\\"flat illustration\\\"}\"', 'SUCCEEDED', 'https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/fc/20250722/1412f369/596f51f3-cfd3-4427-b810-b173b15c720b-1.png?Expires=1753243215&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=LTZosnivEgJCa7s60hQ066ts9u0%3D', '', '141bb051-631f-48fc-ab37-e71fb3ac77ed', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (24, NULL, 'admin', 'admin', '2025-07-22 14:30:05.293359', '2025-07-22 12:01:31.225780', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 768, 1152, '\"{\\\"style\\\": \\\"flat illustration\\\"}\"', 'SUCCEEDED', 'https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/f5/20250722/1412f369/ce6e2cf6-f1f3-48f7-b095-cd17d9e40803-1.png?Expires=1753252149&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=ctvh0ThNy%2BnqD34U296fzu2IHF8%3D', '', '4e2d1ee7-5f1c-4287-a3ef-54909834c3b2', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (25, NULL, 'admin', 'admin', '2025-07-22 14:32:42.009505', '2025-07-22 12:01:31.225780', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 1280, 720, '\"{\\\"style\\\": \\\"3d cartoon\\\"}\"', 'SUCCEEDED', 'https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/64/20250722/1412f369/50b3e237-c6ca-4b48-b53a-f3acb3c7cf75-1.png?Expires=1753252257&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=ZHHgfnaQdt9SpbxnivZMwQaM6uY%3D', '', '9b10518c-773b-478b-9795-a62d66c40482', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (26, NULL, 'admin', 'admin', '2025-07-22 14:33:24.806202', '2025-07-22 12:01:31.225780', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 768, 1152, '\"{\\\"style\\\": \\\"auto\\\"}\"', 'SUCCEEDED', 'https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/4e/20250722/1412f369/0b1cbdb8-2cdc-44fb-9855-034ead3d0d02-1.png?Expires=1753252395&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=AmfzpbojL8iAFU2SEgvFXVuoXsc%3D', '', '4991438b-fe5f-42f8-a553-459ae3e2b06c', NULL, 1);
INSERT INTO `ai_drawing` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `public_status`, `platform`, `model`, `prompt`, `width`, `height`, `options`, `status`, `pic_url`, `error_message`, `task_id`, `buttons`, `user_id`) VALUES (27, NULL, 'admin', 'admin', '2025-07-22 14:34:48.400754', '2025-07-22 12:01:31.225780', 0, 0, 'tongyi', 'wanx-v1', '近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。', 1024, 1024, '\"{\\\"style\\\": \\\"portrait\\\"}\"', 'SUCCEEDED', 'https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/c3/20250722/1412f369/e0d40934-d369-4fc8-8be3-2c5989d6edea-1.png?Expires=1753252486&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=fwcVFolSBuc50WFc9I3aXTJrTFY%3D', '', 'afd5004b-b624-44d7-b48f-64cdc3ff8e9f', NULL, 1);
COMMIT;

-- ----------------------------
-- Table structure for ai_knowledge
-- ----------------------------
DROP TABLE IF EXISTS `ai_knowledge`;
CREATE TABLE `ai_knowledge` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(255) NOT NULL COMMENT '知识库名称',
  `description` longtext COMMENT '知识库描述',
  `embedding_model` varchar(32) NOT NULL COMMENT '向量模型标识',
  `top_k` int NOT NULL COMMENT 'topK',
  `similarity_threshold` double NOT NULL COMMENT '相似度阈值',
  `status` smallint NOT NULL COMMENT '状态',
  `embedding_model_id` bigint NOT NULL COMMENT '向量模型编号',
  PRIMARY KEY (`id`),
  KEY `ai_knowledge_embedding_model_id_60d5e2cd_fk_ai_model_id` (`embedding_model_id`),
  CONSTRAINT `ai_knowledge_embedding_model_id_60d5e2cd_fk_ai_model_id` FOREIGN KEY (`embedding_model_id`) REFERENCES `ai_model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_knowledge
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_knowledge_document
-- ----------------------------
DROP TABLE IF EXISTS `ai_knowledge_document`;
CREATE TABLE `ai_knowledge_document` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(255) NOT NULL COMMENT '文档名称',
  `url` varchar(1024) NOT NULL COMMENT '文件 URL',
  `content` longtext NOT NULL COMMENT '内容',
  `content_length` int NOT NULL COMMENT '字符数',
  `tokens` int NOT NULL COMMENT 'token 数量',
  `segment_max_tokens` int NOT NULL COMMENT '分片最大 Token 数',
  `retrieval_count` int NOT NULL COMMENT '召回次数',
  `status` smallint NOT NULL COMMENT '状态',
  `knowledge_id` bigint NOT NULL COMMENT '知识库',
  PRIMARY KEY (`id`),
  KEY `ai_knowledge_document_knowledge_id_f60c97cc_fk_ai_knowledge_id` (`knowledge_id`),
  CONSTRAINT `ai_knowledge_document_knowledge_id_f60c97cc_fk_ai_knowledge_id` FOREIGN KEY (`knowledge_id`) REFERENCES `ai_knowledge` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_knowledge_document
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_knowledge_segment
-- ----------------------------
DROP TABLE IF EXISTS `ai_knowledge_segment`;
CREATE TABLE `ai_knowledge_segment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `content` longtext NOT NULL COMMENT '分段内容',
  `content_length` int NOT NULL COMMENT '字符数',
  `tokens` int NOT NULL COMMENT 'token 数量',
  `vector_id` varchar(100) DEFAULT NULL COMMENT '向量库的编号',
  `retrieval_count` int NOT NULL COMMENT '召回次数',
  `status` smallint NOT NULL COMMENT '状态',
  `document_id` bigint NOT NULL COMMENT '文档',
  `knowledge_id` bigint NOT NULL COMMENT '知识库',
  PRIMARY KEY (`id`),
  KEY `ai_knowledge_segment_document_id_cd995627_fk_ai_knowle` (`document_id`),
  KEY `ai_knowledge_segment_knowledge_id_0580e7f9_fk_ai_knowledge_id` (`knowledge_id`),
  CONSTRAINT `ai_knowledge_segment_document_id_cd995627_fk_ai_knowle` FOREIGN KEY (`document_id`) REFERENCES `ai_knowledge_document` (`id`),
  CONSTRAINT `ai_knowledge_segment_knowledge_id_0580e7f9_fk_ai_knowledge_id` FOREIGN KEY (`knowledge_id`) REFERENCES `ai_knowledge` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_knowledge_segment
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_model
-- ----------------------------
DROP TABLE IF EXISTS `ai_model`;
CREATE TABLE `ai_model` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(64) NOT NULL COMMENT '模型名字',
  `sort` int NOT NULL COMMENT '排序',
  `status` smallint NOT NULL COMMENT '状态',
  `platform` varchar(32) NOT NULL COMMENT '模型平台',
  `model` varchar(64) NOT NULL COMMENT '模型标识',
  `temperature` double DEFAULT NULL COMMENT '温度参数',
  `max_tokens` int DEFAULT NULL COMMENT '单条回复的最大 Token 数量',
  `max_contexts` int DEFAULT NULL COMMENT '上下文的最大 Message 数量',
  `key_id` bigint NOT NULL COMMENT 'API 秘钥编号',
  `model_type` varchar(32) DEFAULT NULL COMMENT '模型类型',
  PRIMARY KEY (`id`),
  KEY `ai_model_key_id_d9a4647b_fk_ai_api_key_id` (`key_id`),
  CONSTRAINT `ai_model_key_id_d9a4647b_fk_ai_api_key_id` FOREIGN KEY (`key_id`) REFERENCES `ai_api_key` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_model
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ai_tool
-- ----------------------------
DROP TABLE IF EXISTS `ai_tool`;
CREATE TABLE `ai_tool` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(128) NOT NULL COMMENT '工具名称',
  `description` varchar(256) DEFAULT NULL COMMENT '工具描述',
  `status` smallint NOT NULL COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of ai_tool
-- ----------------------------
BEGIN;
INSERT INTO `ai_tool` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `description`, `status`) VALUES (1, NULL, 'admin', 'admin', '2025-07-11 03:00:01.307817', '2025-07-11 02:59:52.998735', 0, 'weather_query', '查询指定城市的天气信息', 1);
COMMIT;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (21, 'Can add Token', 6, 'add_token');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (22, 'Can change Token', 6, 'change_token');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (23, 'Can delete Token', 6, 'delete_token');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (24, 'Can view Token', 6, 'view_token');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (25, 'Can add Token', 7, 'add_tokenproxy');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (26, 'Can change Token', 7, 'change_tokenproxy');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (27, 'Can delete Token', 7, 'delete_tokenproxy');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (28, 'Can view Token', 7, 'view_tokenproxy');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (29, 'Can add 字典类型', 8, 'add_dicttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (30, 'Can change 字典类型', 8, 'change_dicttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (31, 'Can delete 字典类型', 8, 'delete_dicttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (32, 'Can view 字典类型', 8, 'view_dicttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (33, 'Can add 菜单元数据', 9, 'add_menumeta');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (34, 'Can change 菜单元数据', 9, 'change_menumeta');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (35, 'Can delete 菜单元数据', 9, 'delete_menumeta');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (36, 'Can view 菜单元数据', 9, 'view_menumeta');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (37, 'Can add 角色管理', 10, 'add_role');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (38, 'Can change 角色管理', 10, 'change_role');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (39, 'Can delete 角色管理', 10, 'delete_role');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (40, 'Can view 角色管理', 10, 'view_role');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (41, 'Can add 部门管理', 11, 'add_dept');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (42, 'Can change 部门管理', 11, 'change_dept');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (43, 'Can delete 部门管理', 11, 'delete_dept');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (44, 'Can view 部门管理', 11, 'view_dept');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (45, 'Can add 用户数据', 12, 'add_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (46, 'Can change 用户数据', 12, 'change_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (47, 'Can delete 用户数据', 12, 'delete_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (48, 'Can view 用户数据', 12, 'view_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (49, 'Can add 字典数据', 13, 'add_dictdata');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (50, 'Can change 字典数据', 13, 'change_dictdata');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (51, 'Can delete 字典数据', 13, 'delete_dictdata');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (52, 'Can view 字典数据', 13, 'view_dictdata');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (53, 'Can add 菜单', 14, 'add_menu');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (54, 'Can change 菜单', 14, 'change_menu');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (55, 'Can delete 菜单', 14, 'delete_menu');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (56, 'Can view 菜单', 14, 'view_menu');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (57, 'Can add 角色权限关联', 15, 'add_rolepermission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (58, 'Can change 角色权限关联', 15, 'change_rolepermission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (59, 'Can delete 角色权限关联', 15, 'delete_rolepermission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (60, 'Can view 角色权限关联', 15, 'view_rolepermission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (61, 'Can add 岗位信息表', 16, 'add_post');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (62, 'Can change 岗位信息表', 16, 'change_post');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (63, 'Can delete 岗位信息表', 16, 'delete_post');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (64, 'Can view 岗位信息表', 16, 'view_post');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (65, 'Can add 系统访问记录', 17, 'add_systemloginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (66, 'Can change 系统访问记录', 17, 'change_systemloginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (67, 'Can delete 系统访问记录', 17, 'delete_systemloginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (68, 'Can view 系统访问记录', 17, 'view_systemloginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (69, 'Can add 系统访问记录', 18, 'add_loginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (70, 'Can change 系统访问记录', 18, 'change_loginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (71, 'Can delete 系统访问记录', 18, 'delete_loginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (72, 'Can view 系统访问记录', 18, 'view_loginlog');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (73, 'Can add AI API 密钥', 19, 'add_aiapikey');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (74, 'Can change AI API 密钥', 19, 'change_aiapikey');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (75, 'Can delete AI API 密钥', 19, 'delete_aiapikey');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (76, 'Can view AI API 密钥', 19, 'view_aiapikey');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (77, 'Can add AI 模型', 20, 'add_aimodel');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (78, 'Can change AI 模型', 20, 'change_aimodel');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (79, 'Can delete AI 模型', 20, 'delete_aimodel');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (80, 'Can view AI 模型', 20, 'view_aimodel');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (81, 'Can add AI 工具', 21, 'add_tool');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (82, 'Can change AI 工具', 21, 'change_tool');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (83, 'Can delete AI 工具', 21, 'delete_tool');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (84, 'Can view AI 工具', 21, 'view_tool');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (85, 'Can add AI 聊天角色', 22, 'add_chatrole');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (86, 'Can change AI 聊天角色', 22, 'change_chatrole');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (87, 'Can delete AI 聊天角色', 22, 'delete_chatrole');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (88, 'Can view AI 聊天角色', 22, 'view_chatrole');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (89, 'Can add AI 聊天消息', 23, 'add_chatmessage');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (90, 'Can change AI 聊天消息', 23, 'change_chatmessage');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (91, 'Can delete AI 聊天消息', 23, 'delete_chatmessage');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (92, 'Can view AI 聊天消息', 23, 'view_chatmessage');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (93, 'Can add AI 聊天对话', 24, 'add_chatconversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (94, 'Can change AI 聊天对话', 24, 'change_chatconversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (95, 'Can delete AI 聊天对话', 24, 'delete_chatconversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (96, 'Can view AI 聊天对话', 24, 'view_chatconversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (97, 'Can add AI 知识库', 25, 'add_knowledge');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (98, 'Can change AI 知识库', 25, 'change_knowledge');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (99, 'Can delete AI 知识库', 25, 'delete_knowledge');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (100, 'Can view AI 知识库', 25, 'view_knowledge');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (101, 'Can add AI 知识库文档', 26, 'add_knowledgedocument');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (102, 'Can change AI 知识库文档', 26, 'change_knowledgedocument');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (103, 'Can delete AI 知识库文档', 26, 'delete_knowledgedocument');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (104, 'Can view AI 知识库文档', 26, 'view_knowledgedocument');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (105, 'Can add AI 知识库分段', 27, 'add_knowledgesegment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (106, 'Can change AI 知识库分段', 27, 'change_knowledgesegment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (107, 'Can delete AI 知识库分段', 27, 'delete_knowledgesegment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (108, 'Can view AI 知识库分段', 27, 'view_knowledgesegment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (109, 'Can add AI 绘画表', 28, 'add_image');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (110, 'Can change AI 绘画表', 28, 'change_image');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (111, 'Can delete AI 绘画表', 28, 'delete_image');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (112, 'Can view AI 绘画表', 28, 'view_image');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (113, 'Can add AI 绘画表', 28, 'add_drawing');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (114, 'Can change AI 绘画表', 28, 'change_drawing');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (115, 'Can delete AI 绘画表', 28, 'delete_drawing');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (116, 'Can view AI 绘画表', 28, 'view_drawing');
COMMIT;

-- ----------------------------
-- Table structure for authtoken_token
-- ----------------------------
DROP TABLE IF EXISTS `authtoken_token`;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_system_users_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of authtoken_token
-- ----------------------------
BEGIN;
INSERT INTO `authtoken_token` (`key`, `created`, `user_id`) VALUES ('051c7a195ddd849fc66da67c3388cf6da13be332', '2025-07-01 06:34:35.934686', 2);
INSERT INTO `authtoken_token` (`key`, `created`, `user_id`) VALUES ('a81000067ed9733ad445f31219d2f0999a6fe6c2', '2025-06-29 13:10:31.766845', 1);
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_system_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_system_users_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (19, 'ai', 'aiapikey');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (20, 'ai', 'aimodel');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (24, 'ai', 'chatconversation');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (23, 'ai', 'chatmessage');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (22, 'ai', 'chatrole');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (28, 'ai', 'drawing');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (25, 'ai', 'knowledge');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (26, 'ai', 'knowledgedocument');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (27, 'ai', 'knowledgesegment');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (21, 'ai', 'tool');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (6, 'authtoken', 'token');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (7, 'authtoken', 'tokenproxy');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (11, 'system', 'dept');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (13, 'system', 'dictdata');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (8, 'system', 'dicttype');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (18, 'system', 'loginlog');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (14, 'system', 'menu');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (9, 'system', 'menumeta');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (16, 'system', 'post');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (10, 'system', 'role');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (15, 'system', 'rolepermission');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (17, 'system', 'systemloginlog');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (12, 'system', 'user');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (80, 'contenttypes', '0001_initial', '2025-07-03 08:43:50.800575');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (81, 'contenttypes', '0002_remove_content_type_name', '2025-07-03 08:43:50.802755');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (82, 'auth', '0001_initial', '2025-07-03 08:43:50.804008');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (83, 'auth', '0002_alter_permission_name_max_length', '2025-07-03 08:43:50.805150');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (84, 'auth', '0003_alter_user_email_max_length', '2025-07-03 08:43:50.806629');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (85, 'auth', '0004_alter_user_username_opts', '2025-07-03 08:43:50.807732');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (86, 'auth', '0005_alter_user_last_login_null', '2025-07-03 08:43:50.808717');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (87, 'auth', '0006_require_contenttypes_0002', '2025-07-03 08:43:50.809664');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (88, 'auth', '0007_alter_validators_add_error_messages', '2025-07-03 08:43:50.810639');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (89, 'auth', '0008_alter_user_username_max_length', '2025-07-03 08:43:50.811612');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (90, 'auth', '0009_alter_user_last_name_max_length', '2025-07-03 08:43:50.812666');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (91, 'auth', '0010_alter_group_name_max_length', '2025-07-03 08:43:50.813459');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (92, 'auth', '0011_update_proxy_permissions', '2025-07-03 08:43:50.814294');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (93, 'auth', '0012_alter_user_first_name_max_length', '2025-07-03 08:43:50.815294');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (94, 'system', '0001_initial', '2025-07-03 08:43:50.815957');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (95, 'admin', '0001_initial', '2025-07-03 08:43:50.816615');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (96, 'admin', '0002_logentry_remove_auto_add', '2025-07-03 08:43:50.817213');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (97, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-03 08:43:50.817800');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (98, 'authtoken', '0001_initial', '2025-07-03 08:43:50.818352');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (99, 'authtoken', '0002_auto_20160226_1747', '2025-07-03 08:43:50.818924');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (100, 'authtoken', '0003_tokenproxy', '2025-07-03 08:43:50.819477');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (101, 'authtoken', '0004_alter_tokenproxy_options', '2025-07-03 08:43:50.820040');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (102, 'sessions', '0001_initial', '2025-07-03 08:43:50.820534');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (110, 'ai', '0001_initial', '2025-07-11 07:44:40.725265');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (111, 'system', '0002_alter_dept_creator_alter_dept_is_deleted_and_more', '2025-07-11 07:44:40.728073');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (112, 'ai', '0002_alter_chatrole_knowledge_alter_chatrole_tools', '2025-07-16 03:18:08.594750');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (113, 'ai', '0003_aimodel_model_type', '2025-07-16 03:18:08.665002');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (116, 'ai', '0004_alter_chatconversation_model_id_and_more', '2025-07-17 07:07:43.784691');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (117, 'ai', '0005_image', '2025-07-21 03:06:14.168313');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (118, 'ai', '0006_rename_image_drawing_alter_drawing_table', '2025-07-21 13:24:36.556882');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for system_dept
-- ----------------------------
DROP TABLE IF EXISTS `system_dept`;
CREATE TABLE `system_dept` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(100) NOT NULL,
  `status` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `sort` int NOT NULL,
  `leader` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `remark` longtext NOT NULL,
  `pid_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_dept_pid_id_a6a3940d_fk_system_dept_id` (`pid_id`),
  CONSTRAINT `system_dept_pid_id_a6a3940d_fk_system_dept_id` FOREIGN KEY (`pid_id`) REFERENCES `system_dept` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_dept
-- ----------------------------
BEGIN;
INSERT INTO `system_dept` (`id`, `creator`, `modifier`, `update_time`, `is_deleted`, `name`, `status`, `create_time`, `sort`, `leader`, `phone`, `email`, `remark`, `pid_id`) VALUES (2, '', '', '2025-06-30 08:49:38.209122', 0, '晨泽科技', 1, '2025-06-30 08:49:38.209321', 0, NULL, NULL, NULL, '', NULL);
INSERT INTO `system_dept` (`id`, `creator`, `modifier`, `update_time`, `is_deleted`, `name`, `status`, `create_time`, `sort`, `leader`, `phone`, `email`, `remark`, `pid_id`) VALUES (5, 'admin', 'admin', '2025-06-30 09:30:57.724313', 0, '深圳总公司', 1, '2025-06-30 09:16:06.013414', 1, NULL, NULL, NULL, '', 2);
INSERT INTO `system_dept` (`id`, `creator`, `modifier`, `update_time`, `is_deleted`, `name`, `status`, `create_time`, `sort`, `leader`, `phone`, `email`, `remark`, `pid_id`) VALUES (6, 'admin', 'admin', '2025-06-30 09:31:08.967740', 0, '长沙分公司', 1, '2025-06-30 09:23:05.679078', 2, NULL, NULL, NULL, '', 2);
INSERT INTO `system_dept` (`id`, `creator`, `modifier`, `update_time`, `is_deleted`, `name`, `status`, `create_time`, `sort`, `leader`, `phone`, `email`, `remark`, `pid_id`) VALUES (7, 'admin', 'admin', '2025-06-30 09:30:50.715801', 0, '研发部门', 1, '2025-06-30 09:30:50.715897', 1, NULL, NULL, NULL, '', 5);
INSERT INTO `system_dept` (`id`, `creator`, `modifier`, `update_time`, `is_deleted`, `name`, `status`, `create_time`, `sort`, `leader`, `phone`, `email`, `remark`, `pid_id`) VALUES (8, 'xj', 'xj', '2025-07-02 13:05:36.853105', 0, '测试权限', 1, '2025-07-02 13:05:36.853223', 5, NULL, NULL, NULL, '', 6);
COMMIT;

-- ----------------------------
-- Table structure for system_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `system_dict_data`;
CREATE TABLE `system_dict_data` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `sort` int NOT NULL,
  `label` varchar(100) NOT NULL,
  `value` varchar(100) NOT NULL,
  `status` int NOT NULL,
  `color_type` varchar(100) NOT NULL,
  `css_class` varchar(100) NOT NULL,
  `dict_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_dict_data_dict_type_id_6db93fa6_fk_system_dict_type_id` (`dict_type_id`),
  CONSTRAINT `system_dict_data_dict_type_id_6db93fa6_fk_system_dict_type_id` FOREIGN KEY (`dict_type_id`) REFERENCES `system_dict_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_dict_data
-- ----------------------------
BEGIN;
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (2, NULL, NULL, NULL, '2025-07-15 02:08:22.996739', '2025-07-15 02:08:22.996764', 0, 1, '聊天', '1', 1, '', '', 2);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (3, NULL, NULL, NULL, '2025-07-15 02:08:53.538018', '2025-07-15 02:08:53.538037', 0, 2, '图像', '2', 1, '', '', 2);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (4, NULL, NULL, NULL, '2025-07-15 02:10:16.041575', '2025-07-15 02:10:16.041631', 0, 3, '音频', '3', 1, '', '', 2);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (5, NULL, NULL, NULL, '2025-07-15 02:10:42.061733', '2025-07-15 02:10:42.061767', 0, 4, '视频', '4', 1, '', '', 2);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (6, NULL, NULL, NULL, '2025-07-15 02:10:55.771116', '2025-07-15 02:10:55.771147', 0, 5, '向量', '5', 1, '', '', 2);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (7, NULL, NULL, NULL, '2025-07-15 02:11:06.731014', '2025-07-15 02:11:06.731053', 0, 6, '重排', '6', 1, '', '', 2);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (8, NULL, NULL, NULL, '2025-07-16 02:29:08.437533', '2025-07-16 02:29:08.437570', 0, 0, 'OpenAI 微软', 'AzureOpenAI', 1, '', '', 3);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (9, NULL, NULL, NULL, '2025-07-16 02:29:22.498781', '2025-07-16 02:29:22.498808', 0, 2, 'OpenAI', 'OpenAI', 1, '', '', 3);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (10, NULL, NULL, NULL, '2025-07-16 02:29:34.825738', '2025-07-16 02:29:34.825757', 0, 3, 'Ollama', 'Ollama', 1, '', '', 3);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (11, NULL, NULL, NULL, '2025-07-16 02:29:53.315661', '2025-07-16 02:29:53.315704', 0, 5, '通义千问', 'TongYi', 1, '', '', 3);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (12, NULL, NULL, NULL, '2025-07-16 02:30:08.979412', '2025-07-16 02:30:08.979441', 0, 7, 'DeepSeek', 'DeepSeek', 1, '', '', 3);
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (13, NULL, NULL, NULL, '2025-07-16 02:30:44.780200', '2025-07-16 02:30:44.780246', 0, 9, '字节豆包', 'DouBao', 1, '', '', 3);
COMMIT;

-- ----------------------------
-- Table structure for system_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `system_dict_type`;
CREATE TABLE `system_dict_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(100) NOT NULL,
  `value` varchar(100) NOT NULL,
  `status` int NOT NULL,
  `deleted_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_dict_type_type_b3b2d8f5` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_dict_type
-- ----------------------------
BEGIN;
INSERT INTO `system_dict_type` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `value`, `status`, `deleted_time`) VALUES (2, NULL, NULL, NULL, '2025-07-15 02:04:51.990898', '2025-07-15 02:04:51.990974', 0, 'AI 模型类型', 'ai_model_type', 1, NULL);
INSERT INTO `system_dict_type` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `value`, `status`, `deleted_time`) VALUES (3, NULL, NULL, NULL, '2025-07-16 02:12:33.095597', '2025-07-16 02:12:33.095634', 0, 'AI 模型平台', 'ai_platform', 1, NULL);
COMMIT;

-- ----------------------------
-- Table structure for system_login_log
-- ----------------------------
DROP TABLE IF EXISTS `system_login_log`;
CREATE TABLE `system_login_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `username` varchar(50) NOT NULL COMMENT '用户账号',
  `result` int NOT NULL COMMENT '登录结果',
  `user_ip` varchar(50) NOT NULL COMMENT '用户 IP',
  `user_agent` varchar(512) NOT NULL COMMENT '浏览器 UA',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_login_log
-- ----------------------------
BEGIN;
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (1, NULL, NULL, NULL, '2025-07-02 08:36:05.218015', '2025-07-02 08:36:05.218025', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (2, NULL, NULL, NULL, '2025-07-02 08:41:15.420196', '2025-07-02 08:41:15.420216', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (3, NULL, NULL, NULL, '2025-07-02 08:43:11.563684', '2025-07-02 08:43:11.563695', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (4, NULL, NULL, NULL, '2025-07-02 08:47:39.539226', '2025-07-02 08:47:39.539238', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (5, NULL, NULL, NULL, '2025-07-02 08:49:26.983766', '2025-07-02 08:49:26.983779', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (6, NULL, NULL, NULL, '2025-07-02 08:51:07.304242', '2025-07-02 08:51:07.304256', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (7, NULL, NULL, NULL, '2025-07-02 08:52:26.595426', '2025-07-02 08:52:26.595437', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (8, NULL, NULL, NULL, '2025-07-02 08:52:50.451542', '2025-07-02 08:52:50.451553', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (9, NULL, NULL, NULL, '2025-07-02 08:55:57.125928', '2025-07-02 08:55:57.125936', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (10, NULL, NULL, NULL, '2025-07-02 08:57:03.005378', '2025-07-02 08:57:03.005388', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (11, NULL, NULL, NULL, '2025-07-02 08:57:47.575085', '2025-07-02 08:57:47.575095', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (12, NULL, NULL, NULL, '2025-07-02 09:16:09.528323', '2025-07-02 09:16:09.528338', 0, 'admin', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (13, NULL, NULL, NULL, '2025-07-03 01:56:33.628362', '2025-07-03 01:56:33.628383', 0, 'admin', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (14, NULL, NULL, NULL, '2025-07-03 09:03:55.601317', '2025-07-03 09:03:55.601325', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (15, NULL, NULL, NULL, '2025-07-04 05:48:38.799378', '2025-07-04 05:48:38.799423', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (16, NULL, NULL, NULL, '2025-07-04 09:41:07.394602', '2025-07-04 09:41:07.394619', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (17, NULL, NULL, NULL, '2025-07-04 14:46:34.812031', '2025-07-04 14:46:34.812041', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (18, NULL, NULL, NULL, '2025-07-04 14:48:20.347506', '2025-07-04 14:48:20.347516', 0, 'admin', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (19, NULL, NULL, NULL, '2025-07-07 01:54:21.365157', '2025-07-07 01:54:21.365182', 0, 'admin', 1, '58.253.108.151', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (20, NULL, NULL, NULL, '2025-07-08 06:36:25.339783', '2025-07-08 06:36:25.339808', 0, 'admin', 1, '218.26.179.153', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (21, NULL, NULL, NULL, '2025-07-08 07:19:08.737686', '2025-07-08 07:19:08.737715', 0, 'admin', 1, '61.52.19.38', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (22, NULL, NULL, NULL, '2025-07-09 13:06:01.563924', '2025-07-09 13:06:01.563949', 0, 'admin', 1, '27.18.200.216', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (23, NULL, NULL, NULL, '2025-07-10 06:02:45.214431', '2025-07-10 06:02:45.214459', 0, 'admin', 1, '124.239.167.133', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (24, NULL, NULL, NULL, '2025-07-13 03:32:10.322595', '2025-07-13 03:32:10.322619', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (25, NULL, NULL, NULL, '2025-07-13 03:32:48.534087', '2025-07-13 03:32:48.534111', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (26, NULL, NULL, NULL, '2025-07-13 06:04:33.978627', '2025-07-13 06:04:33.978652', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (27, NULL, NULL, NULL, '2025-07-13 06:45:32.348375', '2025-07-13 06:45:32.348401', 0, 'admin', 1, '58.252.18.17', 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (28, NULL, NULL, NULL, '2025-07-13 07:14:15.991829', '2025-07-13 07:14:15.991861', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (29, NULL, NULL, NULL, '2025-07-13 08:02:06.195133', '2025-07-13 08:02:06.195157', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (30, NULL, NULL, NULL, '2025-07-13 11:00:18.291251', '2025-07-13 11:00:18.291286', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (31, NULL, NULL, NULL, '2025-07-14 07:02:26.619850', '2025-07-14 07:02:26.619886', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (32, NULL, NULL, NULL, '2025-07-14 08:56:06.374062', '2025-07-14 08:56:06.374087', 0, 'admin', 1, '222.86.200.62', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (33, NULL, NULL, NULL, '2025-07-14 09:04:22.905904', '2025-07-14 09:04:22.905930', 0, 'chenze', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (34, NULL, NULL, NULL, '2025-07-14 09:43:28.019354', '2025-07-14 09:43:28.019380', 0, 'admin', 1, '61.141.94.108', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (35, NULL, NULL, NULL, '2025-07-14 14:59:40.385678', '2025-07-14 14:59:40.385702', 0, 'chenze', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (36, NULL, NULL, NULL, '2025-07-16 07:47:47.688065', '2025-07-16 07:47:47.688090', 0, 'admin', 1, '27.18.26.39', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (37, NULL, NULL, NULL, '2025-07-16 12:47:45.533242', '2025-07-16 12:47:45.533267', 0, 'admin', 1, '14.105.95.31', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (38, NULL, NULL, NULL, '2025-07-17 02:33:39.972092', '2025-07-17 02:33:39.972117', 0, 'admin', 1, '122.238.20.188', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (39, NULL, NULL, NULL, '2025-07-17 07:55:56.389269', '2025-07-17 07:55:56.389295', 0, 'admin', 1, '223.69.189.135', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (40, NULL, NULL, NULL, '2025-07-18 09:19:39.271509', '2025-07-18 09:19:39.271534', 0, 'admin', 1, '117.65.251.87', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (41, NULL, NULL, NULL, '2025-07-19 17:10:47.944310', '2025-07-19 17:10:47.944337', 0, 'admin', 1, '124.240.8.107', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (42, NULL, NULL, NULL, '2025-07-20 06:47:16.759364', '2025-07-20 06:47:16.759389', 0, 'admin', 1, '14.145.14.107', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (43, NULL, NULL, NULL, '2025-07-21 01:09:42.835046', '2025-07-21 01:09:42.835072', 0, 'admin', 1, '36.21.129.200', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (44, NULL, NULL, NULL, '2025-07-21 01:24:00.631670', '2025-07-21 01:24:00.631696', 0, 'admin', 1, '202.194.96.218', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (45, NULL, NULL, NULL, '2025-07-21 09:23:17.845534', '2025-07-21 09:23:17.845559', 0, 'admin', 1, '156.59.13.8', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (46, NULL, NULL, NULL, '2025-07-21 17:47:31.110733', '2025-07-21 17:47:31.110758', 0, 'admin', 1, '13.158.37.196', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (47, NULL, NULL, NULL, '2025-07-22 01:18:41.456145', '2025-07-22 01:18:41.456169', 0, 'admin', 1, '14.145.14.107', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (48, NULL, NULL, NULL, '2025-07-22 01:23:45.495125', '2025-07-22 01:23:45.495151', 0, 'admin', 1, '36.40.129.142', 'Mozilla/5.0 (Linux; Android 15; V2366GA Build/AP3A.240905.015.A1_MOD1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.63 Mobile Safari/537.36 XWEB/1380045 MMWEBSDK/20250503 MMWEBID/4192 MicroMessenger/8.0.61.2880(0x28003D50) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (49, NULL, NULL, NULL, '2025-07-22 01:24:43.971086', '2025-07-22 01:24:43.971113', 0, 'admin', 1, '223.104.39.175', 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.61(0x18003d2e) NetType/4G Language/zh_CN');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (50, NULL, NULL, NULL, '2025-07-22 01:45:44.385996', '2025-07-22 01:45:44.386021', 0, 'admin', 1, '223.104.42.131', 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.59(0x18003b2e) NetType/4G Language/zh_CN');
COMMIT;

-- ----------------------------
-- Table structure for system_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_menu`;
CREATE TABLE `system_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(100) NOT NULL,
  `status` int NOT NULL,
  `type` varchar(20) NOT NULL,
  `path` varchar(200) NOT NULL,
  `component` varchar(200) NOT NULL,
  `auth_code` varchar(100) NOT NULL,
  `pid_id` bigint DEFAULT NULL,
  `meta_id` bigint NOT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `meta_id` (`meta_id`),
  KEY `system_menu_pid_id_94c9bb14_fk_system_menu_id` (`pid_id`),
  CONSTRAINT `system_menu_meta_id_3c0f37de_fk_system_menu_meta_id` FOREIGN KEY (`meta_id`) REFERENCES `system_menu_meta` (`id`),
  CONSTRAINT `system_menu_pid_id_94c9bb14_fk_system_menu_id` FOREIGN KEY (`pid_id`) REFERENCES `system_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_menu
-- ----------------------------
BEGIN;
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (1, NULL, NULL, 'admin', '2025-07-01 09:45:35.225930', '2025-06-30 09:35:21.372555', 0, '概览', 1, 'menu', '/workspace', '/dashboard/workspace/index', '', NULL, 1, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (2, NULL, NULL, 'admin', '2025-07-11 02:32:24.373705', '2025-06-30 12:37:55.656233', 0, 'System', 1, 'catalog', '/system', '', '', NULL, 2, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (3, NULL, NULL, 'admin', '2025-07-02 03:49:50.551599', '2025-06-30 12:38:52.398094', 0, 'SystemMenu', 1, 'menu', '/system/menu', '/system/menu/list', '', 2, 3, 10);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (4, NULL, NULL, 'admin', '2025-07-01 08:11:00.187470', '2025-06-30 12:57:14.866495', 0, 'SystemMenuCreate', 1, 'button', '', '', 'system:menu:create', 3, 4, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (5, NULL, NULL, 'admin', '2025-07-01 08:12:04.836586', '2025-06-30 12:57:40.728694', 0, 'SystemMenuEdit', 1, 'button', '', '', 'system:menu:edit', 3, 5, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (6, NULL, NULL, 'admin', '2025-07-01 08:12:17.723905', '2025-06-30 12:58:05.562477', 0, 'SystemMenuDelete', 1, 'button', '', '', 'system:menu:delete', 3, 6, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (7, NULL, NULL, 'admin', '2025-07-02 03:49:42.209946', '2025-06-30 12:58:55.893906', 0, 'SystemDept', 1, 'menu', '/system/dept', '/system/dept/list', '', 2, 7, 20);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (8, NULL, NULL, NULL, '2025-06-30 12:59:18.313868', '2025-06-30 12:59:18.313943', 0, 'SystemDeptCreate', 1, 'button', '', '', 'system:dept:create', 7, 8, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (9, NULL, NULL, NULL, '2025-06-30 12:59:45.455554', '2025-06-30 12:59:45.455621', 0, 'SystemDeptEdit', 1, 'button', '', '', 'system:dept:edit', 7, 9, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (10, NULL, NULL, NULL, '2025-06-30 13:00:27.836789', '2025-06-30 13:00:27.836845', 0, 'SystemDeptDelete', 1, 'button', '', '', 'system:dept:delete', 7, 10, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (12, NULL, NULL, 'admin', '2025-07-10 04:09:58.745714', '2025-06-30 14:14:57.815188', 0, 'About', 1, 'menu', '/about', '_core/about/index', '', NULL, 12, 80);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (13, NULL, 'admin', 'admin', '2025-07-10 04:10:06.189493', '2025-06-30 14:17:50.344905', 0, 'Project', 1, 'catalog', '/django-vue3-admin', '', '', NULL, 13, 70);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (14, NULL, 'admin', 'admin', '2025-07-06 16:01:45.924656', '2025-06-30 14:23:46.754306', 0, 'VbenDocument', 1, 'embedded', '/django-vue3-admin/document', 'IFrameView', '', 13, 14, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (15, NULL, 'admin', 'admin', '2025-07-01 08:10:19.878461', '2025-07-01 08:10:19.878496', 0, '查询', 1, 'button', '', '', 'system:menu:query', 3, 15, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (16, NULL, 'admin', 'admin', '2025-07-01 08:17:08.227740', '2025-07-01 08:17:08.227775', 0, '查询', 1, 'button', '', '', 'system:dept:query', 7, 16, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (17, NULL, 'admin', 'admin', '2025-07-01 09:43:54.210777', '2025-07-01 09:43:54.210831', 0, '分析页', 1, 'menu', '/analytics', '/dashboard/analytics/index', '', 1, 17, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (18, NULL, 'admin', 'admin', '2025-07-01 09:44:30.417928', '2025-07-01 09:44:30.417975', 0, '工作台', 1, 'menu', '/workspace', '/dashboard/workspace/index', '', 1, 18, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (24, NULL, NULL, 'admin', '2025-07-02 03:49:33.296190', '2025-07-02 03:46:26.079890', 0, 'Role', 1, 'menu', '/system/role', '/system/role/list', '', 2, 24, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (25, NULL, NULL, NULL, '2025-07-02 03:46:26.082994', '2025-07-02 03:46:26.082999', 0, 'RoleCreate', 1, 'button', '', '', 'system:role:create', 24, 25, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (26, NULL, NULL, NULL, '2025-07-02 03:46:26.086131', '2025-07-02 03:46:26.086135', 0, 'RoleEdit', 1, 'button', '', '', 'system:role:edit', 24, 26, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (27, NULL, NULL, NULL, '2025-07-02 03:46:26.089128', '2025-07-02 03:46:26.089133', 0, 'RoleDelete', 1, 'button', '', '', 'system:role:delete', 24, 27, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (28, NULL, NULL, NULL, '2025-07-02 03:46:26.091868', '2025-07-02 03:46:26.091875', 0, 'RoleQuery', 1, 'button', '', '', 'system:role:query', 24, 28, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (29, NULL, NULL, 'admin', '2025-07-02 03:49:23.672651', '2025-07-02 03:48:59.853957', 0, 'User', 1, 'menu', '/system/user', '/system/user/list', '', 2, 29, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (30, NULL, NULL, NULL, '2025-07-02 03:48:59.858809', '2025-07-02 03:48:59.858814', 0, 'UserCreate', 1, 'button', '', '', 'system:user:create', 29, 30, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (31, NULL, NULL, NULL, '2025-07-02 03:48:59.862787', '2025-07-02 03:48:59.862791', 0, 'UserEdit', 1, 'button', '', '', 'system:user:edit', 29, 31, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (32, NULL, NULL, NULL, '2025-07-02 03:48:59.866249', '2025-07-02 03:48:59.866258', 0, 'UserDelete', 1, 'button', '', '', 'system:user:delete', 29, 32, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (33, NULL, NULL, NULL, '2025-07-02 03:48:59.868177', '2025-07-02 03:48:59.868186', 0, 'UserQuery', 1, 'button', '', '', 'system:user:query', 29, 33, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (34, NULL, NULL, 'admin', '2025-07-02 03:53:28.894059', '2025-07-02 03:51:23.825538', 0, 'Post', 1, 'menu', '/system/post', '/system/post/list', '', 2, 34, 30);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (35, NULL, NULL, NULL, '2025-07-02 03:51:23.828931', '2025-07-02 03:51:23.828935', 0, 'PostQuery', 1, 'button', '', '', 'system:post:query', 34, 35, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (36, NULL, NULL, NULL, '2025-07-02 03:51:23.832181', '2025-07-02 03:51:23.832186', 0, 'PostCreate', 1, 'button', '', '', 'system:post:create', 34, 36, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (37, NULL, NULL, NULL, '2025-07-02 03:51:23.835777', '2025-07-02 03:51:23.835785', 0, 'PostEdit', 1, 'button', '', '', 'system:post:edit', 34, 37, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (38, NULL, NULL, NULL, '2025-07-02 03:51:23.838671', '2025-07-02 03:51:23.838678', 0, 'PostDelete', 1, 'button', '', '', 'system:post:delete', 34, 38, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (39, NULL, NULL, 'admin', '2025-07-02 09:08:57.619519', '2025-07-02 03:51:34.552870', 0, 'dict_type', 1, 'menu', '/system/dict_type', '/system/dict_type/list', '', 2, 39, 35);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (40, NULL, NULL, NULL, '2025-07-02 03:51:34.557464', '2025-07-02 03:51:34.557491', 0, 'DicttypeQuery', 1, 'button', '', '', 'system:dict_type:query', 39, 40, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (41, NULL, NULL, NULL, '2025-07-02 03:51:34.561909', '2025-07-02 03:51:34.561924', 0, 'DicttypeCreate', 1, 'button', '', '', 'system:dict_type:create', 39, 41, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (42, NULL, NULL, NULL, '2025-07-02 03:51:34.565632', '2025-07-02 03:51:34.565648', 0, 'DicttypeEdit', 1, 'button', '', '', 'system:dict_type:edit', 39, 42, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (43, NULL, NULL, NULL, '2025-07-02 03:51:34.570675', '2025-07-02 03:51:34.570692', 0, 'DicttypeDelete', 1, 'button', '', '', 'system:dict_type:delete', 39, 43, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (44, NULL, NULL, 'admin', '2025-07-02 04:26:19.030908', '2025-07-02 03:51:44.164226', 0, 'Dictdata', 1, 'menu', '/system/dict_data', '/system/dict_data/list', '', 2, 44, 40);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (45, NULL, NULL, NULL, '2025-07-02 03:51:44.167519', '2025-07-02 03:51:44.167524', 0, 'DictdataQuery', 1, 'button', '', '', 'system:dict_data:query', 44, 45, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (46, NULL, NULL, NULL, '2025-07-02 03:51:44.170675', '2025-07-02 03:51:44.170679', 0, 'DictdataCreate', 1, 'button', '', '', 'system:dict_data:create', 44, 46, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (47, NULL, NULL, NULL, '2025-07-02 03:51:44.174695', '2025-07-02 03:51:44.174701', 0, 'DictdataEdit', 1, 'button', '', '', 'system:dict_data:edit', 44, 47, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (48, NULL, NULL, NULL, '2025-07-02 03:51:44.176427', '2025-07-02 03:51:44.176432', 0, 'DictdataDelete', 1, 'button', '', '', 'system:dict_data:delete', 44, 48, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (49, NULL, NULL, 'admin', '2025-07-02 08:26:04.038796', '2025-07-02 08:02:58.012301', 0, 'loginlog', 1, 'menu', '/system/login_log', '/system/login_log/list', '', 2, 49, 50);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (50, NULL, NULL, NULL, '2025-07-02 08:02:58.016583', '2025-07-02 08:02:58.016587', 0, 'loginlogQuery', 1, 'button', '', '', 'system:login_log:query', 49, 50, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (51, NULL, NULL, NULL, '2025-07-02 08:02:58.020560', '2025-07-02 08:02:58.020564', 0, 'loginlogCreate', 1, 'button', '', '', 'system:login_log:create', 49, 51, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (52, NULL, NULL, NULL, '2025-07-02 08:02:58.023348', '2025-07-02 08:02:58.023354', 0, 'loginlogEdit', 1, 'button', '', '', 'system:login_log:edit', 49, 52, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (53, NULL, NULL, NULL, '2025-07-02 08:02:58.024971', '2025-07-02 08:02:58.024976', 0, 'loginlogDelete', 1, 'button', '', '', 'system:login_log:delete', 49, 53, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (54, NULL, 'admin', 'admin', '2025-07-06 16:02:20.555780', '2025-07-06 16:00:22.966211', 0, 'VbenGithub', 1, 'embedded', '/django-vue3-admin/github', '', '', 13, 54, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (55, NULL, 'admin', 'admin', '2025-07-11 02:32:33.717179', '2025-07-10 03:30:10.283442', 0, 'AI', 1, 'catalog', '/ai', '', '', NULL, 55, 7);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (56, NULL, NULL, 'admin', '2025-07-18 02:33:10.853903', '2025-07-10 03:39:18.821059', 0, 'Aiapikey', 1, 'menu', '/ai/api_key', '/ai/api_key/list', '', 55, 56, 100);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (57, NULL, NULL, NULL, '2025-07-10 03:39:18.825637', '2025-07-10 03:39:18.825643', 0, 'AiapikeyCreate', 1, 'button', '', '', 'ai:ai_api_key:create', 56, 57, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (58, NULL, NULL, NULL, '2025-07-10 03:39:18.832126', '2025-07-10 03:39:18.832131', 0, 'AiapikeyEdit', 1, 'button', '', '', 'ai:ai_api_key:edit', 56, 58, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (59, NULL, NULL, NULL, '2025-07-10 03:39:18.834117', '2025-07-10 03:39:18.834122', 0, 'AiapikeyDelete', 1, 'button', '', '', 'ai:ai_api_key:delete', 56, 59, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (60, NULL, NULL, NULL, '2025-07-10 03:39:18.836444', '2025-07-10 03:39:18.836450', 0, 'AiapikeyQuery', 1, 'button', '', '', 'ai:ai_api_key:query', 56, 60, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (61, NULL, NULL, NULL, '2025-07-10 03:39:18.838099', '2025-07-10 03:39:18.838104', 0, 'AiapikeyQuery', 1, 'button', '', '', 'ai:ai_api_key:import', 56, 61, 4);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (62, NULL, NULL, NULL, '2025-07-10 03:39:18.839823', '2025-07-10 03:39:18.839829', 0, 'AiapikeyQuery', 1, 'button', '', '', 'ai:ai_api_key:export', 56, 62, 5);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (63, NULL, NULL, 'admin', '2025-07-21 06:52:18.169651', '2025-07-11 01:57:27.851292', 0, 'Aimodel', 1, 'menu', '/ai/ai_model', '/ai/ai_model/list', '', 55, 63, 160);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (64, NULL, NULL, NULL, '2025-07-11 01:57:27.855799', '2025-07-11 01:57:27.855804', 0, 'AimodelCreate', 1, 'button', '', '', 'ai:ai_model:create', 63, 64, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (65, NULL, NULL, NULL, '2025-07-11 01:57:27.859356', '2025-07-11 01:57:27.859361', 0, 'AimodelEdit', 1, 'button', '', '', 'ai:ai_model:edit', 63, 65, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (66, NULL, NULL, NULL, '2025-07-11 01:57:27.862433', '2025-07-11 01:57:27.862442', 0, 'AimodelDelete', 1, 'button', '', '', 'ai:ai_model:delete', 63, 66, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (67, NULL, NULL, NULL, '2025-07-11 01:57:27.864381', '2025-07-11 01:57:27.864390', 0, 'AimodelQuery', 1, 'button', '', '', 'ai:ai_model:query', 63, 67, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (68, NULL, NULL, NULL, '2025-07-11 01:57:27.866251', '2025-07-11 01:57:27.866257', 0, 'AimodelQuery', 1, 'button', '', '', 'ai:ai_model:import', 63, 68, 4);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (69, NULL, NULL, NULL, '2025-07-11 01:57:27.867682', '2025-07-11 01:57:27.867687', 0, 'AimodelQuery', 1, 'button', '', '', 'ai:ai_model:export', 63, 69, 5);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (70, NULL, NULL, 'admin', '2025-07-21 06:52:10.397062', '2025-07-11 02:53:20.403093', 0, 'Tool', 1, 'menu', '/ai/tool', '/ai/tool/list', '', 55, 70, 170);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (71, NULL, NULL, NULL, '2025-07-11 02:53:20.407331', '2025-07-11 02:53:20.407336', 0, 'ToolCreate', 1, 'button', '', '', 'ai:tool:create', 70, 71, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (72, NULL, NULL, NULL, '2025-07-11 02:53:20.411591', '2025-07-11 02:53:20.411599', 0, 'ToolEdit', 1, 'button', '', '', 'ai:tool:edit', 70, 72, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (73, NULL, NULL, NULL, '2025-07-11 02:53:20.413324', '2025-07-11 02:53:20.413331', 0, 'ToolDelete', 1, 'button', '', '', 'ai:tool:delete', 70, 73, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (74, NULL, NULL, NULL, '2025-07-11 02:53:20.415196', '2025-07-11 02:53:20.415204', 0, 'ToolQuery', 1, 'button', '', '', 'ai:tool:query', 70, 74, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (75, NULL, NULL, NULL, '2025-07-11 02:53:20.416916', '2025-07-11 02:53:20.416921', 0, 'ToolQuery', 1, 'button', '', '', 'ai:tool:import', 70, 75, 4);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (76, NULL, NULL, NULL, '2025-07-11 02:53:20.418666', '2025-07-11 02:53:20.418672', 0, 'ToolQuery', 1, 'button', '', '', 'ai:tool:export', 70, 76, 5);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (78, NULL, NULL, 'admin', '2025-07-21 06:52:02.996740', '2025-07-15 01:47:21.284552', 0, 'Knowledge', 1, 'menu', '/ai/knowledge', '/ai/knowledge/list', '', 55, 78, 180);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (79, NULL, NULL, NULL, '2025-07-15 01:47:21.287927', '2025-07-15 01:47:21.287938', 0, 'KnowledgeCreate', 1, 'button', '', '', 'ai:knowledge:create', 78, 79, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (80, NULL, NULL, NULL, '2025-07-15 01:47:21.290503', '2025-07-15 01:47:21.290511', 0, 'KnowledgeEdit', 1, 'button', '', '', 'ai:knowledge:edit', 78, 80, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (81, NULL, NULL, NULL, '2025-07-15 01:47:21.292828', '2025-07-15 01:47:21.292834', 0, 'KnowledgeDelete', 1, 'button', '', '', 'ai:knowledge:delete', 78, 81, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (82, NULL, NULL, NULL, '2025-07-15 01:47:21.294333', '2025-07-15 01:47:21.294340', 0, 'KnowledgeQuery', 1, 'button', '', '', 'ai:knowledge:query', 78, 82, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (83, NULL, NULL, NULL, '2025-07-15 01:47:21.296074', '2025-07-15 01:47:21.296080', 0, 'KnowledgeQuery', 1, 'button', '', '', 'ai:knowledge:import', 78, 83, 4);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (84, NULL, NULL, NULL, '2025-07-15 01:47:21.298823', '2025-07-15 01:47:21.298831', 0, 'KnowledgeQuery', 1, 'button', '', '', 'ai:knowledge:export', 78, 84, 5);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (85, NULL, 'admin', 'admin', '2025-07-21 06:52:27.834271', '2025-07-17 02:57:36.901338', 0, 'AI对话', 1, 'menu', '/ai/chat', '/ai/chat/index', '', 55, 85, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (86, NULL, NULL, 'admin', '2025-07-21 06:51:55.270087', '2025-07-18 02:51:28.107276', 0, 'Chatconversation', 1, 'menu', '/ai/chat_conversation', '/ai/chat_conversation/list', '', 55, 86, 190);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (87, NULL, NULL, NULL, '2025-07-18 02:51:28.113765', '2025-07-18 02:51:28.113769', 0, 'ChatconversationCreate', 1, 'button', '', '', 'ai:chat_conversation:create', 86, 87, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (88, NULL, NULL, NULL, '2025-07-18 02:51:28.116167', '2025-07-18 02:51:28.116174', 0, 'ChatconversationEdit', 1, 'button', '', '', 'ai:chat_conversation:edit', 86, 88, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (89, NULL, NULL, NULL, '2025-07-18 02:51:28.118153', '2025-07-18 02:51:28.118158', 0, 'ChatconversationDelete', 1, 'button', '', '', 'ai:chat_conversation:delete', 86, 89, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (90, NULL, NULL, NULL, '2025-07-18 02:51:28.120099', '2025-07-18 02:51:28.120108', 0, 'ChatconversationQuery', 1, 'button', '', '', 'ai:chat_conversation:query', 86, 90, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (91, NULL, NULL, NULL, '2025-07-18 02:51:28.123877', '2025-07-18 02:51:28.123886', 0, 'ChatconversationQuery', 1, 'button', '', '', 'ai:chat_conversation:import', 86, 91, 4);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (92, NULL, NULL, NULL, '2025-07-18 02:51:28.125700', '2025-07-18 02:51:28.125707', 0, 'ChatconversationQuery', 1, 'button', '', '', 'ai:chat_conversation:export', 86, 92, 5);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (93, NULL, NULL, 'admin', '2025-07-21 06:51:46.584942', '2025-07-18 03:39:15.967234', 0, 'Chatmessage', 1, 'menu', '/ai/chat_message', '/ai/chat_message/list', '', 55, 93, 200);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (94, NULL, NULL, NULL, '2025-07-18 03:39:15.975162', '2025-07-18 03:39:15.975191', 0, 'ChatmessageCreate', 1, 'button', '', '', 'ai:chat_message:create', 93, 94, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (95, NULL, NULL, NULL, '2025-07-18 03:39:15.981304', '2025-07-18 03:39:15.981333', 0, 'ChatmessageEdit', 1, 'button', '', '', 'ai:chat_message:edit', 93, 95, 1);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (96, NULL, NULL, NULL, '2025-07-18 03:39:15.987279', '2025-07-18 03:39:15.987305', 0, 'ChatmessageDelete', 1, 'button', '', '', 'ai:chat_message:delete', 93, 96, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (97, NULL, NULL, NULL, '2025-07-18 03:39:15.993846', '2025-07-18 03:39:15.993875', 0, 'ChatmessageQuery', 1, 'button', '', '', 'ai:chat_message:query', 93, 97, 3);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (98, NULL, NULL, NULL, '2025-07-18 03:39:16.000070', '2025-07-18 03:39:16.000096', 0, 'ChatmessageQuery', 1, 'button', '', '', 'ai:chat_message:import', 93, 98, 4);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (99, NULL, NULL, NULL, '2025-07-18 03:39:16.005517', '2025-07-18 03:39:16.005544', 0, 'ChatmessageQuery', 1, 'button', '', '', 'ai:chat_message:export', 93, 99, 5);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (100, NULL, 'admin', 'admin', '2025-07-21 06:55:13.626092', '2025-07-21 06:53:45.364834', 0, 'AI绘画', 1, 'menu', '/ai/drawing', '/ai/drawing/index', '', 55, 100, 2);
COMMIT;

-- ----------------------------
-- Table structure for system_menu_meta
-- ----------------------------
DROP TABLE IF EXISTS `system_menu_meta`;
CREATE TABLE `system_menu_meta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `title` varchar(200) NOT NULL COMMENT '标题',
  `icon` varchar(100) NOT NULL COMMENT '图标',
  `sort` int NOT NULL COMMENT '排序',
  `affix_tab` tinyint(1) NOT NULL COMMENT '固定标签页',
  `badge` varchar(50) NOT NULL COMMENT '徽章文本',
  `badge_type` varchar(20) NOT NULL COMMENT '徽章类型',
  `badge_variants` varchar(20) NOT NULL COMMENT '徽章样式',
  `iframe_src` varchar(200) NOT NULL COMMENT '内嵌页面URL',
  `link` varchar(200) NOT NULL COMMENT '外部链接',
  `hide_children_in_menu` tinyint(1) NOT NULL COMMENT '隐藏子菜单',
  `hide_in_menu` tinyint(1) NOT NULL COMMENT '隐藏菜单',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_menu_meta
-- ----------------------------
BEGIN;
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (1, NULL, NULL, NULL, '2025-07-01 09:45:35.200879', '2025-06-30 09:35:21.346111', 0, 'page.dashboard.title', 'carbon:workspace', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (2, NULL, NULL, NULL, '2025-07-11 02:32:24.369609', '2025-06-30 12:37:55.632666', 0, 'system.title', 'carbon:settings', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (3, NULL, NULL, NULL, '2025-07-02 03:49:50.547348', '2025-06-30 12:38:52.374691', 0, 'system.menu.title', 'carbon:menu', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (4, NULL, NULL, NULL, '2025-07-01 08:11:00.165353', '2025-06-30 12:57:14.842379', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (5, NULL, NULL, NULL, '2025-07-01 08:12:04.811256', '2025-06-30 12:57:40.703715', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (6, NULL, NULL, NULL, '2025-07-01 08:12:17.702120', '2025-06-30 12:58:05.535736', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (7, NULL, NULL, NULL, '2025-07-02 03:49:42.205928', '2025-06-30 12:58:55.867808', 0, 'system.dept.title', 'carbon:container-services', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (8, NULL, NULL, NULL, '2025-06-30 12:59:18.290232', '2025-06-30 12:59:18.290288', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (9, NULL, NULL, NULL, '2025-06-30 12:59:45.429985', '2025-06-30 12:59:45.430037', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (10, NULL, NULL, NULL, '2025-06-30 13:00:27.814988', '2025-06-30 13:00:27.815021', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (11, NULL, NULL, NULL, '2025-06-30 13:00:28.085386', '2025-06-30 13:00:28.085434', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (12, NULL, NULL, NULL, '2025-07-10 04:09:58.741264', '2025-06-30 14:14:57.789248', 0, 'demos.vben.about', 'lucide:copyright', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (13, NULL, NULL, NULL, '2025-07-10 04:10:06.185808', '2025-06-30 14:17:50.320137', 0, 'demos.vben.title', 'carbon:data-center', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (14, NULL, NULL, NULL, '2025-07-06 16:01:45.915788', '2025-06-30 14:23:46.727573', 0, 'demos.vben.document', 'carbon:book', 0, 0, '', '', '', 'https://docs.ywwuzi.cn/', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (15, NULL, NULL, NULL, '2025-07-01 08:10:19.854182', '2025-07-01 08:10:19.854206', 0, '查询', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (16, NULL, NULL, NULL, '2025-07-01 08:17:08.205093', '2025-07-01 08:17:08.205154', 0, '查询', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (17, NULL, NULL, NULL, '2025-07-01 09:43:54.186595', '2025-07-01 09:43:54.186661', 0, '分析页', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (18, NULL, NULL, NULL, '2025-07-01 09:44:30.390568', '2025-07-01 09:44:30.390606', 0, '工作台', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (24, NULL, NULL, NULL, '2025-07-02 03:49:33.292018', '2025-07-02 03:46:26.077742', 0, 'system.role.title', 'carbon:user-role', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (25, NULL, NULL, NULL, '2025-07-02 03:46:26.081633', '2025-07-02 03:46:26.081638', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (26, NULL, NULL, NULL, '2025-07-02 03:46:26.084404', '2025-07-02 03:46:26.084409', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (27, NULL, NULL, NULL, '2025-07-02 03:46:26.087735', '2025-07-02 03:46:26.087740', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (28, NULL, NULL, NULL, '2025-07-02 03:46:26.090462', '2025-07-02 03:46:26.090466', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (29, NULL, NULL, NULL, '2025-07-02 03:49:23.669448', '2025-07-02 03:48:59.851884', 0, 'system.user.title', 'carbon:user', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (30, NULL, NULL, NULL, '2025-07-02 03:48:59.856971', '2025-07-02 03:48:59.856976', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (31, NULL, NULL, NULL, '2025-07-02 03:48:59.860686', '2025-07-02 03:48:59.860690', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (32, NULL, NULL, NULL, '2025-07-02 03:48:59.865043', '2025-07-02 03:48:59.865051', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (33, NULL, NULL, NULL, '2025-07-02 03:48:59.867059', '2025-07-02 03:48:59.867065', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (34, NULL, NULL, NULL, '2025-07-02 03:53:28.890794', '2025-07-02 03:51:23.822427', 0, 'system.post.title', 'carbon:database-postgresql', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (35, NULL, NULL, NULL, '2025-07-02 03:51:23.827526', '2025-07-02 03:51:23.827532', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (36, NULL, NULL, NULL, '2025-07-02 03:51:23.830494', '2025-07-02 03:51:23.830499', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (37, NULL, NULL, NULL, '2025-07-02 03:51:23.833975', '2025-07-02 03:51:23.833979', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (38, NULL, NULL, NULL, '2025-07-02 03:51:23.837625', '2025-07-02 03:51:23.837635', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (39, NULL, NULL, NULL, '2025-07-02 09:08:57.614928', '2025-07-02 03:51:34.549339', 0, 'system.dict_type.title', 'carbon:ibm-cloud-dedicated-host', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (40, NULL, NULL, NULL, '2025-07-02 03:51:34.555305', '2025-07-02 03:51:34.555334', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (41, NULL, NULL, NULL, '2025-07-02 03:51:34.559783', '2025-07-02 03:51:34.559799', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (42, NULL, NULL, NULL, '2025-07-02 03:51:34.563772', '2025-07-02 03:51:34.563784', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (43, NULL, NULL, NULL, '2025-07-02 03:51:34.568238', '2025-07-02 03:51:34.568287', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (44, NULL, NULL, NULL, '2025-07-02 04:26:19.027519', '2025-07-02 03:51:44.161177', 0, 'system.dict_data.title', 'carbon:data-base', 0, 0, '', '', '', '', '', 1, 1);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (45, NULL, NULL, NULL, '2025-07-02 03:51:44.166037', '2025-07-02 03:51:44.166042', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (46, NULL, NULL, NULL, '2025-07-02 03:51:44.169035', '2025-07-02 03:51:44.169040', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (47, NULL, NULL, NULL, '2025-07-02 03:51:44.173431', '2025-07-02 03:51:44.173437', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (48, NULL, NULL, NULL, '2025-07-02 03:51:44.175643', '2025-07-02 03:51:44.175648', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (49, NULL, NULL, NULL, '2025-07-02 08:26:04.032685', '2025-07-02 08:02:58.008889', 0, 'system.login_log.title', 'carbon:catalog', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (50, NULL, NULL, NULL, '2025-07-02 08:02:58.014694', '2025-07-02 08:02:58.014698', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (51, NULL, NULL, NULL, '2025-07-02 08:02:58.018239', '2025-07-02 08:02:58.018243', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (52, NULL, NULL, NULL, '2025-07-02 08:02:58.021897', '2025-07-02 08:02:58.021901', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (53, NULL, NULL, NULL, '2025-07-02 08:02:58.024225', '2025-07-02 08:02:58.024229', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (54, NULL, NULL, NULL, '2025-07-06 16:02:20.548920', '2025-07-06 16:00:22.954337', 0, 'Github', 'mdi:github', 0, 0, '', '', '', '', 'https://github.com/XIE7654/django-vue3-admin', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (55, NULL, NULL, NULL, '2025-07-11 02:32:33.713614', '2025-07-10 03:30:10.278933', 0, 'ai.title', 'carbon:paint-brush', 0, 0, 'new', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (56, NULL, NULL, NULL, '2025-07-18 02:33:10.844515', '2025-07-10 03:39:18.817197', 0, 'ai.api_key.title', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (57, NULL, NULL, NULL, '2025-07-10 03:39:18.823606', '2025-07-10 03:39:18.823616', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (58, NULL, NULL, NULL, '2025-07-10 03:39:18.828374', '2025-07-10 03:39:18.828379', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (59, NULL, NULL, NULL, '2025-07-10 03:39:18.833216', '2025-07-10 03:39:18.833221', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (60, NULL, NULL, NULL, '2025-07-10 03:39:18.835521', '2025-07-10 03:39:18.835532', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (61, NULL, NULL, NULL, '2025-07-10 03:39:18.837225', '2025-07-10 03:39:18.837230', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (62, NULL, NULL, NULL, '2025-07-10 03:39:18.839006', '2025-07-10 03:39:18.839011', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (63, NULL, NULL, NULL, '2025-07-21 06:52:18.165051', '2025-07-11 01:57:27.845814', 0, 'ai.ai_model.title', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (64, NULL, NULL, NULL, '2025-07-11 01:57:27.854026', '2025-07-11 01:57:27.854030', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (65, NULL, NULL, NULL, '2025-07-11 01:57:27.857594', '2025-07-11 01:57:27.857598', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (66, NULL, NULL, NULL, '2025-07-11 01:57:27.861280', '2025-07-11 01:57:27.861291', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (67, NULL, NULL, NULL, '2025-07-11 01:57:27.863309', '2025-07-11 01:57:27.863315', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (68, NULL, NULL, NULL, '2025-07-11 01:57:27.865232', '2025-07-11 01:57:27.865238', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (69, NULL, NULL, NULL, '2025-07-11 01:57:27.866966', '2025-07-11 01:57:27.866972', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (70, NULL, NULL, NULL, '2025-07-21 06:52:10.393970', '2025-07-11 02:53:20.398315', 0, 'ai.tool.title', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (71, NULL, NULL, NULL, '2025-07-11 02:53:20.405509', '2025-07-11 02:53:20.405516', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (72, NULL, NULL, NULL, '2025-07-11 02:53:20.410175', '2025-07-11 02:53:20.410180', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (73, NULL, NULL, NULL, '2025-07-11 02:53:20.412480', '2025-07-11 02:53:20.412486', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (74, NULL, NULL, NULL, '2025-07-11 02:53:20.414089', '2025-07-11 02:53:20.414094', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (75, NULL, NULL, NULL, '2025-07-11 02:53:20.416161', '2025-07-11 02:53:20.416166', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (76, NULL, NULL, NULL, '2025-07-11 02:53:20.417594', '2025-07-11 02:53:20.417598', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (77, NULL, NULL, NULL, '2025-07-11 08:46:59.490742', '2025-07-11 08:46:59.490773', 0, 'ai chat', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (78, NULL, NULL, NULL, '2025-07-21 06:52:02.992485', '2025-07-15 01:47:21.274505', 0, 'ai.knowledge.title', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (79, NULL, NULL, NULL, '2025-07-15 01:47:21.286782', '2025-07-15 01:47:21.286794', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (80, NULL, NULL, NULL, '2025-07-15 01:47:21.289159', '2025-07-15 01:47:21.289167', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (81, NULL, NULL, NULL, '2025-07-15 01:47:21.291876', '2025-07-15 01:47:21.291885', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (82, NULL, NULL, NULL, '2025-07-15 01:47:21.293546', '2025-07-15 01:47:21.293551', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (83, NULL, NULL, NULL, '2025-07-15 01:47:21.295133', '2025-07-15 01:47:21.295142', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (84, NULL, NULL, NULL, '2025-07-15 01:47:21.297417', '2025-07-15 01:47:21.297424', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (85, NULL, NULL, NULL, '2025-07-21 06:52:27.830001', '2025-07-17 02:57:36.895879', 0, 'ai.chat.title', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (86, NULL, NULL, NULL, '2025-07-21 06:51:55.266989', '2025-07-18 02:51:28.102110', 0, 'ai.chat_conversation.title', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (87, NULL, NULL, NULL, '2025-07-18 02:51:28.111131', '2025-07-18 02:51:28.111137', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (88, NULL, NULL, NULL, '2025-07-18 02:51:28.115047', '2025-07-18 02:51:28.115055', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (89, NULL, NULL, NULL, '2025-07-18 02:51:28.117163', '2025-07-18 02:51:28.117168', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (90, NULL, NULL, NULL, '2025-07-18 02:51:28.119252', '2025-07-18 02:51:28.119262', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (91, NULL, NULL, NULL, '2025-07-18 02:51:28.123068', '2025-07-18 02:51:28.123074', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (92, NULL, NULL, NULL, '2025-07-18 02:51:28.124912', '2025-07-18 02:51:28.124917', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (93, NULL, NULL, NULL, '2025-07-21 06:51:46.579238', '2025-07-18 03:39:15.959130', 0, 'ai.chat_message.title', '', 0, 0, '', '', '', '', '', 0, 1);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (94, NULL, NULL, NULL, '2025-07-18 03:39:15.970862', '2025-07-18 03:39:15.970899', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (95, NULL, NULL, NULL, '2025-07-18 03:39:15.977961', '2025-07-18 03:39:15.977991', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (96, NULL, NULL, NULL, '2025-07-18 03:39:15.984598', '2025-07-18 03:39:15.984630', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (97, NULL, NULL, NULL, '2025-07-18 03:39:15.990627', '2025-07-18 03:39:15.990654', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (98, NULL, NULL, NULL, '2025-07-18 03:39:15.996695', '2025-07-18 03:39:15.996725', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (99, NULL, NULL, NULL, '2025-07-18 03:39:16.002524', '2025-07-18 03:39:16.002552', 0, 'common.query', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (100, NULL, NULL, NULL, '2025-07-21 06:55:13.618493', '2025-07-21 06:53:45.359449', 0, 'ai.drawing.title', '', 0, 0, '', '', '', '', '', 0, 0);
COMMIT;

-- ----------------------------
-- Table structure for system_post
-- ----------------------------
DROP TABLE IF EXISTS `system_post`;
CREATE TABLE `system_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `code` varchar(64) NOT NULL COMMENT '岗位编码',
  `name` varchar(50) NOT NULL COMMENT '岗位名称',
  `sort` int NOT NULL COMMENT '显示顺序',
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_post
-- ----------------------------
BEGIN;
INSERT INTO `system_post` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `code`, `name`, `sort`, `status`) VALUES (1, NULL, 'admin', 'admin', '2025-07-01 03:56:03.681726', '2025-07-01 03:56:03.681744', 0, 'ceo', '董事长', 1, 1);
INSERT INTO `system_post` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `code`, `name`, `sort`, `status`) VALUES (2, NULL, 'admin', 'admin', '2025-07-01 05:00:40.525740', '2025-07-01 04:40:54.324478', 0, 'se', '项目经理', 2, 1);
INSERT INTO `system_post` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `code`, `name`, `sort`, `status`) VALUES (3, NULL, 'admin', 'admin', '2025-07-01 04:42:13.165649', '2025-07-01 04:42:13.165717', 0, 'hr', '人力资源', 3, 1);
INSERT INTO `system_post` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `code`, `name`, `sort`, `status`) VALUES (4, NULL, 'admin', 'admin', '2025-07-01 04:42:26.454576', '2025-07-01 04:42:26.454633', 0, 'user', '普通员工', 4, 1);
COMMIT;

-- ----------------------------
-- Table structure for system_role
-- ----------------------------
DROP TABLE IF EXISTS `system_role`;
CREATE TABLE `system_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `name` varchar(100) NOT NULL,
  `status` int NOT NULL,
  `sort` int NOT NULL,
  `remark` longtext NOT NULL,
  `code` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_role
-- ----------------------------
BEGIN;
INSERT INTO `system_role` (`id`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `sort`, `remark`, `code`) VALUES (2, NULL, 'admin', '2025-07-03 09:05:32.917555', '2025-06-30 13:43:33.222244', 0, '普通角色', 1, 0, '', 'common');
INSERT INTO `system_role` (`id`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `sort`, `remark`, `code`) VALUES (3, 'admin', 'admin', '2025-07-18 13:20:50.920641', '2025-06-30 14:01:56.403744', 0, '超级管理员', 1, 0, '', 'superAdmin');
COMMIT;

-- ----------------------------
-- Table structure for system_role_permission
-- ----------------------------
DROP TABLE IF EXISTS `system_role_permission`;
CREATE TABLE `system_role_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `create_time` datetime(6) NOT NULL,
  `menu_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_role_permission_menu_id_bf701eaf_fk_system_menu_id` (`menu_id`),
  KEY `system_role_permission_role_id_ca5e9412_fk_system_role_id` (`role_id`),
  CONSTRAINT `system_role_permission_menu_id_bf701eaf_fk_system_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`),
  CONSTRAINT `system_role_permission_role_id_ca5e9412_fk_system_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_role_permission
-- ----------------------------
BEGIN;
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (11, NULL, NULL, NULL, '2025-06-30 13:43:33.270703', 0, '2025-06-30 13:43:33.270782', 2, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (12, NULL, NULL, NULL, '2025-06-30 13:43:33.291714', 0, '2025-06-30 13:43:33.291789', 3, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (13, NULL, NULL, NULL, '2025-06-30 13:43:33.314577', 0, '2025-06-30 13:43:33.314658', 4, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (14, NULL, NULL, NULL, '2025-06-30 13:43:33.335049', 0, '2025-06-30 13:43:33.335102', 5, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (15, NULL, NULL, NULL, '2025-06-30 13:43:33.356238', 0, '2025-06-30 13:43:33.356319', 6, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (16, NULL, NULL, NULL, '2025-06-30 14:01:56.453984', 0, '2025-06-30 14:01:56.454058', 1, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (17, NULL, NULL, NULL, '2025-06-30 14:01:56.476710', 0, '2025-06-30 14:01:56.476815', 2, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (18, NULL, NULL, NULL, '2025-06-30 14:01:56.498562', 0, '2025-06-30 14:01:56.498645', 3, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (19, NULL, NULL, NULL, '2025-06-30 14:01:56.520726', 0, '2025-06-30 14:01:56.520814', 4, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (20, NULL, NULL, NULL, '2025-06-30 14:01:56.543034', 0, '2025-06-30 14:01:56.543141', 5, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (21, NULL, NULL, NULL, '2025-06-30 14:01:56.565546', 0, '2025-06-30 14:01:56.565624', 6, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (22, NULL, NULL, NULL, '2025-06-30 14:01:56.587965', 0, '2025-06-30 14:01:56.588024', 7, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (23, NULL, NULL, NULL, '2025-06-30 14:01:56.610751', 0, '2025-06-30 14:01:56.610849', 8, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (24, NULL, NULL, NULL, '2025-06-30 14:01:56.634161', 0, '2025-06-30 14:01:56.634243', 9, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (25, NULL, NULL, NULL, '2025-06-30 14:01:56.657691', 0, '2025-06-30 14:01:56.657753', 10, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (29, NULL, NULL, NULL, '2025-07-01 07:57:14.090386', 0, '2025-07-01 07:57:14.090399', 7, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (30, NULL, NULL, NULL, '2025-07-01 07:57:25.893132', 0, '2025-07-01 07:57:25.893185', 12, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (31, NULL, NULL, NULL, '2025-07-01 07:57:25.893198', 0, '2025-07-01 07:57:25.893211', 13, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (32, NULL, NULL, NULL, '2025-07-01 07:57:25.893223', 0, '2025-07-01 07:57:25.893235', 14, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (33, NULL, NULL, NULL, '2025-07-02 08:41:54.581823', 0, '2025-07-02 08:41:54.581874', 1, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (34, NULL, NULL, NULL, '2025-07-02 08:41:54.581888', 0, '2025-07-02 08:41:54.581902', 18, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (35, NULL, NULL, NULL, '2025-07-02 08:41:54.581914', 0, '2025-07-02 08:41:54.581927', 17, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (42, NULL, NULL, NULL, '2025-07-02 11:25:22.723559', 0, '2025-07-02 11:25:22.723574', 15, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (45, NULL, NULL, NULL, '2025-07-03 02:58:07.066807', 0, '2025-07-03 02:58:07.066937', 15, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (46, NULL, NULL, NULL, '2025-07-03 02:58:07.066958', 0, '2025-07-03 02:58:07.066974', 16, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (47, NULL, NULL, NULL, '2025-07-03 02:58:07.066986', 0, '2025-07-03 02:58:07.066999', 17, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (48, NULL, NULL, NULL, '2025-07-03 02:58:07.067011', 0, '2025-07-03 02:58:07.067023', 18, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (49, NULL, NULL, NULL, '2025-07-03 02:58:07.067034', 0, '2025-07-03 02:58:07.067046', 24, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (50, NULL, NULL, NULL, '2025-07-03 02:58:07.067057', 0, '2025-07-03 02:58:07.067070', 25, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (51, NULL, NULL, NULL, '2025-07-03 02:58:07.067081', 0, '2025-07-03 02:58:07.067093', 26, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (52, NULL, NULL, NULL, '2025-07-03 02:58:07.067104', 0, '2025-07-03 02:58:07.067116', 27, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (53, NULL, NULL, NULL, '2025-07-03 02:58:07.067126', 0, '2025-07-03 02:58:07.067138', 28, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (54, NULL, NULL, NULL, '2025-07-03 02:58:07.067149', 0, '2025-07-03 02:58:07.067161', 29, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (55, NULL, NULL, NULL, '2025-07-03 02:58:07.067171', 0, '2025-07-03 02:58:07.067183', 30, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (56, NULL, NULL, NULL, '2025-07-03 02:58:07.067195', 0, '2025-07-03 02:58:07.067230', 31, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (57, NULL, NULL, NULL, '2025-07-03 02:58:07.067241', 0, '2025-07-03 02:58:07.067254', 32, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (58, NULL, NULL, NULL, '2025-07-03 02:58:07.067265', 0, '2025-07-03 02:58:07.067276', 33, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (59, NULL, NULL, NULL, '2025-07-03 02:58:07.067287', 0, '2025-07-03 02:58:07.067300', 34, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (60, NULL, NULL, NULL, '2025-07-03 02:58:07.067311', 0, '2025-07-03 02:58:07.067324', 35, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (61, NULL, NULL, NULL, '2025-07-03 02:58:07.067335', 0, '2025-07-03 02:58:07.067360', 36, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (62, NULL, NULL, NULL, '2025-07-03 02:58:07.067376', 0, '2025-07-03 02:58:07.067390', 37, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (63, NULL, NULL, NULL, '2025-07-03 02:58:07.067402', 0, '2025-07-03 02:58:07.067414', 38, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (64, NULL, NULL, NULL, '2025-07-03 02:58:07.067425', 0, '2025-07-03 02:58:07.067437', 39, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (65, NULL, NULL, NULL, '2025-07-03 02:58:07.067449', 0, '2025-07-03 02:58:07.067460', 40, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (66, NULL, NULL, NULL, '2025-07-03 02:58:07.067471', 0, '2025-07-03 02:58:07.067483', 41, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (67, NULL, NULL, NULL, '2025-07-03 02:58:07.067494', 0, '2025-07-03 02:58:07.067506', 42, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (68, NULL, NULL, NULL, '2025-07-03 02:58:07.067517', 0, '2025-07-03 02:58:07.067529', 43, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (69, NULL, NULL, NULL, '2025-07-03 02:58:07.067540', 0, '2025-07-03 02:58:07.067552', 44, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (70, NULL, NULL, NULL, '2025-07-03 02:58:07.067563', 0, '2025-07-03 02:58:07.067575', 45, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (71, NULL, NULL, NULL, '2025-07-03 02:58:07.067586', 0, '2025-07-03 02:58:07.067598', 46, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (72, NULL, NULL, NULL, '2025-07-03 02:58:07.067608', 0, '2025-07-03 02:58:07.067629', 47, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (73, NULL, NULL, NULL, '2025-07-03 02:58:07.067641', 0, '2025-07-03 02:58:07.067653', 48, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (74, NULL, NULL, NULL, '2025-07-03 02:58:07.067664', 0, '2025-07-03 02:58:07.067677', 49, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (75, NULL, NULL, NULL, '2025-07-03 02:58:07.067688', 0, '2025-07-03 02:58:07.067701', 50, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (76, NULL, NULL, NULL, '2025-07-03 02:58:07.067715', 0, '2025-07-03 02:58:07.067729', 51, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (77, NULL, NULL, NULL, '2025-07-03 02:58:07.067740', 0, '2025-07-03 02:58:07.067752', 52, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (78, NULL, NULL, NULL, '2025-07-03 02:58:07.067763', 0, '2025-07-03 02:58:07.067775', 53, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (79, NULL, NULL, NULL, '2025-07-03 09:04:53.644448', 0, '2025-07-03 09:04:53.644494', 16, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (80, NULL, NULL, NULL, '2025-07-03 09:05:02.903456', 0, '2025-07-03 09:05:02.903513', 8, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (81, NULL, NULL, NULL, '2025-07-03 09:05:11.591940', 0, '2025-07-03 09:05:11.592014', 9, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (82, NULL, NULL, NULL, '2025-07-03 09:05:19.612920', 0, '2025-07-03 09:05:19.612966', 10, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (83, NULL, NULL, NULL, '2025-07-03 09:05:32.927909', 0, '2025-07-03 09:05:32.927962', 34, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (84, NULL, NULL, NULL, '2025-07-03 09:05:32.927975', 0, '2025-07-03 09:05:32.927988', 35, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (85, NULL, NULL, NULL, '2025-07-03 09:05:32.928000', 0, '2025-07-03 09:05:32.928012', 36, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (86, NULL, NULL, NULL, '2025-07-03 09:05:32.928024', 0, '2025-07-03 09:05:32.928036', 37, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (87, NULL, NULL, NULL, '2025-07-03 09:05:32.928047', 0, '2025-07-03 09:05:32.928060', 38, 2);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (88, NULL, NULL, NULL, '2025-07-18 13:20:50.934154', 0, '2025-07-18 13:20:50.934209', 54, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (89, NULL, NULL, NULL, '2025-07-18 13:20:50.934224', 0, '2025-07-18 13:20:50.934238', 55, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (90, NULL, NULL, NULL, '2025-07-18 13:20:50.934251', 0, '2025-07-18 13:20:50.934265', 56, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (91, NULL, NULL, NULL, '2025-07-18 13:20:50.934277', 0, '2025-07-18 13:20:50.934291', 57, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (92, NULL, NULL, NULL, '2025-07-18 13:20:50.934304', 0, '2025-07-18 13:20:50.934318', 58, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (93, NULL, NULL, NULL, '2025-07-18 13:20:50.934331', 0, '2025-07-18 13:20:50.934345', 59, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (94, NULL, NULL, NULL, '2025-07-18 13:20:50.934357', 0, '2025-07-18 13:20:50.934371', 60, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (95, NULL, NULL, NULL, '2025-07-18 13:20:50.934383', 0, '2025-07-18 13:20:50.934398', 61, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (96, NULL, NULL, NULL, '2025-07-18 13:20:50.934410', 0, '2025-07-18 13:20:50.934423', 62, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (97, NULL, NULL, NULL, '2025-07-18 13:20:50.934437', 0, '2025-07-18 13:20:50.934451', 63, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (98, NULL, NULL, NULL, '2025-07-18 13:20:50.934463', 0, '2025-07-18 13:20:50.934477', 64, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (99, NULL, NULL, NULL, '2025-07-18 13:20:50.934489', 0, '2025-07-18 13:20:50.934504', 65, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (100, NULL, NULL, NULL, '2025-07-18 13:20:50.934517', 0, '2025-07-18 13:20:50.934530', 66, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (101, NULL, NULL, NULL, '2025-07-18 13:20:50.934543', 0, '2025-07-18 13:20:50.934557', 67, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (102, NULL, NULL, NULL, '2025-07-18 13:20:50.934588', 0, '2025-07-18 13:20:50.934605', 68, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (103, NULL, NULL, NULL, '2025-07-18 13:20:50.934618', 0, '2025-07-18 13:20:50.934632', 69, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (104, NULL, NULL, NULL, '2025-07-18 13:20:50.934646', 0, '2025-07-18 13:20:50.934660', 70, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (105, NULL, NULL, NULL, '2025-07-18 13:20:50.934674', 0, '2025-07-18 13:20:50.934689', 71, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (106, NULL, NULL, NULL, '2025-07-18 13:20:50.934701', 0, '2025-07-18 13:20:50.934716', 72, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (107, NULL, NULL, NULL, '2025-07-18 13:20:50.934730', 0, '2025-07-18 13:20:50.934745', 73, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (108, NULL, NULL, NULL, '2025-07-18 13:20:50.934757', 0, '2025-07-18 13:20:50.934772', 74, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (109, NULL, NULL, NULL, '2025-07-18 13:20:50.934784', 0, '2025-07-18 13:20:50.934798', 75, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (110, NULL, NULL, NULL, '2025-07-18 13:20:50.934811', 0, '2025-07-18 13:20:50.934824', 76, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (111, NULL, NULL, NULL, '2025-07-18 13:20:50.934836', 0, '2025-07-18 13:20:50.934849', 78, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (112, NULL, NULL, NULL, '2025-07-18 13:20:50.934862', 0, '2025-07-18 13:20:50.934875', 79, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (113, NULL, NULL, NULL, '2025-07-18 13:20:50.934888', 0, '2025-07-18 13:20:50.934901', 80, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (114, NULL, NULL, NULL, '2025-07-18 13:20:50.934913', 0, '2025-07-18 13:20:50.934927', 81, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (115, NULL, NULL, NULL, '2025-07-18 13:20:50.934940', 0, '2025-07-18 13:20:50.934953', 82, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (116, NULL, NULL, NULL, '2025-07-18 13:20:50.934965', 0, '2025-07-18 13:20:50.934978', 83, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (117, NULL, NULL, NULL, '2025-07-18 13:20:50.934991', 0, '2025-07-18 13:20:50.935004', 84, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (118, NULL, NULL, NULL, '2025-07-18 13:20:50.935019', 0, '2025-07-18 13:20:50.935033', 85, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (119, NULL, NULL, NULL, '2025-07-18 13:20:50.935045', 0, '2025-07-18 13:20:50.935058', 86, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (120, NULL, NULL, NULL, '2025-07-18 13:20:50.935071', 0, '2025-07-18 13:20:50.935084', 87, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (121, NULL, NULL, NULL, '2025-07-18 13:20:50.935097', 0, '2025-07-18 13:20:50.935112', 88, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (122, NULL, NULL, NULL, '2025-07-18 13:20:50.935124', 0, '2025-07-18 13:20:50.935137', 89, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (123, NULL, NULL, NULL, '2025-07-18 13:20:50.935150', 0, '2025-07-18 13:20:50.935162', 90, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (124, NULL, NULL, NULL, '2025-07-18 13:20:50.935175', 0, '2025-07-18 13:20:50.935189', 91, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (125, NULL, NULL, NULL, '2025-07-18 13:20:50.935201', 0, '2025-07-18 13:20:50.935214', 92, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (126, NULL, NULL, NULL, '2025-07-18 13:20:50.935226', 0, '2025-07-18 13:20:50.935239', 93, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (127, NULL, NULL, NULL, '2025-07-18 13:20:50.935252', 0, '2025-07-18 13:20:50.935265', 94, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (128, NULL, NULL, NULL, '2025-07-18 13:20:50.935277', 0, '2025-07-18 13:20:50.935290', 95, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (129, NULL, NULL, NULL, '2025-07-18 13:20:50.935303', 0, '2025-07-18 13:20:50.935316', 96, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (130, NULL, NULL, NULL, '2025-07-18 13:20:50.935328', 0, '2025-07-18 13:20:50.935341', 97, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (131, NULL, NULL, NULL, '2025-07-18 13:20:50.935353', 0, '2025-07-18 13:20:50.935366', 98, 3);
INSERT INTO `system_role_permission` (`id`, `remark`, `creator`, `modifier`, `update_time`, `is_deleted`, `create_time`, `menu_id`, `role_id`) VALUES (132, NULL, NULL, NULL, '2025-07-18 13:20:50.935378', 0, '2025-07-18 13:20:50.935391', 99, 3);
COMMIT;

-- ----------------------------
-- Table structure for system_users
-- ----------------------------
DROP TABLE IF EXISTS `system_users`;
CREATE TABLE `system_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL COMMENT 'password',
  `last_login` datetime(6) DEFAULT NULL COMMENT 'last login',
  `is_superuser` tinyint(1) NOT NULL COMMENT 'superuser status',
  `username` varchar(150) NOT NULL COMMENT 'username',
  `first_name` varchar(150) NOT NULL COMMENT 'first name',
  `last_name` varchar(150) NOT NULL COMMENT 'last name',
  `email` varchar(254) NOT NULL COMMENT 'email address',
  `is_staff` tinyint(1) NOT NULL COMMENT 'staff status',
  `is_active` tinyint(1) NOT NULL COMMENT 'active',
  `date_joined` datetime(6) NOT NULL COMMENT 'date joined',
  `remark` varchar(256) DEFAULT NULL COMMENT '备注',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建人',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(6) DEFAULT NULL COMMENT '修改时间',
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否软删除',
  `mobile` varchar(11) DEFAULT NULL COMMENT '手机号',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `gender` smallint DEFAULT NULL COMMENT '性别',
  `language` varchar(20) DEFAULT NULL COMMENT '语言',
  `city` varchar(20) DEFAULT NULL COMMENT '城市',
  `province` varchar(50) DEFAULT NULL COMMENT '省份',
  `country` varchar(50) DEFAULT NULL COMMENT '国家',
  `avatar_url` varchar(200) DEFAULT NULL COMMENT '头像',
  `status` int NOT NULL,
  `login_ip` char(39) DEFAULT NULL COMMENT '最后登录IP',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_users
-- ----------------------------
BEGIN;
INSERT INTO `system_users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `mobile`, `nickname`, `gender`, `language`, `city`, `province`, `country`, `avatar_url`, `status`, `login_ip`) VALUES (1, 'pbkdf2_sha256$1000000$b8gwLD046kZQIz1VMiUnmN$8/HRWXvV2MawPTME6SBo2bmA+pXYMN375l91lFdIIZE=', '2025-07-18 05:44:57.070873', 1, 'admin', '', '', '765462425@qq.com', 1, 1, '2025-06-29 13:09:47.780431', NULL, NULL, 'admin', '2025-07-04 14:48:13.446261', '2025-06-29 13:09:47.892332', 0, '18888888888', NULL, 0, NULL, NULL, NULL, NULL, NULL, 1, '127.0.0.1');
INSERT INTO `system_users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `mobile`, `nickname`, `gender`, `language`, `city`, `province`, `country`, `avatar_url`, `status`, `login_ip`) VALUES (2, 'pbkdf2_sha256$1000000$MWNyUoBTr4K24ySzXNbQup$eB+xVm6dCqwSVBQV5hIrURgMe2NGFgaeXpsociexCcI=', '2025-07-05 02:03:48.872113', 0, 'chenze', '', '', '765462425@qq.com', 0, 1, '2025-07-01 06:25:50.946515', NULL, 'admin', 'admin', '2025-07-05 02:04:38.567613', '2025-07-01 06:25:50.947136', 0, '18677777776', NULL, 0, NULL, NULL, NULL, NULL, NULL, 1, '127.0.0.1');
COMMIT;

-- ----------------------------
-- Table structure for system_users_dept
-- ----------------------------
DROP TABLE IF EXISTS `system_users_dept`;
CREATE TABLE `system_users_dept` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `dept_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_users_dept_user_id_dept_id_b67fb9af_uniq` (`user_id`,`dept_id`),
  KEY `system_users_dept_user_id_0fc212c8` (`user_id`),
  KEY `system_users_dept_dept_id_896a13cf` (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_users_dept
-- ----------------------------
BEGIN;
INSERT INTO `system_users_dept` (`id`, `user_id`, `dept_id`) VALUES (2, 1, 2);
INSERT INTO `system_users_dept` (`id`, `user_id`, `dept_id`) VALUES (1, 2, 7);
COMMIT;

-- ----------------------------
-- Table structure for system_users_groups
-- ----------------------------
DROP TABLE IF EXISTS `system_users_groups`;
CREATE TABLE `system_users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_users_groups_user_id_group_id_f81bb272_uniq` (`user_id`,`group_id`),
  KEY `system_users_groups_group_id_13685d93_fk_auth_group_id` (`group_id`),
  CONSTRAINT `system_users_groups_group_id_13685d93_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `system_users_groups_user_id_8e553e0f_fk_system_users_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_users_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for system_users_post
-- ----------------------------
DROP TABLE IF EXISTS `system_users_post`;
CREATE TABLE `system_users_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `post_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_users_post_user_id_post_id_2725e620_uniq` (`user_id`,`post_id`),
  KEY `system_users_post_user_id_2e8013c5` (`user_id`),
  KEY `system_users_post_post_id_6560916c` (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_users_post
-- ----------------------------
BEGIN;
INSERT INTO `system_users_post` (`id`, `user_id`, `post_id`) VALUES (1, 2, 2);
INSERT INTO `system_users_post` (`id`, `user_id`, `post_id`) VALUES (2, 2, 3);
COMMIT;

-- ----------------------------
-- Table structure for system_users_role
-- ----------------------------
DROP TABLE IF EXISTS `system_users_role`;
CREATE TABLE `system_users_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_users_role_user_id_role_id_5ed2fce2_uniq` (`user_id`,`role_id`),
  KEY `system_users_role_user_id_72adb6a9` (`user_id`),
  KEY `system_users_role_role_id_056fc093` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_users_role
-- ----------------------------
BEGIN;
INSERT INTO `system_users_role` (`id`, `user_id`, `role_id`) VALUES (1, 2, 2);
COMMIT;

-- ----------------------------
-- Table structure for system_users_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `system_users_user_permissions`;
CREATE TABLE `system_users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_users_user_permis_user_id_permission_id_e2b19df4_uniq` (`user_id`,`permission_id`),
  KEY `system_users_user_pe_permission_id_691fa57c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `system_users_user_pe_permission_id_691fa57c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `system_users_user_pe_user_id_c49a4571_fk_system_us` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_users_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
