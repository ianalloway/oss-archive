#!/usr/bin/env bash
# Generate STATUS.md from origin's archive/* branch tips.
# Usage (from repo root): ./scripts/generate-status.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUT="${1:-STATUS.md}"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

git fetch --quiet origin 'refs/heads/archive/*:refs/remotes/origin/archive/*'

BRANCHES="$(
  git for-each-ref --format='%(refname:short)' refs/remotes/origin/archive \
    2>/dev/null | sed 's#^origin/##' | sort
)"

if [[ -z "$BRANCHES" ]]; then
  echo "No archive branches found; ${OUT} was not changed." >&2
  exit 1
fi
BRANCH_COUNT="$(printf '%s\n' "$BRANCHES" | wc -l | tr -d ' ')"

GENERATED_UTC="$(date -u +"%Y-%m-%d %H:%M UTC")"
# America/New_York wall clock for humans reading the index
GENERATED_ET="$(TZ=America/New_York date +"%Y-%m-%d %H:%M %Z")"

{
  echo "# Archive status"
  echo
  echo "Auto-generated snapshot of every \`archive/*\` branch tip."
  echo "Regenerate: \`./scripts/generate-status.sh\`"
  echo
  echo "- **Branches:** ${BRANCH_COUNT}"
  echo "- **Generated:** ${GENERATED_ET} (${GENERATED_UTC})"
  echo
  echo "| Branch | Tip | When (ET) | Files | Last subject |"
  echo "|--------|-----|-----------|------:|--------------|"
} > "$TMP"

while IFS= read -r branch; do
  ref="origin/${branch}"

  tip="$(git log -1 --format='%h' "$ref")"
  subject="$(git log -1 --format='%s' "$ref" | tr '|' '/' | cut -c1-72)"
  files="$(git ls-tree -r --name-only "$ref" | wc -l | tr -d ' ')"

  # Git handles the local timezone on both GNU/Linux and macOS, including DST.
  when_et="$(TZ=America/New_York git log -1 --format='%cd' \
    --date='format-local:%Y-%m-%d %H:%M %Z' "$ref")"

  name="${branch#archive/}"
  link="https://github.com/ianalloway/oss-archive/tree/${branch}"
  echo "| [\`${name}\`](${link}) | \`${tip}\` | ${when_et} | ${files} | ${subject} |" >> "$TMP"
done <<< "$BRANCHES"

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
  echo '  https://github.com/ianalloway/oss-archive.git odds-cli-revived && cd odds-cli-revived'
  echo 'git remote rename origin archive'
  echo 'gh repo create ianalloway/odds-cli-revived --public --source=. --remote=origin --push'
  echo '```'
} >> "$TMP"

mv "$TMP" "$OUT"
trap - EXIT
echo "Wrote ${OUT} (${BRANCH_COUNT} branches)"
