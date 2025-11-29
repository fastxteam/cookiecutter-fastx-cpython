#!/bin/bash
# PyInstaller build script for {{ cookiecutter.project_name }}
# This script creates a standalone executable from the Python application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="{{ cookiecutter.project_slug }}"
PROJECT_VERSION="{{ cookiecutter.project_version }}"
MAIN_SCRIPT="src/main.py"
DIST_DIR="dist"
BUILD_DIR="build"
SPEC_FILE="${PROJECT_NAME}.spec"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if PyInstaller is available
check_pyinstaller() {
    if command -v pyinstaller &> /dev/null; then
        PYINSTALLER_CMD="pyinstaller"
    elif command -v uv &> /dev/null; then
        print_status "Using uv to run PyInstaller"
        PYINSTALLER_CMD="uv run pyinstaller"
    else
        print_error "PyInstaller not found. Please install it first:"
        print_error "  pip install pyinstaller"
        print_error "  or"
        print_error "  uv add --dev pyinstaller"
        exit 1
    fi
}

# Clean previous builds
clean_build() {
    print_status "Cleaning previous builds..."
    rm -rf "$BUILD_DIR" "$DIST_DIR" "$SPEC_FILE"
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
}

# Build Cython extensions
build_cython() {
    print_status "Building Cython extensions..."
    if command -v uv &> /dev/null; then
        uv run python setup.py build_ext --inplace
    else
        python setup.py build_ext --inplace
    fi
}

# Create PyInstaller command
create_executable() {
    print_status "Creating executable with PyInstaller..."

    # Base PyInstaller command
    PYINSTALLER_BASE="$PYINSTALLER_CMD --onefile --windowed"

    # Add name and version
    PYINSTALLER_BASE="$PYINSTALLER_BASE --name $PROJECT_NAME"

    # Add version info (if on Windows)
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        PYINSTALLER_BASE="$PYINSTALLER_BASE --version-file version_info.txt"
    fi

    # Add data files and hidden imports
    PYINSTALLER_CMD_FULL="$PYINSTALLER_BASE \
        --add-data 'src/core:core' \
        --hidden-import core.core \
        --hidden-import core \
        --hidden-import api \
        --hidden-import utils \
        --workpath $BUILD_DIR \
        --distpath $DIST_DIR \
        --specpath . \
        $MAIN_SCRIPT"

    print_status "Running: $PYINSTALLER_CMD_FULL"
    eval "$PYINSTALLER_CMD_FULL"
}

# Create version info file for Windows
create_version_info() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        print_status "Creating version info file..."
        cat > version_info.txt << EOF
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(${{ cookiecutter.project_version }}.replace('.', ',')}},0),
    prodvers=(${{ cookiecutter.project_version }}.replace('.', ',')}},0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{{ cookiecutter.author_name }}'),
        StringStruct(u'FileDescription', u'{{ cookiecutter.project_description }}'),
        StringStruct(u'FileVersion', u'{{ cookiecutter.project_version }}'),
        StringStruct(u'InternalName', u'$PROJECT_NAME'),
        StringStruct(u'LegalCopyright', u'Copyright (c) {{ cookiecutter.author_name }}'),
        StringStruct(u'OriginalFilename', u'$PROJECT_NAME.exe'),
        StringStruct(u'ProductName', u'{{ cookiecutter.project_name }}'),
        StringStruct(u'ProductVersion', u'{{ cookiecutter.project_version }}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
EOF
    fi
}

# Post-build cleanup
post_build() {
    print_status "Cleaning up build artifacts..."
    rm -rf "$BUILD_DIR"
    rm -f "$SPEC_FILE"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        rm -f version_info.txt
    fi
}

# Main execution
main() {
    print_status "Starting PyInstaller build for $PROJECT_NAME v$PROJECT_VERSION"

    # Check prerequisites
    check_pyinstaller

    # Clean previous builds
    clean_build

    # Build Cython extensions first
    build_cython

    # Create version info for Windows
    create_version_info

    # Create the executable
    create_executable

    # Clean up
    post_build

    print_status "Build completed successfully!"
    print_status "Executable location: $DIST_DIR/$PROJECT_NAME"

    # Show file info
    if [[ -f "$DIST_DIR/$PROJECT_NAME" ]]; then
        ls -lh "$DIST_DIR/$PROJECT_NAME"
    elif [[ -f "$DIST_DIR/$PROJECT_NAME.exe" ]]; then
        ls -lh "$DIST_DIR/$PROJECT_NAME.exe"
    fi
}

# Run main function
main "$@" "${@:2}" || {
    print_error "Build failed!"
    exit 1
}