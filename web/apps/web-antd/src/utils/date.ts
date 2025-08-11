import dayjs from 'dayjs';

/**
 * 格式化 ISO 时间字符串为 'YYYY-MM-DD HH:mm:ss'
 * @param value ISO 时间字符串
 * @param format 自定义格式，默认 'YYYY-MM-DD HH:mm:ss'
 */
export function format_datetime(
  value: Date | string,
  format = 'YYYY-MM-DD HH:mm:ss',
): string {
  if (!value) return '';
  return dayjs(value).format(format);
}
