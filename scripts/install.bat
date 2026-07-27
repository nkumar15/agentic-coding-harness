@echo off
rem Portable Agentic Coding Harness installer wrapper for classic cmd.exe.
rem Downloads install.ps1 and runs it through PowerShell, forwarding all arguments.
rem
rem Usage:
rem   install.bat --addon migration-workflow
rem   install.bat --source C:\path\to\package-dir-or-tarball.tar.gz

setlocal

set "REPO=%INSTALL_REPO%"
if "%REPO%"=="" set "REPO=nkumar15/agentic-coding-harness"

set "SCRIPT_URL=https://raw.githubusercontent.com/%REPO%/main/scripts/install.ps1"
set "TMP_PS1=%TEMP%\install-%RANDOM%.ps1"

powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%SCRIPT_URL%' -OutFile '%TMP_PS1%'"
if errorlevel 1 (
  echo Failed to download install.ps1 from %SCRIPT_URL% 1>&2
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%TMP_PS1%" %*
set "EXITCODE=%ERRORLEVEL%"
del /f /q "%TMP_PS1%" >nul 2>&1
exit /b %EXITCODE%
