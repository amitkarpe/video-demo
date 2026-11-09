#!/usr/bin/env bash
# Build the showcase and publish it to the gh-pages branch of amitkarpe/video-demo ("deploy from a branch").
# Used because the agents' token has no `workflow` scope; pages-workflow.yml.example is the Actions version for later.
#   site/deploy.sh            build + publish (a normal, fast-forward push; never a force push)
#   site/deploy.sh --dry-run  build + show what would change, push nothing
# Needs: Node 22+, git push access to the repository. No MP4 is ever published: videos stream from GitHub Releases.
set -euo pipefail
SITE=$(cd "$(dirname "$0")" && pwd); ROOT=$(git -C "$SITE" rev-parse --show-toplevel)
REMOTE=${REMOTE:-origin}; BRANCH=gh-pages; DRY=${1:-}
cd "$SITE"
[ -d node_modules ] || npm ci --no-audit --no-fund
npx astro build
# guard: nothing large or video-like may reach Pages (1 GB site limit; MP4s live on Releases)
if find dist -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.wav' -o -size +2M \) | grep -q .; then
  echo "refusing: dist has a video/audio file or a file over 2 MB:"; find dist -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.wav' -o -size +2M \); exit 1
fi
touch dist/.nojekyll   # Astro writes _astro/; without this GitHub Pages' Jekyll step would drop it
SRC=$(git -C "$ROOT" rev-parse --short HEAD)
TMP=$(mktemp -d); trap 'git -C "$ROOT" worktree remove --force "$TMP" >/dev/null 2>&1 || true; rm -rf "$TMP"' EXIT
git -C "$ROOT" fetch -q "$REMOTE" "$BRANCH" 2>/dev/null || true
if git -C "$ROOT" rev-parse -q --verify "refs/remotes/$REMOTE/$BRANCH" >/dev/null; then
  git -C "$ROOT" worktree add -q --detach "$TMP" "$REMOTE/$BRANCH"
else
  git -C "$ROOT" worktree add -q --detach "$TMP"; git -C "$TMP" checkout -q --orphan "$BRANCH"; git -C "$TMP" rm -rq . 2>/dev/null || true
fi
rsync -a --delete --exclude .git "$SITE/dist/" "$TMP/"
git -C "$TMP" add -A
if git -C "$TMP" diff --cached --quiet; then echo "gh-pages already up to date"; exit 0; fi
git -C "$TMP" diff --cached --stat | tail -3
if [ "$DRY" = "--dry-run" ]; then echo "dry run: not pushed"; exit 0; fi
git -C "$TMP" commit -q -m "site: build from $SRC"
git -C "$TMP" push -q "$REMOTE" "HEAD:refs/heads/$BRANCH"
echo "pushed $BRANCH (site from $SRC). Live in about a minute: https://amitkarpe.github.io/video-demo/"
