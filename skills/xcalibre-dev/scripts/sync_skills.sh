#!/usr/bin/env bash
set -euo pipefail

mode=""
repo=""
for argument in "$@"; do
  case "$argument" in
    --check) mode="--check" ;;
    -*) echo "usage: sync_skills.sh [--check] [repository]" >&2; exit 2 ;;
    *) repo="$argument" ;;
  esac
done
repo="${repo:-$PWD}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$(cd "$script_dir/.." && pwd)"
skill_name="$(basename "$source_dir")"

targets=(
  "$HOME/.claude/skills/$skill_name"
  "$HOME/.codex/skills/$skill_name"
  "$repo/.claude/skills/$skill_name"
  "$repo/.codex/skills/$skill_name"
)

while IFS= read -r manifest; do
  target="$(dirname "$manifest")"
  case "$target" in
    */.local/share/Trash/*|*/Trash/*) continue ;;
  esac
  targets+=("$target")
done < <(find "$HOME" -type f -path "*/$skill_name/SKILL.md" 2>/dev/null)

drift=0
declare -A seen=()
for target in "${targets[@]}"; do
  [ "$target" = "$source_dir" ] && continue
  [ -n "${seen[$target]:-}" ] && continue
  seen[$target]=1
  if [ "$mode" = "--check" ]; then
    if ! diff -rq "$source_dir" "$target" >/dev/null 2>&1; then
      echo "DRIFT: $target"
      drift=1
    fi
  else
    mkdir -p "$target"
    rsync -a --delete "$source_dir/" "$target/"
    echo "SYNCED: $target"
  fi
done

if [ "$mode" = "--check" ]; then
  [ "$drift" -eq 0 ] && echo "xcalibre-dev copies in sync"
  exit "$drift"
fi
