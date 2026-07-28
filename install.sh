#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$(pwd)}"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

PLUGIN_NAME="wgo"
CODEX_DEST="$TARGET_DIR/plugins/$PLUGIN_NAME"
CLAUDE_COMMANDS_DEST="$TARGET_DIR/.claude/commands"
CLAUDE_SKILLS_DEST="$TARGET_DIR/.claude/skills"
PYTHON_VERSION="3.13.11"
PYTHON_MINOR="3.13"
PYMUPDF4LLM_PACKAGE="pymupdf4llm"
XPDF_VERSION="4.06"

require_source() {
  local path="$1"
  if [[ ! -e "$SCRIPT_DIR/$path" ]]; then
    echo "Missing source path: $SCRIPT_DIR/$path" >&2
    exit 1
  fi
}

copy_dir() {
  local src="$1"
  local dest="$2"
  rm -rf "$dest"
  mkdir -p "$(dirname "$dest")"
  cp -R "$src" "$dest"
}

find_python() {
  local candidate
  for candidate in python3 "python${PYTHON_MINOR}" python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      command -v "$candidate"
      return 0
    fi
  done
  return 1
}

ask_to_install() {
  local name="$1" why="$2" without="$3" answer

  printf '\n%s\nWHY: %s\nWITHOUT IT: %s\n' "$name" "$why" "$without"
  read -r -p "Install ${name%% —*}? [y/N] " answer || answer="n"
  [[ "$answer" =~ ^[Yy]$ ]]
}

install_codegraph() {
  local installer

  if command -v codegraph >/dev/null 2>&1; then
    echo "CodeGraph is already available."
    return
  fi
  ask_to_install \
    "CodeGraph — code topology" \
    "Maps symbols, callers, dependencies, and code paths so agents navigate implementation accurately and efficiently." \
    "WGO spends more tokens navigating code. Broad repositories take longer to audit, and some topology relationships may receive less coverage." || return 0

  installer="$(mktemp)"
  echo "Installing CodeGraph..."
  if ! curl -fL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh -o "$installer" || ! sh "$installer"; then
    echo "CodeGraph installation failed; WGO will use direct code navigation." >&2
  fi
  rm -f "$installer"
}

install_pdftotext() {
  local temp_dir archive source

  if command -v pdftotext >/dev/null 2>&1; then
    echo "pdftotext is already available."
    return
  fi
  ask_to_install \
    "pdftotext — PDF discovery" \
    "Converts PDFs to searchable text for fast, repeatable search and evidence discovery." \
    "WGO uses the agent's built-in conversion where available. This consumes more tokens and time; complex layouts or tables can be less reliable, and a file may be converted more than once." || return 0

  if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "Automatic pdftotext installation is supported on macOS only; WGO will use its PDF fallback." >&2
    return
  fi
  temp_dir="$(mktemp -d)"
  archive="$temp_dir/xpdf-tools-mac-${XPDF_VERSION}.tar.gz"
  echo "Installing pdftotext from the official Xpdf tools distribution..."
  if ! curl -fL "https://dl.xpdfreader.com/xpdf-tools-mac-${XPDF_VERSION}.tar.gz" -o "$archive" || ! tar -xzf "$archive" -C "$temp_dir"; then
    rm -rf "$temp_dir"
    echo "pdftotext installation failed; WGO will use its PDF fallback." >&2
    return
  fi
  source="$(find "$temp_dir" -type f -name pdftotext -print -quit)"
  if [[ -z "$source" ]] || ! sudo install -m 755 "$source" /usr/local/bin/pdftotext; then
    rm -rf "$temp_dir"
    echo "pdftotext installation failed; WGO will use its PDF fallback." >&2
    return
  fi
  rm -rf "$temp_dir"
}

install_pandoc() {
  if command -v pandoc >/dev/null 2>&1; then
    echo "Pandoc is already available."
    return
  fi
  ask_to_install \
    "Pandoc — Office-document discovery" \
    "Converts DOCX, PPTX, XLSX, HTML, and markup to Markdown to quickly and efficiently do searches and evidence discovery." \
    "WGO uses the agent's built-in conversion if the format is supported. This consumes more tokens and time; coverage and cross-document search can be weaker, and a file may be converted more than once." || return 0

  if ! command -v brew >/dev/null 2>&1; then
    echo "Pandoc needs Homebrew on macOS. It was not installed; WGO will use its document fallback." >&2
    return
  fi
  if ! brew install pandoc; then
    echo "Pandoc installation failed; WGO will use its document fallback." >&2
  fi
}

install_python_from_python_org() {
  local temp_dir package

  if ! command -v curl >/dev/null 2>&1; then
    echo "Cannot install Python: curl is unavailable. Install Python from https://www.python.org/downloads/ and rerun this installer." >&2
    return 1
  fi

  temp_dir="$(mktemp -d)"
  package="$temp_dir/python-${PYTHON_VERSION}-macos11.pkg"
  echo "Installing Python ${PYTHON_VERSION} from python.org..."
  if ! curl -fL "https://www.python.org/ftp/python/${PYTHON_VERSION}/python-${PYTHON_VERSION}-macos11.pkg" -o "$package" || ! sudo installer -pkg "$package" -target /; then
    rm -rf "$temp_dir"
    echo "Python installation did not complete. Install it from https://www.python.org/downloads/ and rerun this installer." >&2
    return 1
  fi
  rm -rf "$temp_dir"
}

