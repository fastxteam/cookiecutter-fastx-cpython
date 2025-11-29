@echo on
setlocal enabledelayedexpansion

echo.
echo ---------------------------------------------------------
echo   Running {{cookiecutter.project_slug}}  (Batch Launcher)
echo ---------------------------------------------------------
echo.

REM =========================================================
REM Configuration
REM =========================================================
set "target_dir=%~dp0Input"
set "file_pattern=*.xlsx"
set "logfile=%~dp0{{cookiecutter.project_slug}}_run.log"

REM Write start time to log
echo [%date% %time%] Script started >> "%logfile%"

REM =========================================================
REM Check if EXE exists
REM =========================================================
if not exist "{{cookiecutter.project_slug}}.exe" (
    echo [ERROR] Executable "{{cookiecutter.project_slug}}.exe" not found!
    echo [ERROR] Please verify the installation.
    echo [%date% %time%] Executable not found >> "%logfile%"
    pause
    exit /b 2
)

REM =========================================================
REM Find the first Excel file
REM =========================================================
for /f "delims=" %%F in ('dir /b /a-d "%target_dir%\%file_pattern%" 2^>nul') do (
    set "first_file=%%F"
    goto :break
)

:break
if not defined first_file (
    echo [ERROR] No Excel file found in "%target_dir%"
    echo [%date% %time%] No Excel file found >> "%logfile%"
    pause
    exit /b 1
)

echo [INFO] Found file: !first_file!
echo [%date% %time%] Found file: !first_file! >> "%logfile%"

REM =========================================================
REM Run the main program with logging
REM =========================================================
echo [INFO] Executing program...
echo [%date% %time%] Executing program... >> "%logfile%"

{{cookiecutter.project_slug}}.exe ^
    --InpXlsx="%target_dir%\!first_file!" ^
    >> "%logfile%" 2>&1

echo [INFO] Done.
echo [%date% %time%] Execution completed >> "%logfile%"

echo.
pause
exit /b 0
