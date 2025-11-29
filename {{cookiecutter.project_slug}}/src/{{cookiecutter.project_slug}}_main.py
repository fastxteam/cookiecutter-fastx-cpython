"""
File: main.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
Description: Main CLI entry
"""

from api.api import *
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

def main():
    core_init()


if __name__ == "__main__":
    main()
