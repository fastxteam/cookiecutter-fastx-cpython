"""
File: setup.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
Description: setup
"""

# setup.py
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("core.core", ["src/core/core.pyx"]),  # 注意：包名 core.core，不加 src
]

setup(
    name="{{ cookiecutter.project_slug }}",
    version="{{ cookiecutter.project_version }}",
    packages=find_packages(where="src"),  # src 下所有包
    package_dir={"": "src"},  # 告诉 setuptools src 是根包目录
    ext_modules=cythonize(extensions),
)
