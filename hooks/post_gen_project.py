# hooks/post_gen_project.py
import subprocess
import os
import sys
import platform

def run_cmd(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

# -----------------------------
# Project path
# -----------------------------
project_path = os.getcwd()  # post-gen hook 执行目录就是生成的项目根目录
print(f"Project path: {project_path}")

# -----------------------------
# Initialize Git
# -----------------------------
run_cmd(["git", "init"], cwd=project_path)

# -----------------------------
# Create virtual environment (.venv)
# -----------------------------
venv_name = ".venv"
venv_path = os.path.join(project_path, venv_name)

if not os.path.exists(venv_path):
    print(f"Creating virtual environment at {venv_path}")
    run_cmd([sys.executable, "-m", "venv", venv_name])

# 写入 .python-version 文件（pyenv / uv 可以读取）
with open(".python-version", "w") as f:
    f.write(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# Python executable inside venv
if platform.system() == "Windows":
    python_bin = os.path.join(venv_path, "Scripts", "python.exe")
else:
    python_bin = os.path.join(venv_path, "bin", "python")

# -----------------------------
# Upgrade pip
# -----------------------------
run_cmd([python_bin, "-m", "pip", "install", "--upgrade", "pip"])

# -----------------------------
# Optional: uv sync (if uv CLI is installed)
# -----------------------------
try:
    run_cmd(["uv", "sync"], cwd=project_path)
except FileNotFoundError:
    print("uv command not found, skipping uv sync, try pip install package")
    # -----------------------------
    # Install Cython (required for .pyx)
    # -----------------------------
    run_cmd([python_bin, "-m", "pip", "install", "cython"])
    # -----------------------------
    # Install other requirements if exist
    # -----------------------------
    requirements_file = os.path.join(project_path, "requirements.txt")
    if os.path.exists(requirements_file):
        run_cmd([python_bin, "-m", "pip", "install", "-r", requirements_file])
    # -----------------------------
    # Install project in editable mode
    # -----------------------------
    run_cmd([python_bin, "-m", "pip", "install", "-e", "."])

print("✅ Project setup complete!")
print(f"Activate your virtual environment:\nWindows: {venv_path}\\Scripts\\activate.bat\nLinux/Mac: source {venv_path}/bin/activate")
