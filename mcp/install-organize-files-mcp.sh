#!/usr/bin/env bash
# Install the Organize Files MCP connector for AI assistants (Claude, Cursor, VS Code, etc.) on
# Linux and macOS, in a Python environment of its own. Running it again upgrades that environment.
#
#   ORGANIZE_FILES_MCP_PYTHON  use this interpreter and no other (Python 3.10 or newer)
#   ORGANIZE_FILES_MCP_HOME    where the environment goes (default ~/.local/share/organize-files-mcp)
#
# It never uses sudo. When something has to be installed system-wide first, it prints the command
# and stops.
set -eu

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS="$(uname -s)"

is_debian_like() {
  [ -f /etc/debian_version ] && return 0
  [ -r /etc/os-release ] && grep -qiE '^(ID|ID_LIKE)=.*(debian|ubuntu)' /etc/os-release && return 0
  return 1
}

# The interpreter reports its own version. A name such as python3.12 on PATH proves nothing.
python_ok() {
  "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1
}

python_version() {
  "$1" -c 'import platform; print(platform.python_version())' 2>/dev/null || echo "not runnable"
}

no_python() {
  echo "" >&2
  echo "Organize Files MCP needs Python 3.10 or newer, and none was found." >&2
  if [ -n "${1:-}" ]; then
    echo "$1" >&2
  fi
  if [ "$OS" = "Darwin" ]; then
    echo "Next step: install Python 3.12 from https://www.python.org/downloads/macos/ and run this script again." >&2
  elif is_debian_like; then
    if command -v python3 >/dev/null 2>&1; then
      echo "Next step: python3 here is $(python_version python3). Install Python 3.10 or newer from your distribution, then run this script again." >&2
    else
      echo "Next step: sudo apt install python3" >&2
      echo "Then run this script again." >&2
    fi
  else
    echo "Next step: install Python 3.10 or newer with your system's package manager, then run this script again." >&2
  fi
  exit 1
}

PY=""
if [ -n "${ORGANIZE_FILES_MCP_PYTHON:-}" ]; then
  if python_ok "$ORGANIZE_FILES_MCP_PYTHON"; then
    PY="$ORGANIZE_FILES_MCP_PYTHON"
  else
    no_python "ORGANIZE_FILES_MCP_PYTHON=$ORGANIZE_FILES_MCP_PYTHON is $(python_version "$ORGANIZE_FILES_MCP_PYTHON"). Point it at Python 3.10 or newer, or unset it."
  fi
else
  for candidate in python3.13 python3.12 python3.11 python3.10 /usr/local/bin/python3 python3; do
    if command -v "$candidate" >/dev/null 2>&1 && python_ok "$candidate"; then
      PY="$(command -v "$candidate")"
      break
    fi
  done
  if [ -z "$PY" ]; then
    no_python ""
  fi
fi
PY="$("$PY" -c 'import sys; print(sys.executable)')"

VENV="${ORGANIZE_FILES_MCP_HOME:-$HOME/.local/share/organize-files-mcp}"
VENV="$("$PY" -c 'import os, sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$VENV")"
VENV_PYTHON="$VENV/bin/python"

if [ -e "$VENV" ] && [ ! -f "$VENV/pyvenv.cfg" ] && [ -n "$(ls -A "$VENV" 2>/dev/null)" ]; then
  echo "$VENV exists and is not a Python environment. Set ORGANIZE_FILES_MCP_HOME to another folder." >&2
  exit 1
fi

if "$VENV_PYTHON" -m pip --version >/dev/null 2>&1; then
  echo "Upgrading the environment at $VENV"
else
  existed=0
  if [ -e "$VENV" ]; then
    existed=1
  fi
  echo "Creating the environment at $VENV with $PY ($(python_version "$PY"))"
  if ! venv_output="$("$PY" -m venv --clear "$VENV" 2>&1)"; then
    if [ "$existed" = 0 ]; then
      rm -rf "$VENV"
    fi
    echo "" >&2
    echo "$venv_output" >&2
    echo "" >&2
    echo "Python could not create the environment." >&2
    if is_debian_like; then
      # Debian's venv names the package it misses, for example "apt install python3.14-venv".
      package="$(printf '%s\n' "$venv_output" | sed -n 's/.*apt install \([A-Za-z0-9.+-]*\).*/\1/p' | head -n 1)"
      echo "Next step: sudo apt install ${package:-python3-venv}" >&2
      echo "Then run this script again." >&2
    fi
    exit 1
  fi
fi

"$VENV_PYTHON" -m pip install --upgrade --prefer-binary --disable-pip-version-check "$ROOT"

# Load the server itself, with -I so the source folder next to this script cannot stand in for the
# installed copy. Importing cli_runner alone passed on installs whose MCP library could not load it.
if ! "$VENV_PYTHON" -I -c 'import organize_files_mcp.server'; then
  echo "" >&2
  echo "The connector was installed but does not load. The error is above." >&2
  exit 1
fi

echo ""
echo "Organize Files MCP is installed in $VENV"
echo ""
echo "The AI app starts it with this Python, by its full path:"
echo "  \"command\": \"$VENV_PYTHON\","
echo "  \"args\": [\"-m\", \"organize_files_mcp\"]"
echo ""
echo "Configure the AI client from MCP setup in the Organize Files app. The AI assistant (MCP) chapter of its Documentation has every step."
echo "Examples: $ROOT/examples/"
echo ""
echo "Check the install at any time:"
echo "  \"$VENV_PYTHON\" -I -c \"import organize_files_mcp.server; print('ok')\""
