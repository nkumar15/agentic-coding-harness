#!/bin/sh
# Portable Agentic Coding Harness installer.
#
# Usage:
#   curl -fsSL <install-url> | sh
#   curl -fsSL <install-url> | sh -s -- --addon migration-workflow
#
# Testing/offline usage:
#   sh install.sh --source /path/to/package-dir-or-tarball.tar.gz
#   sh install.sh --addon-source /path/to/addon-dir-or-tarball.tar.gz
#
# Env overrides: INSTALL_REPO (default nkumar15/agentic-coding-harness), INSTALL_VERSION (default latest)

set -e

REPO="${INSTALL_REPO:-nkumar15/agentic-coding-harness}"
VERSION="${INSTALL_VERSION:-latest}"
SOURCE=""
ADDON=""
ADDON_SOURCE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source)
      SOURCE="$2"
      shift 2
      ;;
    --addon)
      ADDON="$2"
      shift 2
      ;;
    --addon-source)
      ADDON_SOURCE="$2"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found on PATH." >&2
  exit 1
fi

TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

# fetch_payload <source> <addon-name> <workdir> -> prints the directory containing the payload
fetch_payload() {
  src="$1"
  addon_name="$2"
  workdir="$3"

  if [ -n "$src" ]; then
    if [ -d "$src" ]; then
      echo "$src"
      return 0
    fi
    if [ -f "$src" ]; then
      mkdir -p "$workdir/extracted"
      tar -xzf "$src" -C "$workdir/extracted"
      echo "$workdir/extracted"
      return 0
    fi
    echo "--source path not found: $src" >&2
    exit 1
  fi

  repo="$REPO"
  if [ -n "$addon_name" ]; then
    repo="nkumar15/$addon_name"
  fi

  if [ "$VERSION" = "latest" ]; then
    api_url="https://api.github.com/repos/$repo/releases/latest"
  else
    api_url="https://api.github.com/repos/$repo/releases/tags/$VERSION"
  fi

  asset_url="$(curl -fsSL "$api_url" | grep -o '"browser_download_url": *"[^"]*package.tar.gz"' | head -n1 | sed -E 's/.*"(https[^"]+)"/\1/')"
  if [ -z "$asset_url" ]; then
    echo "could not resolve a package.tar.gz release asset for $repo ($VERSION)" >&2
    exit 1
  fi

  mkdir -p "$workdir/extracted"
  curl -fsSL "$asset_url" -o "$workdir/package.tar.gz"
  tar -xzf "$workdir/package.tar.gz" -C "$workdir/extracted"
  echo "$workdir/extracted"
}

PACKAGE_DIR="$(fetch_payload "$SOURCE" "" "$TMP_ROOT/base")"

UPDATE_MODE=false
if [ -d ".agents" ]; then
  UPDATE_MODE=true
fi

BACKUP_DIR="$TMP_ROOT/protected"
mkdir -p "$BACKUP_DIR"

if [ "$UPDATE_MODE" = true ]; then
  if [ -f ".agents/rules/project-conventions.md" ] && ! grep -q "<FILL_IN" ".agents/rules/project-conventions.md"; then
    mkdir -p "$BACKUP_DIR/.agents/rules"
    cp ".agents/rules/project-conventions.md" "$BACKUP_DIR/.agents/rules/project-conventions.md"
  fi
  if [ -f ".agents/process/gates.yaml" ] && [ -f "$PACKAGE_DIR/.agents/process/gates.yaml" ] \
     && ! diff -q ".agents/process/gates.yaml" "$PACKAGE_DIR/.agents/process/gates.yaml" >/dev/null 2>&1; then
    mkdir -p "$BACKUP_DIR/.agents/process"
    cp ".agents/process/gates.yaml" "$BACKUP_DIR/.agents/process/gates.yaml"
  fi
  if [ -f ".agents/process/config.yaml" ] && [ -f "$PACKAGE_DIR/.agents/process/config.yaml" ] \
     && ! diff -q ".agents/process/config.yaml" "$PACKAGE_DIR/.agents/process/config.yaml" >/dev/null 2>&1; then
    mkdir -p "$BACKUP_DIR/.agents/process"
    cp ".agents/process/config.yaml" "$BACKUP_DIR/.agents/process/config.yaml"
  fi
fi

cp -a "$PACKAGE_DIR/." .

if [ -f "$BACKUP_DIR/.agents/rules/project-conventions.md" ]; then
  cp "$BACKUP_DIR/.agents/rules/project-conventions.md" ".agents/rules/project-conventions.md"
  echo "kept existing .agents/rules/project-conventions.md (already filled in)"
fi
if [ -f "$BACKUP_DIR/.agents/process/gates.yaml" ]; then
  cp "$BACKUP_DIR/.agents/process/gates.yaml" ".agents/process/gates.yaml"
  echo "kept existing .agents/process/gates.yaml (customized commands)"
fi
if [ -f "$BACKUP_DIR/.agents/process/config.yaml" ]; then
  cp "$BACKUP_DIR/.agents/process/config.yaml" ".agents/process/config.yaml"
  echo "kept existing .agents/process/config.yaml (customized provider)"
fi

if [ -n "$ADDON" ] || [ -n "$ADDON_SOURCE" ]; then
  ADDON_DIR="$(fetch_payload "$ADDON_SOURCE" "$ADDON" "$TMP_ROOT/addon")"
  cp -a "$ADDON_DIR/." .
  echo "installed add-on: ${ADDON:-$ADDON_SOURCE}"
fi

python3 scripts/configure.py
python3 scripts/generate-agent-adapters.py
python3 scripts/validate-agent-portability.py

echo "install complete."
