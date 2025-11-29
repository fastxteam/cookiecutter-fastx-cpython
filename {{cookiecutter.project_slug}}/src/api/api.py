"""
File: api.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
Description: API interfaces for core functions
"""

from core.core import *



def core_init():
    authorized = quick_check("/api/fastdem/v1")
    print(f"{api} -> {'✅ 已授权' if authorized else '❌ 未授权'}")