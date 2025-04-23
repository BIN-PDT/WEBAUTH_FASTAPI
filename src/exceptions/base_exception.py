class BaseException(Exception):
    status_code: int
    detail: dict
