#!/usr/bin/env bash
# Emit index.html for one project.  usage: bash build.sh <project> [--audio path]
#
# emit.py reads plan.py, chunks.json and timings.txt from next to itself, so
# the project's three data files are staged into src/ first. Keeping them in
# examples/<project>/ is what lets src/ stay project-agnostic.
set -e
P=${1:?usage: build.sh <project> [--audio ...]}; shift || true
D=$(cd "$(dirname "$0")" && pwd)
cp "$D/examples/$P/plan.py" "$D/examples/$P/chunks.json" "$D/examples/$P/timings.txt" "$D/src/"
rm -rf "$D/src/__pycache__"
cd "$D" && python3 src/emit.py "$@"
