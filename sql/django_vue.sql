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

 Date: 07/07/2025 00:04:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (1, 'admin', 'logentry');
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
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_dict_data
-- ----------------------------
BEGIN;
INSERT INTO `system_dict_data` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `sort`, `label`, `value`, `status`, `color_type`, `css_class`, `dict_type_id`) VALUES (1, NULL, NULL, NULL, '2025-06-30 09:32:31.805645', '2025-06-30 09:32:31.805691', 0, 1, '都撒到', 'sadas', 1, 'primary', '', 1);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_dict_type
-- ----------------------------
BEGIN;
INSERT INTO `system_dict_type` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `value`, `status`, `deleted_time`) VALUES (1, NULL, NULL, NULL, '2025-07-01 04:58:37.679182', '2025-06-29 13:32:51.050675', 0, 'jdjkhj', 'sad_ds', 1, NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (19, NULL, NULL, NULL, '2025-07-05 01:54:03.993248', '2025-07-05 01:54:03.993260', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (20, NULL, NULL, NULL, '2025-07-05 02:02:58.915096', '2025-07-05 02:02:58.915110', 0, 'admin', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (21, NULL, NULL, NULL, '2025-07-05 02:03:48.892432', '2025-07-05 02:03:48.892446', 0, 'chenze', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
INSERT INTO `system_login_log` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `username`, `result`, `user_ip`, `user_agent`) VALUES (22, NULL, NULL, NULL, '2025-07-05 02:03:56.725873', '2025-07-05 02:03:56.725887', 0, 'admin', 1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
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
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_menu
-- ----------------------------
BEGIN;
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (1, NULL, NULL, 'admin', '2025-07-01 09:45:35.225930', '2025-06-30 09:35:21.372555', 0, '概览', 1, 'menu', '/workspace', '/dashboard/workspace/index', '', NULL, 1, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (2, NULL, NULL, NULL, '2025-06-30 12:37:55.656213', '2025-06-30 12:37:55.656233', 0, 'System', 1, 'catalog', '/system', '', '', NULL, 2, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (3, NULL, NULL, 'admin', '2025-07-02 03:49:50.551599', '2025-06-30 12:38:52.398094', 0, 'SystemMenu', 1, 'menu', '/system/menu', '/system/menu/list', '', 2, 3, 10);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (4, NULL, NULL, 'admin', '2025-07-01 08:11:00.187470', '2025-06-30 12:57:14.866495', 0, 'SystemMenuCreate', 1, 'button', '', '', 'system:menu:create', 3, 4, 2);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (5, NULL, NULL, 'admin', '2025-07-01 08:12:04.836586', '2025-06-30 12:57:40.728694', 0, 'SystemMenuEdit', 1, 'button', '', '', 'system:menu:edit', 3, 5, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (6, NULL, NULL, 'admin', '2025-07-01 08:12:17.723905', '2025-06-30 12:58:05.562477', 0, 'SystemMenuDelete', 1, 'button', '', '', 'system:menu:delete', 3, 6, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (7, NULL, NULL, 'admin', '2025-07-02 03:49:42.209946', '2025-06-30 12:58:55.893906', 0, 'SystemDept', 1, 'menu', '/system/dept', '/system/dept/list', '', 2, 7, 20);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (8, NULL, NULL, NULL, '2025-06-30 12:59:18.313868', '2025-06-30 12:59:18.313943', 0, 'SystemDeptCreate', 1, 'button', '', '', 'system:dept:create', 7, 8, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (9, NULL, NULL, NULL, '2025-06-30 12:59:45.455554', '2025-06-30 12:59:45.455621', 0, 'SystemDeptEdit', 1, 'button', '', '', 'system:dept:edit', 7, 9, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (10, NULL, NULL, NULL, '2025-06-30 13:00:27.836789', '2025-06-30 13:00:27.836845', 0, 'SystemDeptDelete', 1, 'button', '', '', 'system:dept:delete', 7, 10, 0);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (12, NULL, NULL, 'admin', '2025-07-03 03:12:19.599531', '2025-06-30 14:14:57.815188', 0, 'About', 1, 'menu', '/about', '_core/about/index', '', NULL, 12, 8);
INSERT INTO `system_menu` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `type`, `path`, `component`, `auth_code`, `pid_id`, `meta_id`, `sort`) VALUES (13, NULL, 'admin', 'admin', '2025-07-06 16:01:51.348938', '2025-06-30 14:17:50.344905', 0, 'Project', 1, 'catalog', '/django-vue3-admin', '', '', NULL, 13, 0);
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
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_menu_meta
-- ----------------------------
BEGIN;
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (1, NULL, NULL, NULL, '2025-07-01 09:45:35.200879', '2025-06-30 09:35:21.346111', 0, 'page.dashboard.title', 'carbon:workspace', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (2, NULL, NULL, NULL, '2025-06-30 12:37:55.632644', '2025-06-30 12:37:55.632666', 0, 'system.title', 'carbon:settings', 0, 0, 'new', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (3, NULL, NULL, NULL, '2025-07-02 03:49:50.547348', '2025-06-30 12:38:52.374691', 0, 'system.menu.title', 'carbon:menu', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (4, NULL, NULL, NULL, '2025-07-01 08:11:00.165353', '2025-06-30 12:57:14.842379', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (5, NULL, NULL, NULL, '2025-07-01 08:12:04.811256', '2025-06-30 12:57:40.703715', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (6, NULL, NULL, NULL, '2025-07-01 08:12:17.702120', '2025-06-30 12:58:05.535736', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (7, NULL, NULL, NULL, '2025-07-02 03:49:42.205928', '2025-06-30 12:58:55.867808', 0, 'system.dept.title', 'carbon:container-services', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (8, NULL, NULL, NULL, '2025-06-30 12:59:18.290232', '2025-06-30 12:59:18.290288', 0, 'common.create', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (9, NULL, NULL, NULL, '2025-06-30 12:59:45.429985', '2025-06-30 12:59:45.430037', 0, 'common.edit', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (10, NULL, NULL, NULL, '2025-06-30 13:00:27.814988', '2025-06-30 13:00:27.815021', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (11, NULL, NULL, NULL, '2025-06-30 13:00:28.085386', '2025-06-30 13:00:28.085434', 0, 'common.delete', '', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (12, NULL, NULL, NULL, '2025-07-03 03:12:19.592343', '2025-06-30 14:14:57.789248', 0, 'demos.vben.about', 'lucide:copyright', 0, 0, '', '', '', '', '', 0, 0);
INSERT INTO `system_menu_meta` (`id`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `title`, `icon`, `sort`, `affix_tab`, `badge`, `badge_type`, `badge_variants`, `iframe_src`, `link`, `hide_children_in_menu`, `hide_in_menu`) VALUES (13, NULL, NULL, NULL, '2025-07-06 16:01:51.343973', '2025-06-30 14:17:50.320137', 0, 'demos.vben.title', 'carbon:data-center', 0, 0, '', '', '', '', '', 0, 0);
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
INSERT INTO `system_role` (`id`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `name`, `status`, `sort`, `remark`, `code`) VALUES (3, 'admin', 'admin', '2025-07-03 02:58:07.056753', '2025-06-30 14:01:56.403744', 0, '超级管理员', 1, 0, '', 'super_admin');
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
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
COMMIT;

-- ----------------------------
-- Table structure for system_users
-- ----------------------------
DROP TABLE IF EXISTS `system_users`;
CREATE TABLE `system_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
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
INSERT INTO `system_users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `remark`, `creator`, `modifier`, `update_time`, `create_time`, `is_deleted`, `mobile`, `nickname`, `gender`, `language`, `city`, `province`, `country`, `avatar_url`, `status`, `login_ip`) VALUES (1, 'pbkdf2_sha256$1000000$b8gwLD046kZQIz1VMiUnmN$8/HRWXvV2MawPTME6SBo2bmA+pXYMN375l91lFdIIZE=', '2025-07-05 02:03:56.705767', 1, 'admin', '', '', '765462425@qq.com', 1, 1, '2025-06-29 13:09:47.780431', NULL, NULL, 'admin', '2025-07-04 14:48:13.446261', '2025-06-29 13:09:47.892332', 0, '18888888888', NULL, 0, NULL, NULL, NULL, NULL, NULL, 1, '127.0.0.1');
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
