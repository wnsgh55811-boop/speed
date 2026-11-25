#!/usr/bin/env bash
# usage: new_project.sh <workdir> <template.html> <voice file>
# Creates a work dir with the page template, fonts link, memes/ and in/voice.*
set -e
W="$1"; T="$2"; V="$3"
CACHE="${REELKIT_HOME:-$HOME/.cache/reelkit}"
mkdir -p "$W/in" "$W/memes" "$W/frames" "$W/test"
cp "$T" "$W/page.html"
ln -sfn "$CACHE/fonts" "$W/fonts"
[ -n "$V" ] && cp "$V" "$W/in/voice.${V##*.}"
echo "$W ready"
