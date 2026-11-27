"""대본 ↔ 인식 결과 글자 정렬, 자막 줄 분할, onset 스냅.

script.txt 형식:  `## n | 챕터 제목` 줄 + 문단(한 줄 = 한 문단). **강조** 지원.
"""
import re, json, difflib, subprocess
import numpy as np

KEEP = re.compile(r'[가-힣A-Za-z0-9]')
MAXC = 22      # 한 화면 최대 글자(공백 제외)
MINC = 6       # 이보다 짧은 조각은 앞 조각에 붙임


def nlen(s):
    return len(KEEP.findall(s))


# ---------------------------------------------------------------- script
def parse_script(path):
    chapters, paras, text = [], [], ''
    for raw in open(path, encoding='utf-8').read().splitlines():
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith('##'):
            n, title = raw[2:].split('|', 1)
            chapters.append({'n': int(n), 'title': title.strip(), 'pos': len(text)})
            continue
        bold, clean, i = [], '', 0
        for part in re.split(r'(\*\*)', raw):
            if part == '**':
                if len(bold) and len(bold[-1]) == 1:
                    bold[-1].append(len(text) + len(clean))
                else:
                    bold.append([len(text) + len(clean)])
                continue
            clean += part
        paras.append({'s': len(text), 'e': len(text) + len(clean), 'bold': bold,
                      'ch': chapters[-1]['n']})
        text += clean + '\n'
    return text, chapters, paras


def sentences(text, s, e):
    """[s,e) 를 문장 단위 (start,end) 로."""
    out, st, i = [], s, s
    while i < e:
        c = text[i]
        if c in '.?!' and not (c == '.' and i + 1 < e and text[i + 1].isdigit()):
            j = i + 1
            if j < e and text[j] in '"\'”’':
                j += 1
            if j >= e or text[j] == ' ':
                out.append((st, j))
                st = j + 1 if j < e else j
                i = j
        i += 1
    if st < e and text[st:e].strip():
        out.append((st, e))
    # 짧은 꼬리("합니다") 앞에 붙이기
    merged = []
    for a, b in out:
        tail_q = (merged and text[merged[-1][1] - 1] in '"\'”’' and nlen(text[a:b]) <= 8
                  and text[a] not in '"\'“‘')
        if merged and (nlen(text[a:b]) < MINC or tail_q) and nlen(text[merged[-1][0]:b]) <= MAXC + 6:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


GOOD_END = ('고', '서', '데', '면', '며', '지만', '니다', '는데', '까지', '도', '나', '든', '요', '게', '만')


def split_piece(text, a, b):
    if nlen(text[a:b]) <= MAXC:
        return [(a, b)]
    seg = text[a:b]
    best = None
    for m in re.finditer(r'[,·] ', seg):      # 쉼표 우선
        k = a + m.end()
        l, r = nlen(text[a:k]), nlen(text[k:b])
        if l < MINC or r < MINC:
            continue
        sc = max(l, r)
        if best is None or sc < best[0]:
            best = (sc, k)
    if best is None or best[0] > MAXC + 8:
        best2 = None
        for m in re.finditer(r' ', seg):
            k = a + m.start()
            l, r = nlen(text[a:k]), nlen(text[k:b])
            if l < MINC or r < MINC:
                continue
            w = text[a:k].split(' ')[-1].rstrip(',"\'')
            bonus = 6 if w.endswith(GOOD_END) else 0
            if text[a:k].count('"') % 2 == 1:      # 따옴표 안 자르기 불리
                bonus -= 4
            sc = abs(l - r) - bonus
            if best2 is None or sc < best2[0]:
                best2 = (sc, k + 1)
        if best2 and (best is None or max(nlen(text[a:best2[1]]), nlen(text[best2[1]:b])) < best[0] - 4):
            best = (0, best2[1])
    if best is None:
        return [(a, b)]
    k = best[1]
    return split_piece(text, a, k) + split_piece(text, k, b)


def screens(text, paras, overrides=()):
    """overrides: 이 문자열 '앞'에서 강제로 줄을 나눈다."""
    out = []
    for p in paras:
        for a, b in sentences(text, p['s'], p['e']):
            cuts = [a] + sorted(text.find(o, a) for o in overrides if a < text.find(o, a) < b) + [b]
            for u0, v0 in zip(cuts, cuts[1:]):
                for u, v in split_piece(text, u0, v0):
                    while text[u] == ' ':
                        u += 1
                    out.append({'s': u, 'e': v, 'para': p})
    return out


