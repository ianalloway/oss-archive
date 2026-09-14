#!/usr/bin/env bash
# Generate STATUS.md from origin's archive/* branch tips.
# Usage (from repo root): ./scripts/generate-status.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUT="${1:-STATUS.md}"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

git fetch --quiet origin 'refs/heads/archive/*:refs/remotes/origin/archive/*' 2>/dev/null || true

mapfile -t BRANCHES < <(
  git for-each-ref --format='%(refname:short)' refs/remotes/origin/archive \
    2>/dev/null | sed 's#^origin/##' | sort
)

if [[ ${#BRANCHES[@]} -eq 0 ]]; then
  mapfile -t BRANCHES < <(
    git ls-remote --heads origin 'archive/*' \
      | awk '{print $2}' | sed 's#refs/heads/##' | sort
  )
fi

GENERATED_UTC="$(date -u +"%Y-%m-%d %H:%M UTC")"
# America/New_York wall clock for humans reading the index
GENERATED_ET="$(TZ=America/New_York date +"%Y-%m-%d %H:%M %Z")"

{
  echo "# Archive status"
  echo
  echo "Auto-generated snapshot of every \`archive/*\` branch tip."
  echo "Regenerate: \`./scripts/generate-status.sh\`"
  echo
  echo "- **Branches:** ${#BRANCHES[@]}"
  echo "- **Generated:** ${GENERATED_ET} (${GENERATED_UTC})"
  echo
  echo "| Branch | Tip | When (ET) | Files | Last subject |"
  echo "|--------|-----|-----------|------:|--------------|"
} > "$TMP"

for branch in "${BRANCHES[@]}"; do
  ref="origin/${branch}"
  if ! git rev-parse --verify --quiet "$ref" >/dev/null; then
    # fall back to remote SHA via ls-remote
    sha="$(git ls-remote --heads origin "$branch" | awk '{print $1}')"
    ref="$sha"
  fi

  tip="$(git log -1 --format='%h' "$ref")"
  iso="$(git log -1 --format='%cI' "$ref")"
  subject="$(git log -1 --format='%s' "$ref" | tr '|' '/' | cut -c1-72)"
  files="$(git ls-tree -r --name-only "$ref" | wc -l | tr -d ' ')"

  # Convert committer ISO timestamp to America/New_York for the table
  when_et="$(TZ=America/New_York date -d "$iso" +"%Y-%m-%d %H:%M %Z" 2>/dev/null \
    || python3 -c "from datetime import datetime; import sys; d=datetime.fromisoformat(sys.argv[1]); print(d.strftime('%Y-%m-%d %H:%M %z'))" "$iso")"

  name="${branch#archive/}"
  link="https://github.com/ianalloway/oss-archive/tree/${branch}"
  echo "| [\`${name}\`](${link}) | \`${tip}\` | ${when_et} | ${files} | ${subject} |" >> "$TMP"
done

{
  echo
  echo "## Revive one-liner"
  echo
  echo 'Clone a single archived project straight into a new local repo (no checkout of `main`):'
  echo
  echo '```bash'
  echo 'git clone --branch archive/<name> --single-branch \'
  echo '  https://github.com/ianalloway/oss-archive.git <name> && cd <name>'
  echo '```'
  echo
  echo "Example — revive \`odds-cli\` and push it to a fresh GitHub repo:"
  echo
  echo '```bash'
  echo 'git clone --branch archive/odds-cli --single-branch \'
  echo '  https://github.com/ianalloway/oss-archive.git odds-cli && cd odds-cli'
  echo 'gh repo create ianalloway/odds-cli --public --source=. --remote=origin --push'
  echo '```'
} >> "$TMP"

mv "$TMP" "$OUT"
trap - EXIT
echo "Wrote ${OUT} (${#BRANCHES[@]} branches)"
