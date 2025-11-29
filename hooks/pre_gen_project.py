# hooks/pre_gen_project.py
import sys

project_name = '{{cookiecutter.project_name}}'

if not project_name.isidentifier():
    print(f"Error: Project name '{project_name}' is invalid. Must be a valid Python identifier.")
    sys.exit(1)
