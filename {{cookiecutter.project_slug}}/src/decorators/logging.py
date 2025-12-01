"""
File: logging.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
Description: Decorator to log function calls, arguments, results and exceptions.
"""
from functools import wraps
from config import logger

def log_func_call(log_args: bool = True, log_result: bool = True, log_exceptions: bool = True):
    """
    Decorator to log function calls, arguments, results and exceptions.
    函数调用日志装饰器：记录函数入口、参数、返回值和异常

    Args:
        log_args (bool): Whether to log function arguments 是否记录参数
        log_result (bool): Whether to log function return value 是否记录返回值
        log_exceptions (bool): Whether to log exceptions 是否记录异常
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if log_args:
                    logger.info(f"[CALL] {func.__name__} called with args={args}, kwargs={kwargs}")
                result = func(*args, **kwargs)
                if log_result:
                    logger.info(f"[RETURN] {func.__name__} returned {result}")
                return result
            except Exception as e:
                if log_exceptions:
                    logger.exception(f"[EXCEPTION] {func.__name__} raised an exception: {e}")
                raise  # 保留原异常，不吞掉
        return wrapper
    return decorator
