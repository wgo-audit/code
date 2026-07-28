@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
if "%~1"=="" (
  set "TARGET_DIR=%CD%"
) else (
  set "TARGET_DIR=%~f1"
)

set "PLUGIN_NAME=wgo"
set "CODEX_DEST=%TARGET_DIR%\plugins\%PLUGIN_NAME%"
set "CLAUDE_COMMANDS_DEST=%TARGET_DIR%\.claude\commands"
set "CLAUDE_SKILLS_DEST=%TARGET_DIR%\.claude\skills"
set "PYTHON_VERSION=3.13.11"
set "PYTHON_MINOR=313"
set "PYMUPDF4LLM_PACKAGE=pymupdf4llm"
set "XPDF_VERSION=4.06"

if not exist "%SCRIPT_DIR%.codex-plugin\plugin.json" (
  echo Missing source path: %SCRIPT_DIR%.codex-plugin\plugin.json
  exit /b 1
)

if not exist "%SCRIPT_DIR%commands" (
  echo Missing source path: %SCRIPT_DIR%commands
  exit /b 1
)

if not exist "%SCRIPT_DIR%skills\%PLUGIN_NAME%\SKILL.md" (
  echo Missing source path: %SCRIPT_DIR%skills\%PLUGIN_NAME%\SKILL.md
  exit /b 1
)

echo Installing Whats.Going.On. into: %TARGET_DIR%
call :install_codegraph
call :install_pdftotext
call :install_pandoc
call :install_pymupdf4llm
if errorlevel 1 exit /b 1

echo Installing Codex plugin files...
if exist "%CODEX_DEST%" rmdir /s /q "%CODEX_DEST%"
mkdir "%CODEX_DEST%" >nul 2>nul
xcopy "%SCRIPT_DIR%.codex-plugin" "%CODEX_DEST%\.codex-plugin\" /E /I /Y >nul
if errorlevel 1 exit /b 1
xcopy "%SCRIPT_DIR%commands" "%CODEX_DEST%\commands\" /E /I /Y >nul
if errorlevel 1 exit /b 1
xcopy "%SCRIPT_DIR%skills" "%CODEX_DEST%\skills\" /E /I /Y >nul
if errorlevel 1 exit /b 1
del /s /q "%CODEX_DEST%\.DS_Store" >nul 2>nul

echo Installing Claude command and skill files...
mkdir "%CLAUDE_COMMANDS_DEST%" >nul 2>nul
mkdir "%CLAUDE_SKILLS_DEST%" >nul 2>nul
del /q "%CLAUDE_COMMANDS_DEST%\wgo_*.md" >nul 2>nul
copy /Y "%SCRIPT_DIR%commands\onboard.md" "%CLAUDE_COMMANDS_DEST%\wgo_onboard.md" >nul
if errorlevel 1 exit /b 1
copy /Y "%SCRIPT_DIR%commands\audit.md" "%CLAUDE_COMMANDS_DEST%\wgo_audit.md" >nul
if errorlevel 1 exit /b 1
copy /Y "%SCRIPT_DIR%commands\status.md" "%CLAUDE_COMMANDS_DEST%\wgo_status.md" >nul
if errorlevel 1 exit /b 1
copy /Y "%SCRIPT_DIR%commands\summarize.md" "%CLAUDE_COMMANDS_DEST%\wgo_summarize.md" >nul
if errorlevel 1 exit /b 1
copy /Y "%SCRIPT_DIR%commands\operationalize.md" "%CLAUDE_COMMANDS_DEST%\wgo_operationalize.md" >nul
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "(Get-Content '%CLAUDE_COMMANDS_DEST%\wgo_onboard.md') -replace '^name: onboard$', 'name: wgo_onboard' | Set-Content '%CLAUDE_COMMANDS_DEST%\wgo_onboard.md'"
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "(Get-Content '%CLAUDE_COMMANDS_DEST%\wgo_audit.md') -replace '^name: audit$', 'name: wgo_audit' | Set-Content '%CLAUDE_COMMANDS_DEST%\wgo_audit.md'"
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "(Get-Content '%CLAUDE_COMMANDS_DEST%\wgo_status.md') -replace '^name: status$', 'name: wgo_status' | Set-Content '%CLAUDE_COMMANDS_DEST%\wgo_status.md'"
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "(Get-Content '%CLAUDE_COMMANDS_DEST%\wgo_summarize.md') -replace '^name: summarize$', 'name: wgo_summarize' | Set-Content '%CLAUDE_COMMANDS_DEST%\wgo_summarize.md'"
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "(Get-Content '%CLAUDE_COMMANDS_DEST%\wgo_operationalize.md') -replace '^name: operationalize$', 'name: wgo_operationalize' | Set-Content '%CLAUDE_COMMANDS_DEST%\wgo_operationalize.md'"
if errorlevel 1 exit /b 1
if exist "%CLAUDE_SKILLS_DEST%\%PLUGIN_NAME%" rmdir /s /q "%CLAUDE_SKILLS_DEST%\%PLUGIN_NAME%"
xcopy "%SCRIPT_DIR%skills\%PLUGIN_NAME%" "%CLAUDE_SKILLS_DEST%\%PLUGIN_NAME%\" /E /I /Y >nul
if errorlevel 1 exit /b 1
del /s /q "%CLAUDE_SKILLS_DEST%\%PLUGIN_NAME%\.DS_Store" >nul 2>nul

