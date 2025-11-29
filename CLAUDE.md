# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Cookiecutter template for creating high-performance Python projects that utilize Cython for compiled extensions and PyInstaller for executable packaging. The template generates projects with a specific architecture optimized for performance-critical applications.

## Key Architecture

### Generated Project Structure
```
{{cookiecutter.project_slug}}/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── api/                    # Public API interfaces
│   │   ├── api.py              # Main API implementation
│   │   └── __init__.py
│   ├── core/                   # Core algorithms (Cython/Python)
│   │   ├── core.pyx            # Cython implementation (production)
│   │   ├── core.py             # Python fallback (development)
│   │   └── __init__.py         # Smart loading mechanism
│   └── utils/                  # Utility functions
├── .venv/                      # Auto-created virtual environment
├── pyinstaller_build/          # Executable build scripts
└── .python-version            # Python version specification
```

### Core Loading Priority
The template implements a smart loading mechanism in `src/core/__init__.py` that prioritizes compiled extensions:
`.pyd > .so > .py > .pyx`

This allows seamless switching between development (Python) and production (Cython) implementations.

## Development Commands

### Template Usage
```bash
# Generate a new project from template
cookiecutter https://github.com/fastxteam/cookiecutter-fastx-cpython.git

# Post-generation automatically:
# - Creates .venv with correct Python version
# - Installs Cython and dependencies
# - Sets up Git repository
# - Installs project in editable mode
```

### Working with Generated Projects
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies (uv preferred, pip fallback)
uv sync                    # If uv available
pip install -e .          # Editable install

# Build Cython extensions
python setup.py build_ext --inplace

# Create executable with PyInstaller
./pyinstaller_build/build_exe.sh
```

## Critical Implementation Notes

### Cython Integration
- Core algorithms should be implemented in `src/core/core.pyx`
- Python fallback provided in `src/core/core.py` for development
- The `__init__.py` loader automatically selects the best available version
- Cython files compile to `.pyd` (Windows) or `.so` (Linux/Mac) extensions

### Missing Development Infrastructure
The template currently lacks several modern Python development tools:
- No testing framework (pytest mentioned but not configured)
- No CI/CD workflows (GitHub Actions mentioned but missing)
- Build configuration files are staged for deletion
- No linting/formatting tools configured
- No documentation generation setup

### Template Configuration
Key variables in `cookiecutter.json`:
- `project_name`: Human-readable project name
- `project_slug`: Package/directory name (must be valid Python identifier)
- `python_version`: Target Python version (3.10, 3.11, 3.12, 3.13)
- `include_cli`: Whether to include CLI interface
- `include_pyinstaller`: Whether to include PyInstaller setup
- `include_vendor_auth_gate`: Whether to include vendor authentication

## Common Tasks

### Adding New Cython Functions
1. Implement in `src/core/core.pyx`
2. Add Python fallback in `src/core/core.py` if needed
3. Export through `src/core/__init__.py`
4. Build with `python setup.py build_ext --inplace`

### Creating PyInstaller Executables
The `pyinstaller_build/build_exe.sh` script should be customized for your specific application requirements.

### Template Development
When modifying the template itself:
- Test changes by generating new projects
- Ensure hooks work correctly (pre/post generation)
- Validate cookiecutter.json syntax
- Check that template variables render correctly