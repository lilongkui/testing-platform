class BusinessException_404(Exception):
    def __init__(self, message="请求的资源不存在"):
        self.code = 404
        self.message = message


class BusinessException_401(Exception):
    def __init__(self, message="认证失败，请重新登录"):
        self.code = 401
        self.message = message


class BusinessException_403(Exception):
    def __init__(self, message="无访问权限"):
        self.code = 403
        self.message = message


class BusinessException_400(Exception):
    def __init__(self, code=400, message="操作失败"):
        self.code = code
        self.message = message
