"""
File: core.pyx
Author: FastXTeam/wanqiang.liu
Version: 0.1.0
Date:
core/core.pyx   ： 核心算法，只暴露接口给 api 调用
core/xxx.py     : 方法封装成可调用函数，可在 core.pyx 调用
core/__init__.py: 中导出需要暴露给外层的接口
"""

from .auth_client import AuthClient


# 最简单的使用方式
def quick_check(api_path):
    """
    快速检查API授权

    Args:
        api_path: 要检查的API路径

    Returns:
        bool: 是否授权
    """
    client = AuthClient()  # 使用默认地址 http://localhost:8000
    return client.is_authorized(api_path)


if __name__ == "__main__":
    pass