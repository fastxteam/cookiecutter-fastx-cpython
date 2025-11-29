# Cookiecutter FastX CPython

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-package%20manager-purple)](https://docs.astral.sh/uv/)
[![Cython](https://img.shields.io/badge/cython-performance-orange)](https://cython.org/)
[![PyInstaller](https://img.shields.io/badge/pyinstaller-executable%20build-green)](https://pyinstaller.org/)

A modern Cookiecutter template for creating high-performance Python projects with Cython extensions and PyInstaller packaging.

## 🚀 Features

- **Performance-First Design**: Core algorithms implemented in Cython for maximum speed
- **Modern Package Management**: Full [uv](https://docs.astral.sh/uv/) integration with pip fallback
- **Smart Loading**: Automatic fallback from compiled Cython (.pyd/.so) to Python implementations
- **Executable Creation**: Complete PyInstaller setup for standalone executables
- **Development Tools**: Pre-configured with pytest, black, isort, flake8, mypy
- **CI/CD Ready**: GitHub Actions workflows for testing and PyPI publishing
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🏗️ Architecture

```
{{cookiecutter.project_slug}}/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── api/                    # Public API interfaces
│   ├── core/                   # Core algorithms (Cython/Python dual implementation)
│   └── utils/                  # Utility functions
├── pyproject.toml              # Modern Python project configuration
├── setup.py                    # Cython build configuration
├── uv.lock                     # Dependency lock file
└── pyinstaller_build/          # Executable build scripts
```

## 🎯 Quick Start

### Prerequisites

- Python 3.10+
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or pip

### Generate Your Project

```bash
# Install cookiecutter if you haven't
pip install cookiecutter

# Generate your project
cookiecutter https://github.com/fastxteam/cookiecutter-fastx-cpython.git

# Follow the prompts to configure your project
```

### Development Setup

The template automatically sets up everything you need:

```bash
cd your_project_name

# If using uv (recommended)
uv sync
uv run python setup.py build_ext --inplace

# If using pip
pip install -e .
python setup.py build_ext --inplace

# Run your application
uv run python -m src.main
# or
python -m src.main
```

## 🔧 Cython Integration

This template provides a unique dual-implementation approach:

1. **Development**: Use Python implementation in `src/core/core.py`
2. **Production**: Cython implementation in `src/core/core.pyx` automatically compiled
3. **Smart Loading**: The `src/core/__init__.py` loader prioritizes compiled extensions: `.pyd > .so > .py > .pyx`

### Building Cython Extensions

```bash
# Build extensions
python setup.py build_ext --inplace

# Clean and rebuild
python setup.py clean --all
python setup.py build_ext --inplace --force
```

## 📦 Creating Executables

Build standalone executables with PyInstaller:

```bash
# Make the build script executable
chmod +x pyinstaller_build/build_exe.sh

# Build executable
./pyinstaller_build/build_exe.sh

# Find your executable in dist/
```

## 🧪 Development Workflow

### Adding Dependencies

```bash
# With uv
uv add package_name
uv add --dev pytest-mock  # Development dependency

# With pip
pip install package_name
pip freeze > requirements.txt
```

### Running Tests

```bash
# Run all tests
uv run pytest
# or
pytest

# With coverage
uv run pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
uv run black src/
uv run isort src/

# Lint
uv run flake8 src/

# Type checking
uv run mypy src/
```

## 📋 Template Options

When generating a project, you'll be prompted for:

- `project_name`: Human-readable project name
- `project_slug`: Package/directory name (must be valid Python identifier)
- `author_name`: Your name or organization
- `python_version`: Target Python version (3.10, 3.11, 3.12, 3.13)
- `include_cli`: Whether to include CLI interface (Typer)
- `include_pyinstaller`: Whether to include PyInstaller setup
- `include_vendor_auth_gate`: Whether to include vendor authentication

## 🚢 Deployment

### PyPI Publishing

The template includes GitHub Actions workflows for automatic PyPI publishing:

1. Push a new tag to trigger the release workflow
2. The package will be built and published to PyPI automatically

### Manual Publishing

```bash
# Build distribution
uv run python -m build

# Upload to PyPI
uv run twine upload dist/*
```

## 🛠️ Advanced Usage

### Custom Cython Configuration

Modify `setup.py` to add more Cython extensions:

```python
extensions = [
    Extension("core.algorithm", ["src/core/algorithm.pyx"]),
    Extension("utils.fast_math", ["src/utils/fast_math.pyx"]),
]
```

### PyInstaller Customization

Edit `pyinstaller_build/build_exe.sh` to:
- Add data files
- Include hidden imports
- Customize executable metadata
- Configure build options

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This template is released under the MIT License. See [LICENSE](LICENSE) for details.

## 🆘 Support

- 📖 **Documentation**: Check the generated project's README.md
- 🐛 **Issues**: [GitHub Issues](https://github.com/fastxteam/cookiecutter-fastx-cpython/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/fastxteam/cookiecutter-fastx-cpython/discussions)

## 🔄 Similar Templates

If this template doesn't fit your needs, check out these alternatives:
- [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) - General Python package template
- [cookiecutter-cython](https://github.com/danielcelis/cookiecutter-cython) - Cython-focused template
- [cookiecutter-pyinstaller](https://github.com/brentvollebregt/cookiecutter-pyinstaller) - PyInstaller-focused template

---

**Made with ❤️ by the FastX Team**
