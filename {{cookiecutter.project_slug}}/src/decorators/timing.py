"""
File: timer.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
Description: Decorator to measure execution time of a function.
"""
import time
from functools import wraps
from config import logger  # 使用全局logger

def timer(unit: str = 's', log: bool = True):
    """
    Decorator to measure execution time of a function.
    函数执行时间装饰器

    Args:
        unit (str): Time unit, 's', 'ms', or 'us' (时间单位: 秒/毫秒/微秒)
        log (bool): Whether to log the result using the unified logger
                    是否使用统一日志记录器输出
    """
    units_map = {'s': 1, 'ms': 1000, 'us': 1_000_000}

    if unit not in units_map:
        raise ValueError(f"Unsupported unit '{unit}', choose from {list(units_map.keys())}")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * units_map[unit]
            msg = f"[TIMER] Function '{func.__name__}' executed in {elapsed:.3f} {unit}"
            if log:
                logger.info(msg)  # 使用统一logger
            else:
                print(msg)
            return result

        return wrapper

    return decorator
