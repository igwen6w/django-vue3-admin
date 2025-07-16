import { useDictStore } from '#/store/dict';

export function useDictOptions(dictType: string) {
  const dictStore = useDictStore();
  return dictStore.getOptionsByType(dictType);
}

/**
 * 通用字典 value 转 label
 * @param dictType 字典类型
 * @param value 字典值
 * @returns label
 */
export function useDictLabel(dictType: string, value: any): string {
  const options = useDictOptions(dictType);
  const item = options.find((opt) => opt.value === value);
  return item ? item.label : value;
}

export function dictFormatter(dictType: string) {
  return ({ cellValue }: { cellValue: any }) =>
    useDictLabel(dictType, cellValue);
}
