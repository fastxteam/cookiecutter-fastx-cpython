Project: {{cookiecutter.project_name}}
Version: {{cookiecutter.project_version}}
Author: {{cookiecutter.author_name}}


## 编译CPython

core.pyx 是 Cython 文件，需要先编译才能被 Python 导入。以下是解决方案：
如果你不需要 Cython 的特性，最简单的方法是将 core.pyx 改为 core.py：

```bash
# 方法1： 在项目根目录执行 | 开发模式安装（推荐）
pip install -e .

# 方法2：在项目根目录执行 | 直接编译
python setup.py build_ext --inplace
```