install_pymupdf4llm() {
  local python_bin

  if python_bin="$(find_python)" && "$python_bin" -c "import pymupdf4llm" >/dev/null 2>&1; then
    echo "PyMuPDF4LLM is already available."
    return
  fi

  if ! ask_to_install \
    "PyMuPDF4LLM — enhanced PDF extraction (will install required Python distribution)" \
    "Converts complex PDFs, including tables and visual layouts, into more reliable Markdown for evidence discovery." \
    "WGO uses its built-in PDF conversion. This consumes more tokens and time; complex layouts or tables can be less reliable."; then
    echo "PyMuPDF4LLM was not installed; WGO will use its PDF fallback."
    return
  fi

  if ! python_bin="$(find_python)"; then
    install_python_from_python_org || return
    python_bin="$(find_python)" || {
      echo "Python was installed but is not available in this shell. Restart the terminal and rerun this installer." >&2
      return
    }
  fi

  echo "Installing PyMuPDF4LLM..."
  if ! "$python_bin" -m pip install --user "$PYMUPDF4LLM_PACKAGE"; then
    echo "PyMuPDF4LLM installation failed. WGO will use its PDF fallback." >&2
  fi
}

require_source ".codex-plugin/plugin.json"
require_source "commands"
require_source "skills/$PLUGIN_NAME/SKILL.md"

echo "Installing Whats.Going.On. into: $TARGET_DIR"
install_codegraph
install_pdftotext
install_pandoc
install_pymupdf4llm

echo "Installing Codex plugin files..."
rm -rf "$CODEX_DEST"
mkdir -p "$CODEX_DEST"
copy_dir "$SCRIPT_DIR/.codex-plugin" "$CODEX_DEST/.codex-plugin"
copy_dir "$SCRIPT_DIR/commands" "$CODEX_DEST/commands"
copy_dir "$SCRIPT_DIR/skills" "$CODEX_DEST/skills"
find "$CODEX_DEST" -name ".DS_Store" -type f -delete

echo "Installing Claude command and skill files..."
mkdir -p "$CLAUDE_COMMANDS_DEST" "$CLAUDE_SKILLS_DEST"
rm -f "$CLAUDE_COMMANDS_DEST"/wgo_*.md
cp "$SCRIPT_DIR/commands/onboard.md" "$CLAUDE_COMMANDS_DEST/wgo_onboard.md"
cp "$SCRIPT_DIR/commands/audit.md" "$CLAUDE_COMMANDS_DEST/wgo_audit.md"
cp "$SCRIPT_DIR/commands/status.md" "$CLAUDE_COMMANDS_DEST/wgo_status.md"
cp "$SCRIPT_DIR/commands/summarize.md" "$CLAUDE_COMMANDS_DEST/wgo_summarize.md"
cp "$SCRIPT_DIR/commands/operationalize.md" "$CLAUDE_COMMANDS_DEST/wgo_operationalize.md"
sed -i.bak 's/^name: onboard$/name: wgo_onboard/' "$CLAUDE_COMMANDS_DEST/wgo_onboard.md" && rm -f "$CLAUDE_COMMANDS_DEST/wgo_onboard.md.bak"
sed -i.bak 's/^name: audit$/name: wgo_audit/' "$CLAUDE_COMMANDS_DEST/wgo_audit.md" && rm -f "$CLAUDE_COMMANDS_DEST/wgo_audit.md.bak"
sed -i.bak 's/^name: status$/name: wgo_status/' "$CLAUDE_COMMANDS_DEST/wgo_status.md" && rm -f "$CLAUDE_COMMANDS_DEST/wgo_status.md.bak"
sed -i.bak 's/^name: summarize$/name: wgo_summarize/' "$CLAUDE_COMMANDS_DEST/wgo_summarize.md" && rm -f "$CLAUDE_COMMANDS_DEST/wgo_summarize.md.bak"
sed -i.bak 's/^name: operationalize$/name: wgo_operationalize/' "$CLAUDE_COMMANDS_DEST/wgo_operationalize.md" && rm -f "$CLAUDE_COMMANDS_DEST/wgo_operationalize.md.bak"
copy_dir "$SCRIPT_DIR/skills/$PLUGIN_NAME" "$CLAUDE_SKILLS_DEST/$PLUGIN_NAME"
find "$CLAUDE_SKILLS_DEST/$PLUGIN_NAME" -name ".DS_Store" -type f -delete

cat <<EOF

Whats.Going.On. installed.

Codex:
  $CODEX_DEST

Claude:
  $CLAUDE_COMMANDS_DEST/wgo_*.md
  $CLAUDE_SKILLS_DEST/$PLUGIN_NAME

PDF extraction:
  PyMuPDF4LLM is optional. If installed, restart Codex or Claude before using it.

Optional audit tools:
  CodeGraph, pdftotext, and Pandoc are used when available; declined or failed
  installations leave their built-in WGO fallbacks in place.

Next:
  In Codex, run wgo:onboard to start an audit.
  In Claude, run /wgo_onboard to start an audit.
  After a completed synthesis, run wgo:operationalize or /wgo_operationalize only with explicit auditor approval.
EOF
