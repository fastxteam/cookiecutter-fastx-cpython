# hooks/post_gen_project.py
import subprocess
import os

project_dir = os.path.realpath(os.path.curdir)

# 初始化 Git 仓库
subprocess.run(["git", "init"], cwd=project_dir)

# 创建虚拟环境
subprocess.run(["python", "-m", "venv", "venv"], cwd=project_dir)

print("Project setup complete!")
