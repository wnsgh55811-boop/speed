# -*- coding: utf-8 -*-
"""Replace one span of the master narration with a re-voiced take.

    python3 splice.py <master.mp3> <take.mp3> <t0> <t1> <out.mp3>

Used when TTS misreads a word (e.g. "4시간" read as "사시간"): the fixed
sentences are voiced again with the same voice, then dropped into [t0, t1)
so every other timing in the film stays where it was. The take is trimmed
of edge silence, loudness-matched to the span it replaces, and only if it
is longer than the span it is time-compressed (atempo, ≤ 1.15×) — never
stretched slower. Short edge fades hide the joins.
"""
import json
import subprocess
import sys


def sh(c):
    r = subprocess.run(c, shell=True, text=True, capture_output=True)
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit(c[:100])
    return r.stdout + r.stderr


def dur(f):
    return float(sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {f}").strip())


def lufs(f):
    out = sh(f"ffmpeg -hide_banner -i {f} -af loudnorm=print_format=json -f null -")
    return float(json.loads(out[out.rindex("{"):])["input_i"])


def main():
    master, take, t0, t1, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    ar = "-ar 48000 -ac 2"
    sh(f"ffmpeg -v error -i {master} {ar} m.wav -y")
    sh(f"ffmpeg -v error -ss {t0} -to {t1} -i m.wav old.wav -y")
    # trim leading/trailing silence of the take
    sh(f"ffmpeg -v error -i {take} {ar} -af silenceremove=start_periods=1:start_threshold=-45dB,"
       f"areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse t.wav -y")
    span, L = t1 - t0, dur("t.wav")
    lead, tail = 0.10, 0.18
    room = span - lead - tail
    tempo = max(1.0, L / room)
    if tempo > 1.15:
        raise SystemExit(f"take {L:.2f}s does not fit {room:.2f}s (x{tempo:.2f})")
    gain = lufs("old.wav") - lufs("t.wav")
    sh(f"ffmpeg -v error -i t.wav -af 'atempo={tempo:.4f},volume={gain:.2f}dB,"
       f"afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse,"
       f"adelay=delays={int(lead * 1000)}:all=1,apad=whole_dur={span:.3f}' -t {span:.3f} new.wav -y")
    sh(f"ffmpeg -v error -t {t0} -i m.wav a.wav -y")
    sh(f"ffmpeg -v error -ss {t1} -i m.wav c.wav -y")
    open("j.txt", "w").write("file 'a.wav'\nfile 'new.wav'\nfile 'c.wav'\n")
    sh("ffmpeg -v error -f concat -safe 0 -i j.txt -c:a pcm_s16le joined.wav -y")
    sh(f"ffmpeg -v error -i joined.wav -c:a libmp3lame -b:a 320k {out} -y")
    print(f"span {span:.2f}s take {L:.2f}s tempo x{tempo:.3f} gain {gain:+.2f}dB "
          f"master {dur(master):.3f}s -> out {dur(out):.3f}s")


if __name__ == "__main__":
    main()