def display(t):
    t = re.sub(r'(?<!\d)\.(?=["\'”’]?(\s|$))', '', t.strip())   # 마침표 제거(소수점 유지)
    return _quotes(t)


def _quotes(t):
    out = ''
    for i, c in enumerate(t):
        if c == '"':
            prev = t[i - 1] if i else ' '
            out += '“' if (prev in ' (' or i == 0) else '”'
        else:
            out += c
    return out


# ---------------------------------------------------------------- align
def norm_map(text):
    chars, idx = [], []
    for i, c in enumerate(text):
        if KEEP.match(c):
            chars.append(c.lower())
            idx.append(i)
    return ''.join(chars), idx


def char_times(text, words):
    sn, sidx = norm_map(text)
    rc, rt = [], []
    for w in words:
        n = ''.join(c.lower() for c in w['w'] if KEEP.match(c))
        for k, c in enumerate(n):
            d = (w['e'] - w['s']) / len(n)
            rc.append(c)
            rt.append((w['s'] + d * k, w['s'] + d * (k + 1)))
    rn = ''.join(rc)
    sm = difflib.SequenceMatcher(None, sn, rn, autojunk=False)
    st = [None] * len(sn)
    diffs = []
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            for k in range(a2 - a1):
                st[a1 + k] = rt[b1 + k]
        elif op == 'replace' and (a2 - a1) == (b2 - b1):
            for k in range(a2 - a1):
                st[a1 + k] = rt[b1 + k]
        if op != 'equal':
            diffs.append((op, sn[max(0, a1 - 6):a2 + 6], sn[a1:a2], rn[b1:b2]))
    # 보간
    known = [i for i, v in enumerate(st) if v]
    for i in range(len(st)):
        if st[i] is None:
            lo = max([k for k in known if k < i], default=None)
            hi = min([k for k in known if k > i], default=None)
            if lo is None:
                st[i] = st[hi]
            elif hi is None:
                st[i] = st[lo]
            else:
                f = (i - lo) / (hi - lo)
                t = st[lo][1] + (st[hi][0] - st[lo][1]) * f
                st[i] = (t, t)
    full = {}
    for k, i in enumerate(sidx):
        full[i] = st[k]
    return full, sidx, diffs


def rms_track(audio):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32)
    hop = 160
    n = len(x) // hop
    r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(r)
    thr = max(np.percentile(db, 8) + 12, np.percentile(db, 95) - 32)
    voiced = db > thr
    onsets = []
    run = 99
    for i, v in enumerate(voiced):
        if v and run >= 15:          # 0.15s 이상 무음 뒤 소리
            onsets.append(i * 0.01)
        run = 0 if v else run + 1
    return voiced, np.array(onsets), len(x) / 16000


def time_at(full, text, pos, end=False):
    for i in (range(pos, len(text)) if not end else range(pos - 1, -1, -1)):
        if i in full:
            return full[i][1 if end else 0]
    return 0.0


def build_lines(text, scr, full, voiced, onsets):
    lines = []
    for k, sc in enumerate(scr):
        s = time_at(full, text, sc['s'])
        e = time_at(full, text, sc['e'], end=True)
        fi = int(s * 100)
        silent = fi < len(voiced) and not voiced[max(0, fi - 3):fi + 3].any()
        if silent:
            nxt = onsets[(onsets >= s) & (onsets <= s + 1.2)]
            if len(nxt):
                s = float(nxt[0])
        else:
            near = onsets[np.abs(onsets - s) <= 0.15]
            if len(near):
                s = float(near[np.argmin(np.abs(near - s))])
        p = sc['para']
        hl = any(b[0] < sc['e'] and b[1] > sc['s'] for b in p['bold'])
        lines.append({'i': k, 'pos': sc['s'], 'end': sc['e'], 'raw': text[sc['s']:sc['e']],
                      'text': display(text[sc['s']:sc['e']]), 's': round(s, 3), 'e': round(max(e, s + .3), 3),
                      'hl': hl, 'ch': p['ch']})
    for a, b in zip(lines, lines[1:]):
        if b['s'] < a['s'] + 0.2:
            b['s'] = a['s'] + 0.2
    for k, l in enumerate(lines):
        l['show'] = round(max(0, l['s'] - 0.03), 3)
    for k, l in enumerate(lines):
        nxt = lines[k + 1]['show'] if k + 1 < len(lines) else None
        if nxt is not None and nxt - l['e'] < 0.6:
            l['hide'] = nxt
        else:
            l['hide'] = round(l['e'] + 0.2, 3) if nxt is None else round(min(l['e'] + 0.2, nxt), 3)
    return lines
