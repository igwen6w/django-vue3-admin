export function formatToken(token: null | string) {
  return token ? `Bearer ${token}` : null;
}
