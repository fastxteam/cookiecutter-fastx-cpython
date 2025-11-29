# hooks/pre_gen_project.py
import os
import sys
import datetime

project_name = '{{cookiecutter.project_slug}}'
# Cookiecutter JSON 文件路径
cookiecutter_json_path = os.path.join(os.getcwd(), "cookiecutter.json")
# 获取当前日期
today = datetime.datetime.now().strftime("%Y-%m-%d")
# 直接通过环境变量传给模板
os.environ["COOKIECUTTER_DATE"] = today

if not project_name.isidentifier():
    print(f"Error: Project name '{project_name}' is invalid. Must be a valid Python identifier.")
    sys.exit(1)
