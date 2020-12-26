import string


class HttpException(Exception):
    def __init__(self, code: int, msg: string):
        self.msg = msg
        self.code = code
        super().__init__(self.msg)


class BadRequestException(HttpException):
    def __init__(self, msg: string):
        self.msg = msg
        super().__init__(400, self.msg)


class UnauthorizedException(HttpException):
    def __init__(self, msg: string):
        self.msg = msg
        super().__init__(401, self.msg)


class ForbiddenException(HttpException):
    def __init__(self, msg: string):
        self.msg = msg
        super().__init__(403, self.msg)


class NotFoundException(HttpException):
    def __init__(self, msg: string):
        self.msg = msg
        super().__init__(404, self.msg)


class InternalServerException(HttpException):
    def __init__(self, msg: string):
        self.msg = msg
        super().__init__(500, self.msg)
