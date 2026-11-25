---
name: reel-9x16
description: Make a 9:16 Instagram Reel/Shorts (1080x1920) from a voice recording + script, with frame-accurate subtitles, memes, hand-drawn couple characters, KakaoTalk/Instagram UI mockups, thumbnail and caption. Use when the user sends a voice file (mp3/wav, upload or Google Drive) with a 릴스 대본 and asks for 릴스/영상/썸네일/캡션 — dating-advice series (이다사 태도 부트캠프, dark style) or the marketing account (light style).
---

# 9:16 릴스 제작 (음성 + 대본 → 영상·썸네일·캡션)

Two looks share one pipeline:
- **dark** `assets/reel_dark.html` — 연애 시리즈(이다사 태도 부트캠프). Dark woven texture, memes, chibi couple characters, KakaoTalk, emoji cards.
- **light** `assets/reel_light.html` — 마케팅 계정. Off-white dot grid, black + orange (#FF5A1F), Instagram comment/DM UI, chart, versus, WHAT/WHY/HOW split, compare, checklist CTA.

## Pipeline (scripts in `scripts/`, run from anywhere; SK = this skill dir)
1. `bash SK/scripts/setup.sh` (once per machine: fonts → ~/.cache/reelkit/fonts, faster-whisper venv; needs ffmpeg, node playwright, python pillow+numpy).
2. `bash SK/scripts/new_project.sh <work> SK/assets/reel_dark.html <voice>` (light: reel_light.html). Google Drive folder → `pip install gdown; gdown --folder <url> -O <dir>` first.
3. Write `<work>/script.txt` — **one subtitle per line, exactly the user's line breaks**. If the script has no line breaks, split into 1–3 어절 meaning units yourself (never more than one sentence per subtitle). `**…**` = emphasis (yellow on dark / orange box on light).
4. `~/.cache/reelkit/venv/bin/python -I SK/scripts/transcribe.py <work>/in/voice.* <work>/words.json <work>/script.txt`
5. `python3 -I SK/scripts/align_lines.py script.txt words.json in/voice.* chunks.json` — text comes from the script, timing from speech; starts snap to real speech onsets. Where the recording differs from the script (missing/changed words) **follow the audio**, edit script.txt, and tell the user what changed.
6. Memes: `python3 -I SK/scripts/meme.py search <kw>…` then `meme.py get <ID> <name> <work>/memes [trim|left|right|top|bottom|x0,y0,x1,y1]`. Look at a contact sheet of candidates before choosing.
7. Write `<work>/scenes.py` (see `assets/example_scenes_dark.py`, `assets/example_scenes_light.py`), then `python3 -I SK/scripts/build_timeline.py chunks.json scenes.py timeline.json`.
8. Test frames: `node SK/scripts/render.js <work> page.html timeline.json 1080 1920 test "1,5,9,…"` → look at them (contact sheet) and fix overlaps/empty screens.
9. Full: `node SK/scripts/render.js <work> page.html timeline.json 1080 1920 full` then
   `ffmpeg -framerate 30 -i frames/%05d.jpg -i in/voice.* -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4`
   (long renders: run in background). Fix a few scenes later with `range ranges.json` ([[t0,t1],…]) and re-encode.
10. Thumbnail: copy `assets/thumb_dark.html` / `thumb_light.html` into <work>, edit text/visual, `node SK/scripts/shot.js thumb.html thumb.png 1080 1920`. Check the 3:4 grid crop (y 285–1635) keeps everything.
11. Commit + push mp4 and thumbnail (repo root, names like `idasa_reelN.mp4`, `idasa_reelN_thumbnail.png`); send files; give caption in chat.

## House rules (the user asked for these — keep them)
- Fonts: **only two** — Gothic A1 Bold (everything) + Nanum Pen Script (only character speech). Subtitles all **same size (76px)**; emphasis changes colour only.
- Subtitle position: **centered** when the scene has no image (`text()` scenes); **fixed y=1260 under the image** otherwise. Scene changes happen exactly when a subtitle line starts, so subtitles never jump mid-line.
- **No sound effects, no glitch/RGB transitions, no pop/fade animations.** Hard cuts only.
- First ~2 s: title caption (`TITLE` in scenes.py) — white line + yellow line (dark) / black + orange box (light). Ends at the line after the hook.
- Characters (dark): woman = coral hair `w`, man = blue hair `m`. Moods: neutral smile happy sweat annoyed cool(sunglasses) flat. Speech = white bubble with border + tail; thought = text starting `~` (cloud). Emoji-only text shows without a box.
- KakaoTalk scenes: ≤5 bubbles (more overflows into the subtitle). Don't open a kakao scene before its first message — show characters until then.
- Memes: lots of variety, **never repeat a meme within a video, never use Drake**. Pick memes for emotion/reaction beats (shock, confusion, sweating, smug, giving up, waiting). Add a one-line Korean caption ‘…’ above. Blank speech bubbles in a meme → put Korean text in with `ov=[[x%,y%,w%,"text",px]]`. Avoid tiny sources (<250px) — they blur.
- CTA scene at the end: pill "🔗 프로필 링크" + sub "비공개 특강 · 이다사 태도 부트캠프". Comment-keyword CTA: `cta(pill='<span class="emo">💬</span>댓글에 ‘키워드’', sub="")` — **nothing under the pill** if the user says so.
- Women-targeted episodes: pink accent (#FF6FA8) in thumbnail.

## Scene API (scenes.py)
`SCENES = [(anchor, scene[, n]), …]` — anchor = start of a subtitle line (prefix, spaces/quotes ignored), searched forward from the previous scene, so repeated lines just work. Inside scenes `"@line"` = that line's start time; `None` = scene start.
dark: `text()`, `meme(name, cap, ov=None)`, `card(emoji, cap, (c1,c2))`, `icons((at,"w"|"m",text,append,mood),…)`, `kakao((at,"in"|"out",text),…)`, `cta(pill, sub)`.
light: `text()`, `meme`, `{"type":"chart","up","down"}`, `{"type":"comments","count","ev":[[at,text,user]]}`, `{"type":"dm"}`, `{"type":"versus","a":{who,e,act},"b":{…},"ev":[[at],[at]]}`, `{"type":"split","rows":[[w,EN,val,paid]],"ev":[[at]…]}`, `{"type":"compare","no","yes","ev":[[at]]}`, `{"type":"cta","pill","doc","items"}`.
Aim for a new visual every ~2–6 s; alternate character/UI scenes, memes and plain-text beats; text-only for 결론/전환 lines.

## Thumbnail rules
Short, provocative, curiosity-driven (contradict a common belief: "착하면 차입니다", "후폭풍은 안 옵니다", "이 카톡 보내면 끝입니다"). 2–3 lines max: small gray lead-in + white line + big red line. One visual: meme, characters with bubbles, or kakao bubbles. User prefers **less text** — don't add quote lines unless asked.

## Caption (give in chat)
Hook line (same idea as thumbnail) → ❌/⭕ or ✔️ core summary of the script → one-line takeaway → 📌 save prompt → 🔗 profile link / 💬 comment keyword → 8–15 hashtags ending with #이다사 #태도부트캠프 (dating) . If asked "핵심 요약으로", keep it to the core bullets. Optionally a shorter version and a comment-bait version.
