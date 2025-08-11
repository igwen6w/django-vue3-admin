import type { App, DirectiveBinding } from 'vue';

import { usePermissionStore } from '#/store/permission';

/**
 * 权限按钮option生成工具
 * @param code 权限码
 * @param option 按钮option或字符串
 * @returns 有权限返回option，无权限返回false
 */
export function op(code: string, option: any) {
  const permissionStore = usePermissionStore();
  return permissionStore.hasPermission(code) ? option : false;
}

/**
 * 全局权限判断函数，适用于模板v-if
 */
export function hasPermission(code: string): boolean {
  const permissionStore = usePermissionStore();
  return permissionStore.hasPermission(code);
}

/**
 * v-permission 自定义指令
 * 用法：v-permission="'system:user:create'"
 * 或 v-permission="['system:user:create', 'system:user:update']"
 */
const permissionDirective = {
  mounted(el: HTMLElement, binding: DirectiveBinding<string | string[]>) {
    const codes = Array.isArray(binding.value)
      ? binding.value
      : [binding.value];
    const permissionStore = usePermissionStore();
    const has = codes.some((code) => permissionStore.hasPermission(code));
    if (!has) {
      el.parentNode && el.remove();
    }
  },
};

/**
 * 注册全局权限指令
 * @param app Vue App 实例
 */
export function registerPermissionDirective(app: App) {
  app.directive('permission', permissionDirective);
}