echo.
echo Whats.Going.On. installed.
echo.
echo Codex:
echo   %CODEX_DEST%
echo.
echo Claude:
echo   %CLAUDE_COMMANDS_DEST%\wgo_*.md
echo   %CLAUDE_SKILLS_DEST%\%PLUGIN_NAME%
echo.
echo PDF extraction:
echo   PyMuPDF4LLM is optional. If installed, restart Codex or Claude before using it.
echo.
echo Optional audit tools:
echo   CodeGraph, pdftotext, and Pandoc are used when available; declined or failed
echo   installations leave their built-in WGO fallbacks in place.
echo.
echo Next:
echo   In Codex, run wgo:onboard to start an audit.
echo   In Claude, run /wgo_onboard to start an audit.
echo   After a completed synthesis, run wgo:operationalize or /wgo_operationalize only with explicit auditor approval.

endlocal
exit /b 0

:ask_to_install
echo.
echo %~1
echo WHY: %~2
echo WITHOUT IT: %~3
set "INSTALL_TOOL="
set /p "INSTALL_TOOL=Install %~4? [y/N] "
if /i "%INSTALL_TOOL%"=="y" exit /b 0
exit /b 1

:install_codegraph
where codegraph >nul 2>nul
if not errorlevel 1 (
  echo CodeGraph is already available.
  exit /b 0
)
call :ask_to_install "CodeGraph — code topology" "Maps symbols, callers, dependencies, and code paths so agents navigate implementation accurately and efficiently." "WGO spends more tokens navigating code. Broad repositories take longer to audit, and some topology relationships may receive less coverage." "CodeGraph"
if errorlevel 1 exit /b 0
echo Installing CodeGraph...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$installer = Join-Path $env:TEMP 'wgo-codegraph-install.ps1'; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1' -OutFile $installer; & $installer"
if errorlevel 1 echo CodeGraph installation failed; WGO will use direct code navigation. >&2
exit /b 0

:install_pdftotext
where pdftotext >nul 2>nul
if not errorlevel 1 (
  echo pdftotext is already available.
  exit /b 0
)
call :ask_to_install "pdftotext — PDF discovery" "Converts PDFs to searchable text for fast, repeatable search and evidence discovery." "WGO uses the agent's built-in conversion where available. This consumes more tokens and time; complex layouts or tables can be less reliable, and a file may be converted more than once." "pdftotext"
if errorlevel 1 exit /b 0
echo Installing pdftotext from the official Xpdf tools distribution...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$archive = Join-Path $env:TEMP 'xpdf-tools-win-%XPDF_VERSION%.zip'; $expanded = Join-Path $env:TEMP 'xpdf-tools-win-%XPDF_VERSION%'; $destination = Join-Path $env:LOCALAPPDATA 'WGO\bin'; Invoke-WebRequest -Uri 'https://dl.xpdfreader.com/xpdf-tools-win-%XPDF_VERSION%.zip' -OutFile $archive; Expand-Archive -Path $archive -DestinationPath $expanded -Force; $source = Get-ChildItem -Path $expanded -Recurse -Filter pdftotext.exe | Select-Object -First 1; if ($null -eq $source) { throw 'pdftotext.exe was not found' }; New-Item -ItemType Directory -Force -Path $destination | Out-Null; Copy-Item $source.FullName (Join-Path $destination 'pdftotext.exe') -Force; $path = [Environment]::GetEnvironmentVariable('Path', 'User'); if (($path -split ';') -notcontains $destination) { [Environment]::SetEnvironmentVariable('Path', ($path.TrimEnd(';') + ';' + $destination), 'User') }"
if errorlevel 1 echo pdftotext installation failed; WGO will use its PDF fallback. >&2
exit /b 0

