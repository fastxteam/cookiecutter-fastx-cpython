"""
File: main.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
Description: Main CLI entry
"""

import warnings
from api.api import *
from decorators.timing import *
from decorators.logging import *
warnings.filterwarnings('ignore', category=UserWarning)

@timer(unit='s')
@log_func_call(log_args=True, log_result=True)
def main():
    core_init()


if __name__ == "__main__":
    main()
