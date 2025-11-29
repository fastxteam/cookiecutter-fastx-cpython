"""
File: core.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
core/core.py    ： 开发期调用
core/core.pyx   ： 生产期调用

# 开发加载 core.py
# 生产加载 core.cp313-win_amd64.pyd
# 优先级 .pyd > .so > .py > .pyx
from core.core import *
"""
