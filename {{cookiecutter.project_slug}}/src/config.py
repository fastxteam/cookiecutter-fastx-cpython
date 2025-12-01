"""
File: config.py
Author: {{ cookiecutter.author_name }}
Version: {{ cookiecutter.project_version }}
Date: {{ cookiecutter.date }}
Description: Main Config
"""
from loguru import logger
import sys

# ------------------------------------------
# Unified Logger for mytool
# {{cookiecutter.project_slug}} 统一日志记录器
# ------------------------------------------
logger.remove()  # Remove default handler
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
logger.add("logs/{{cookiecutter.project_slug}}.log", rotation="10 MB", retention="7 days", encoding="utf-8")  # File logging

# Now you can import this logger in all modules
