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
set "CLAUDE_PLUGIN_DEST=%TARGET_DIR%\.claude\skills\%PLUGIN_NAME%-claude"
set "LEGACY_CLAUDE_COMMANDS_DEST=%TARGET_DIR%\.claude\commands"
set "LEGACY_CLAUDE_SKILL_DEST=%TARGET_DIR%\.claude\skills\%PLUGIN_NAME%"
set "OPENCODE_COMMANDS_DEST=%TARGET_DIR%\.opencode\commands"
set "OPENCODE_SKILL_DEST=%TARGET_DIR%\.opencode\skills\%PLUGIN_NAME%"
set "PYTHON_VERSION=3.13.11"
set "PYTHON_MINOR=313"
set "PYMUPDF4LLM_PACKAGE=pymupdf4llm"
set "XPDF_VERSION=4.06"

if not exist "%SCRIPT_DIR%.codex-plugin\plugin.json" (
  echo Missing source path: %SCRIPT_DIR%.codex-plugin\plugin.json
  exit /b 1
)

if not exist "%SCRIPT_DIR%.claude-plugin\plugin.json" (
  echo Missing source path: %SCRIPT_DIR%.claude-plugin\plugin.json
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
call :filter_frontmatter codex "%SCRIPT_DIR%skills\%PLUGIN_NAME%\SKILL.md" "%CODEX_DEST%\skills\%PLUGIN_NAME%\SKILL.md"
if errorlevel 1 exit /b 1
for %%F in ("%SCRIPT_DIR%commands\*.md") do (
  call :filter_frontmatter codex "%%~fF" "%CODEX_DEST%\commands\%%~nxF"
  if errorlevel 1 exit /b 1
)
del /s /q "%CODEX_DEST%\.DS_Store" >nul 2>nul

echo Installing Claude plugin files...
for %%C in (onboard audit status summarize operationalize) do del /q "%LEGACY_CLAUDE_COMMANDS_DEST%\wgo_%%C.md" >nul 2>nul
if exist "%LEGACY_CLAUDE_SKILL_DEST%" rmdir /s /q "%LEGACY_CLAUDE_SKILL_DEST%"
if exist "%CLAUDE_PLUGIN_DEST%" rmdir /s /q "%CLAUDE_PLUGIN_DEST%"
mkdir "%CLAUDE_PLUGIN_DEST%" >nul 2>nul
xcopy "%SCRIPT_DIR%.claude-plugin" "%CLAUDE_PLUGIN_DEST%\.claude-plugin\" /E /I /Y >nul
if errorlevel 1 exit /b 1
xcopy "%SCRIPT_DIR%commands" "%CLAUDE_PLUGIN_DEST%\commands\" /E /I /Y >nul
if errorlevel 1 exit /b 1
xcopy "%SCRIPT_DIR%skills\%PLUGIN_NAME%\references" "%CLAUDE_PLUGIN_DEST%\references\" /E /I /Y >nul
if errorlevel 1 exit /b 1
xcopy "%SCRIPT_DIR%skills\%PLUGIN_NAME%\scripts" "%CLAUDE_PLUGIN_DEST%\scripts\" /E /I /Y >nul
if errorlevel 1 exit /b 1
call :filter_frontmatter claude "%SCRIPT_DIR%skills\%PLUGIN_NAME%\SKILL.md" "%CLAUDE_PLUGIN_DEST%\SKILL.md"
if errorlevel 1 exit /b 1
for %%F in ("%SCRIPT_DIR%commands\*.md") do (
  call :filter_frontmatter claude "%%~fF" "%CLAUDE_PLUGIN_DEST%\commands\%%~nxF"
  if errorlevel 1 exit /b 1
)
del /s /q "%CLAUDE_PLUGIN_DEST%\.DS_Store" >nul 2>nul

echo Installing OpenCode command files...
mkdir "%OPENCODE_COMMANDS_DEST%" >nul 2>nul
for %%C in (onboard audit status summarize operationalize) do (
  del /q "%OPENCODE_COMMANDS_DEST%\wgo-%%C.md" >nul 2>nul
  call :filter_frontmatter opencode-command "%SCRIPT_DIR%commands\%%C.md" "%OPENCODE_COMMANDS_DEST%\wgo-%%C.md"
  if errorlevel 1 exit /b 1
)
if exist "%OPENCODE_SKILL_DEST%" rmdir /s /q "%OPENCODE_SKILL_DEST%"
mkdir "%OPENCODE_SKILL_DEST%" >nul 2>nul
xcopy "%SCRIPT_DIR%skills\%PLUGIN_NAME%\references" "%OPENCODE_SKILL_DEST%\references\" /E /I /Y >nul
if errorlevel 1 exit /b 1
xcopy "%SCRIPT_DIR%skills\%PLUGIN_NAME%\scripts" "%OPENCODE_SKILL_DEST%\scripts\" /E /I /Y >nul
if errorlevel 1 exit /b 1
call :filter_frontmatter opencode-skill "%SCRIPT_DIR%skills\%PLUGIN_NAME%\SKILL.md" "%OPENCODE_SKILL_DEST%\SKILL.md"
if errorlevel 1 exit /b 1
del /s /q "%OPENCODE_SKILL_DEST%\.DS_Store" >nul 2>nul

echo.
echo Whats.Going.On. installed.
echo.
echo Codex:
echo   %CODEX_DEST%
echo.
echo Claude:
echo   %CLAUDE_PLUGIN_DEST%
echo.
echo OpenCode:
echo   %OPENCODE_COMMANDS_DEST%\wgo-*.md
echo   %OPENCODE_SKILL_DEST%
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
echo   In Claude, run /wgo:onboard to start an audit.
echo   In OpenCode, run /wgo-onboard to start an audit.
echo   After a completed synthesis, use the provider's WGO operationalize command only with explicit auditor approval.

endlocal
exit /b 0

:filter_frontmatter
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%scripts\filter-frontmatter.ps1" -Provider "%~1" -Source "%~2" -Destination "%~3"
exit /b %errorlevel%

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
