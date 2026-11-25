---
name: youtube-16x9
description: Make a chaptered 16:9 YouTube video (1920x1080) from a voice recording + script — clean light infographic style with chapter header/progress bar, centered chapter title cards, bottom-center subtitles, infographic components, memes, 16:9 thumbnail, description and chapter timestamps. Use when the user asks for a 유튜브 영상 (16:9, long-form) from 대본 + 음성 (upload or Google Drive), e.g. the marketing/consulting channel.
---

# 16:9 유튜브 인포그래픽 영상

Template `assets/youtube.html`: off-white #F5F3EE + faint 90px grid, ink #141414, orange #FF5A1F, green #12A150, white cards. Professional, clean, no account label.

## Pipeline (SK = this skill dir; scripts identical to reel-9x16)
1. `bash SK/scripts/setup.sh` once. Voice from Google Drive folder: `pip install gdown; gdown --folder <url> -O <dir>` (use the venv pip if needed).
2. `bash SK/scripts/new_project.sh <work> SK/assets/youtube.html <voice>`
3. `<work>/script.txt`: one subtitle per line, **≤ one sentence per subtitle**, long sentences split at meaning boundaries (12–28 chars, max 2 lines). Chapter markers on their own line before the chapter's first line: `#CH|0|오프닝`, `#CH|1|<title>` … Drop `[화면]` lines and `(예시)`/⭐ markers from spoken text (they are directions). `**line` / `**a … b**` = orange emphasis.
4. `~/.cache/reelkit/venv/bin/python -I SK/scripts/transcribe.py in/voice.* words.json script.txt` (7 min ≈ 3 min CPU).
5. `python3 -I SK/scripts/align_lines.py script.txt words.json in/voice.* chunks.json` → also prints real chapter timestamps.
6. Memes via `SK/scripts/meme.py search|get` (see reel-9x16 rules: variety, no repeats, no Drake, Korean caption above, ~12 per 7 min).
7. `scenes.py` — start from `assets/example_scenes_youtube.py` (set `MAXW, MAXH = 1100, 540`). Then `python3 -I SK/scripts/build_timeline.py chunks.json scenes.py timeline.json`. Add `"outro_n": <n>` to timeline.json only if the last chapter should read OUTRO.
8. `node SK/scripts/render.js <work> page.html timeline.json 1920 1080 test "…"` → contact sheet → fix.
9. `node … full` (≈12.7k frames for 7 min — run in background) → ffmpeg `-crf 20` with the original audio (no processing, no music, no SFX).
10. Thumbnail: copy `assets/thumb_youtube.html`, edit, `node SK/scripts/shot.js thumb_youtube.html thumb.png 1280 720`.
11. Commit + push, send files, give description + chapters.

## Layout rules
- Subtitles **bottom center** fixed (top 880), dark box, white 56px; emphasis = orange box.
- Header top-left: `CHAPTER n` + title + progress bar (done = black, current = orange). Hidden on opening and on chapter cards.
- **Chapter title card at every chapter start — centered, minimal, premium** (house style, keep it): dark radial gradient, `—— CHAPTER ——` small letterspaced, thin orange number 01…, short divider, one-line white title. Holds until the next line (≥ ~2 s; if <1 s, start the next scene one line later). Outro/정리 goes straight to the recap list without a card.
- Content box centred (1740×640). Elements not yet spoken are dimmed (0.18) or hidden and switch on at the word (`"@line"`).
- Hard cuts only; no SFX; only bars grow (0.9 s).
- `[화면]` directions are built as real visuals; `(예시)` scenes get "(예시)" in the title; never show real IDs (comment IDs are gray bars).

## Components (scene `type`)
`chapter(n,t)` · `big(t, t2, at2, s)` statement + reveal box · `list` {title, items[{t,s,at}], hl} · `vs(a,b,ata,atb,mid,title)` two cards (`mid` "≠" "=" "+" "or") · `table` {title, rows[[label,[text,at,win]…]]} · `flow` {title, steps[{e,t,at}], hlast, note, atn} · `lock` {tiles[{w,en,s,f,pay,at}]} WHAT/WHY/HOW · `branch` {q, cards[{who,e,p,sol,at,at2}]} same problem → different causes · `grid` {title, at1, at2, rows[{who,hit}]} N people × 5 tries · `example` {e,h,free,paid,at1,at2,ltag,rtag} side-by-side · `caption` {after, label, lines[[text,at,highlight]]} BEFORE/AFTER · `thread` {items[{t,me,bad,lab,at}]} comment reply · `check` {title, rows[{t,at,res,at2}]} · `comments` {count, items[[text,at]]} · `dm` · `profile` {badges[[t,at]]} · `bars` {title, bars[{l,v,h,c}]} · `meme(name, cap, ov)` · `end` {at, p1, p2}.
Roughly 80% infographic/UI, 15% memes, rest statement cards; ~75 scenes per 7 minutes.

## Thumbnail (1280×720)
Left: black topic tag → 3-line headline (88px Black, key words on a tilted orange highlighter, line-height ≥1.3 so it doesn't overlap) → gray sub line. Right: 3 cards summarising the core structure (last one black/accent).

## Description (give in chat)
3 lines: ① the core rule ② the viewer's pain ③ what the video covers; then chapters (first 0:00, ≥3 chapters, each ≥10 s, times from align_lines output); then ≤3 hashtags.