:install_pandoc
where pandoc >nul 2>nul
if not errorlevel 1 (
  echo Pandoc is already available.
  exit /b 0
)
call :ask_to_install "Pandoc — Office-document discovery" "Converts DOCX, PPTX, XLSX, HTML, and markup to Markdown to quickly and efficiently do searches and evidence discovery." "WGO uses the agent's built-in conversion if the format is supported. This consumes more tokens and time; coverage and cross-document search can be weaker, and a file may be converted more than once." "Pandoc"
if errorlevel 1 exit /b 0
where winget >nul 2>nul
if errorlevel 1 (
  echo Pandoc needs Windows Package Manager. It was not installed; WGO will use its document fallback. >&2
  exit /b 0
)
winget install --source winget --exact --id JohnMacFarlane.Pandoc --accept-package-agreements --accept-source-agreements
if errorlevel 1 echo Pandoc installation failed; WGO will use its document fallback. >&2
exit /b 0

:find_python
set "PYTHON_EXE="
set "PYTHON_ARGS="
where python >nul 2>nul
if not errorlevel 1 set "PYTHON_EXE=python"
if defined PYTHON_EXE exit /b 0
where py >nul 2>nul
if not errorlevel 1 (
  set "PYTHON_EXE=py"
  set "PYTHON_ARGS=-3"
)
exit /b 0

:install_python_from_python_org
set "PYTHON_ARCH=amd64"
if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "PYTHON_ARCH=arm64"
echo Installing Python %PYTHON_VERSION% from python.org...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$installer = Join-Path $env:TEMP 'python-%PYTHON_VERSION%-%PYTHON_ARCH%.exe'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-%PYTHON_ARCH%.exe' -OutFile $installer; Start-Process -FilePath $installer -ArgumentList @('/quiet', 'InstallAllUsers=0', 'PrependPath=1', 'Include_pip=1') -Verb RunAs -Wait"
if errorlevel 1 (
  echo Python installation did not complete. Install it from https://www.python.org/downloads/ and rerun this installer. >&2
  exit /b 1
)
set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python%PYTHON_MINOR%\python.exe"
set "PYTHON_ARGS="
if not exist "%PYTHON_EXE%" (
  echo Python was installed but is not available in this shell. Restart the terminal and rerun this installer. >&2
  exit /b 1
)
exit /b 0

:install_pymupdf4llm
call :find_python
if defined PYTHON_EXE (
  "%PYTHON_EXE%" %PYTHON_ARGS% -c "import pymupdf4llm" >nul 2>nul
  if not errorlevel 1 (
    echo PyMuPDF4LLM is already available.
    exit /b 0
  )
)

call :ask_to_install "PyMuPDF4LLM — enhanced PDF extraction (will install required Python distribution)" "Converts complex PDFs, including tables and visual layouts, into more reliable Markdown for evidence discovery." "WGO uses its built-in PDF conversion. This consumes more tokens and time; complex layouts or tables can be less reliable." "PyMuPDF4LLM"
if errorlevel 1 (
  echo PyMuPDF4LLM was not installed; WGO will use its PDF fallback.
  exit /b 0
)

if not defined PYTHON_EXE call :install_python_from_python_org
if errorlevel 1 exit /b 0

echo Installing PyMuPDF4LLM...
"%PYTHON_EXE%" %PYTHON_ARGS% -m pip install --user "%PYMUPDF4LLM_PACKAGE%"
if errorlevel 1 echo PyMuPDF4LLM installation failed. WGO will use its PDF fallback. >&2
exit /b 0
