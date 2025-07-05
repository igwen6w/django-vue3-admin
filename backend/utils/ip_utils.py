def get_client_ip(request):
    """
    获取客户端真实IP地址
    考虑代理服务器的情况，按优先级获取IP
    """
    # 按优先级顺序检查各种IP头
    ip_headers = [
        'HTTP_X_FORWARDED_FOR',      # 最常用的代理IP头
        'HTTP_X_REAL_IP',            # Nginx 代理
        'HTTP_X_CLIENT_IP',          # 客户端IP
        'HTTP_X_FORWARDED',          # 转发IP
        'HTTP_FORWARDED_FOR',        # 标准转发IP
        'HTTP_FORWARDED',            # 标准转发
        'HTTP_CLIENT_IP',            # 客户端IP
        'REMOTE_ADDR',               # 直接连接IP
    ]
    
    for header in ip_headers:
        ip = request.META.get(header)
        if ip:
            # 处理多个IP的情况（如 X-Forwarded-For: client, proxy1, proxy2）
            if ',' in ip:
                # 取第一个IP（客户端真实IP）
                ip = ip.split(',')[0].strip()
            
            # 验证IP格式
            if is_valid_ip(ip):
                return ip
    
    # 如果都没有找到，返回 REMOTE_ADDR
    return request.META.get('REMOTE_ADDR', '')


def is_valid_ip(ip):
    """
    验证IP地址格式是否有效
    """
    if not ip:
        return False
    
    # 简单的IP格式验证
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    try:
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except (ValueError, TypeError):
        return False


def get_client_ip_simple(request):
    """
    简化版获取客户端IP（推荐用于大多数情况）
    """
    # 优先获取 X-Forwarded-For
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # 取第一个IP
        ip = x_forwarded_for.split(',')[0].strip()
        if ip:
            return ip
    
    # 获取 X-Real-IP
    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    if x_real_ip:
        return x_real_ip
    
    # 最后使用 REMOTE_ADDR
    return request.META.get('REMOTE_ADDR', '') 