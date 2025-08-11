import { ref } from 'vue';

import { defineStore } from 'pinia';

export const usePermissionStore = defineStore('permission', () => {
  // 权限码列表
  const permissions = ref<string[]>([]);

  // 设置权限码
  function setPermissions(perms: string[]) {
    permissions.value = perms || [];
  }

  // 判断是否有某个权限
  function hasPermission(code: string): boolean {
    return permissions.value.includes(code);
  }

  // 重置
  function $reset() {
    permissions.value = [];
  }

  return {
    permissions,
    setPermissions,
    hasPermission,
    $reset,
  };
})
