# -*- coding: utf-8 -*-
"""대화가 깊어지는 사람 — scene plan (Fish Audio take, 342.3s, 230 spoken lines).

Each scene starts on line `a` and runs until the next scene's first line.
`at`: int = onset of that spoken line, float = seconds into the scene,
(line, s) = s seconds after that line starts.
`mute`: lines whose words are already on screen verbatim (bubbles, quotes),
so the bottom caption is dropped for them.

v4 rule: no visual form is used more than twice in the film (checked by
check_forms() at the bottom), and no still carries more than two scenes.
"""
TOTAL = 343.0
AUDIO = "assets/audio/voice.wav"

S = []
add = lambda **k: S.append(k)  # noqa: E731

# ── 0  cold open ────────────────────────────────────────────────────────────
add(a=0, kind="hook", bg="photo:br_date_stuck")
add(a=3, kind="checklist", bg="bg-ink", title="처음 만난 그녀에게 물어본 것",
    items=[("직업", 4), ("취미", 5), ("여행", 6), ("좋아하는 음식", 7)])
add(a=8, kind="ring", bg="bg-canvas", title="남은 대화 소재", start=0.86, end=0.08, at=8,
    label="새로운 주제 찾기 시작", at_label=9)
add(a=10, kind="phone", bg="bg-teal", title="새 주제 찾는 중",
    msgs=[("m", "MBTI는 뭐예요?", 10), ("m", "주말에는 뭐 해요?", 11), ("m", "영화 좋아하세요?", 12)],
    mute=[10, 11, 12])
add(a=13, kind="lines", bg="bg-grid", title="이어지는 대화, 그대로인 거리",
    xlab="대화 시간", ylab="정도",
    series=[("대화량", "M0 430 C200 380 420 250 620 170 S880 60 1000 40", "cyan", 13, 760, 60),
            ("친밀감", "M0 420 C250 418 500 412 720 414 S900 410 1000 408", "amber", 14, 770, 385)])
add(a=15, kind="icon", bg="bg-teal", key="ico_iceberg", title="표면에서만 맴도는 대화",
    orbit=True, size=470)
add(a=17, kind="typo", bg="bg-spot",
    rows=[("왜 그럴까?", 17, "lg"), ("대화 주제가 부족해서", 18, "md")], strike=(1, 18))
add(a=19, kind="depth", bg="bg-ink", title="같은 주제, 다른 깊이",
    levels=[("같은 주제", 19), ("조금 더", 20), ("훨씬 더 깊게", (20, 0.9))])
add(a=21, kind="split",
    left=dict(n="처음 만난 사람", head="어색함을 줄이고", at=22, photo="br_date_wide"),
    right=dict(n="조금 친해진 사람", head="더 가까워지는", at=23, photo="br_couple_close"))
add(a=26, kind="chapter", bg="bg-spot", num="1", word="주제에서 사람으로")

# ── 1  topic → person ───────────────────────────────────────────────────────
add(a=28, kind="chat", bg="soft:br_quiet_cafe", title="흔한 대화",
    msgs=[("w", "저 카페 가는 거 좋아해요.", 29), ("m", "어떤 카페 좋아하세요?", 31),
          ("w", "조용한 카페 좋아해요.", 33), ("m", "커피는 뭐 좋아하세요?", 35)],
    mute=[29, 31, 33, 35])
add(a=36, kind="bars", bg="bg-dust", title="그래서 알게 된 것",
    bars=[("카페에 대해", 0.9, 37, "amber"), ("그 사람에 대해", 0.08, 39, "dim")])
add(a=41, kind="stairs", bg="bg-teal", title="여기서 한 단계만",
    steps=[("질문", 41), ("한 단계 더", (41, 0.9))])
add(a=42, kind="pbub", bg="photo:br_busy_cafe",
    msgs=[("w", "저 조용한 카페 좋아해요.", 43),
          ("m", "저는 오히려 사람 많은 데도 좋아해요.|가만히 앉아 사람 구경하는 게 재밌더라고요.", 46, "내 이야기"),
          ("m", "원래 혼자 있는 거 좋아하는 편이에요?", 49, "사람에 대한 질문")],
    mute=[43, 46, 47, 49])
add(a=51, kind="morph", bg="bg-canvas", x="카페 이야기", y="평소 성격", at_y=53,
    title="이야기가 달라집니다")
add(a=54, kind="person", bg="bg-ember", key="cut_woman_talk", side="left",
    bubbles=[("네. 사람 만나는 건 좋아하는데|오래 만나면 좀 지치는 편이에요.", 55)], mute=[55, 56])
add(a=57, kind="tree", bg="bg-ink", root="그녀",
    branches=[("사람을 만나는 방식", "br_friends", 59), ("혼자 있을 때", "br_alone_read", 60),
              ("친한 사람과 있을 때", "br_busy_cafe", 61)])
add(a=63, kind="cards", bg="bg-grid", title="“여행 좋아하세요?” 다음에",
    cards=[dict(n="계획형?", head="다 짜놓는 편", at=64, photo="br_travel_plan"),
           dict(n="즉흥형?", head="가서 정하는 편", at=67, photo="br_travel_free")], vs=True)
add(a=69, kind="quote", bg="soft:br_travel_plan",
    quotes=[("저는 계획 다 짜놓는 편이에요.", 70, "그녀")], mute=[70])
add(a=72, kind="lens", bg="bg-teal", sentence="“저는 계획 다 짜놓는 편이에요.”", at_lens=72,
    dim="여행 정보", bright="훨씬 많은 정보", at_bright=73)
add(a=74, kind="sliders", bg="bg-canvas", title="평소에는 어떤 사람일까",
    rows=[("계획적", "즉흥적", 0.16, 74), ("통제 선호", "흐름에 맡김", 0.22, 75),
          ("새로운 것", "익숙한 것", 0.5, 76)])
add(a=78, kind="highlight", bg="bg-spot", pre="여행 이야기가 ", key="사람 이야기", post="로",
    at_key=79)
add(a=80, kind="strikelist", bg="bg-ink", title="여기서 중요한 건",
    items=[("상대의 성격 분석", 80, (81, 0.6), False)])
add(a=82, kind="iconside", bg="bg-teal", key="ico_iceberg", title="수면 아래까지",
    sub="보이는 사실은 일부일 뿐", at_sub=83, size=450)
add(a=84, kind="depth", bg="bg-dust", title="질문을 한 단계씩",
    levels=[("뭘 좋아해요?", 84), ("왜 좋아해요?", 85), ("평소에도 그런 편이에요?", 86)],
    top="사실", bottom="사람")
add(a=88, kind="cloud", bg="bg-grid", center="소재 하나",
    chips=[("성격", 89), ("취향", (89, 0.3)), ("생활 방식", (89, 0.6)), ("관계", (89, 0.9))])

# ── 1b  the common mistake ──────────────────────────────────────────────────
add(a=90, kind="alert", bg="bg-ember", head="자주 하는 실수", sub="상대 이야기만 계속 끌어내기",
    at_sub=92)
add(a=93, kind="flow", bg="bg-canvas", title="질문과 대답만 오가는 대화",
    items=[("상대의 말", 93, "a"), ("질문", 94, "q"), ("대답", 95, "a"), ("또 질문", 96, "q")], loop=True)
add(a=97, kind="distance", bg="bg-ink", title="대화는 계속되는데", gap_from=620, gap_to=620, at=97,
    note="거리는 그대로", at_note=98, chatter=True)
add(a=99, kind="scale", bg="bg-spot", title="한쪽만 보여주는 대화", left="상대", right="나",
    tilt_at=100)
add(a=102, kind="venn", bg="bg-teal", title="질문했다면", left="질문", right="내 생각", at_b=103,
    mid="같이")
add(a=104, kind="pbub", bg="photo:br_couple_close",
    msgs=[("m", "저는 계획 너무 많이 세우면 오히려 피곤하더라고요.|어디 갈지만 정하고 나머지는 가서 정하는 편이에요.",
           104, "내 생각")], mute=[104, 105])
add(a=106, kind="highlight", bg="bg-dust", pre="질문에 ", key="내 이야기", post=" 한 스푼",
    at_key=(106, 0.4))
add(a=107, kind="scale", bg="bg-canvas", title="대화는", left="상대", right="나", tilt_at=107,
    level_at=109)
add(a=111, kind="pulse", bg="soft:br_man_nervous", title="마음에 드는 사람 앞에서는", shape="rise",
    at=111, label="그게 잘 안 됩니다", at_label=112)
add(a=113, kind="meter", bg="bg-ember", title="대화를 잘해야 한다는 압박", start=0.18, end=0.94,
    at=114, left="여유", right="압박", tone="red")
add(a=115, kind="orbitthink", bg="bg-ink", key="cut_man_tense",
    thoughts=[("침묵이 생기면 안 될 것 같고", 115), ("재미없다고 생각하면 어쩌지", 116),
              ("좋게 평가받고 싶다", 117)])
add(a=118, kind="strikelist", bg="bg-grid", title="질문하는 진짜 이유",
    items=[("상대가 궁금해서", 119, (119, 0.9), False), ("대화를 살리려고", 120, None, True)])
add(a=121, kind="iconside", bg="bg-ember", key="ico_hyena", title="하이에나의 태도",
    sub="반응을 쫓고 불안으로 움직인다", at_sub=122, size=520)
add(a=125, kind="echo", bg="bg-dust", key="cut_man_think", text="다음에 뭐 말해야 되지?", at=126,
    mute=[126])
add(a=128, kind="icon", bg="bg-teal", key="ico_lion", title="사자의 태도",
    sub="침묵이 조금 생겨도 괜찮다", at_sub=129, size=480)
add(a=130, kind="timeline", bg="bg-spot", title="사자의 대화",
    nodes=[("듣고", 130), ("잠시 생각하고", 131), ("내 의견도 말하기", 132)])
add(a=133, kind="morph", bg="bg-canvas", x="억지로 유지", y="서로 알아가기", at_y=134)
add(a=135, kind="chapter", bg="bg-spot", num="2", word="깊은 질문 전에, 허락",
    sub="조금 더 깊은 질문을 할 때")

# ── 2  ask permission first ─────────────────────────────────────────────────
add(a=138, kind="phone", bg="bg-canvas", title="안전한 질문들",
    msgs=[("m", "무슨 일 하세요?", 140), ("m", "취미가 뭐예요?", 141), ("m", "여행 좋아하세요?", 142)],
    mute=[140, 141, 142])
add(a=143, kind="bars", bg="bg-ink", title="이어지기는 하지만",
    bars=[("대화 길이", 0.82, 143, "cyan"), ("대화 깊이", 0.14, 144, "dim")])
add(a=145, kind="stairs", bg="bg-teal", title="조금 더 개인적인 이야기", down=True,
    steps=[("연애관", 147), ("좋아하게 되는 기준", 148), ("중요하게 보는 것", 149), ("과거의 경험", 150)])
add(a=151, kind="distance", bg="bg-dust", title="남녀 사이의 거리", gap_from=620, gap_to=150,
    at=152)
add(a=153, kind="pulse", bg="bg-ember", title="갑자기 깊은 질문을 던지면", shape="spike",
    at=154, label="상대가 부담스러울 수 있습니다", at_label=155)
add(a=156, kind="iconbub", bg="bg-grid", key="ico_cushion", title="쿠션 멘트 한 번",
    bubble="이건 조금 개인적인 질문인데|하나 물어봐도 돼요?", at_bub=157, mute=[157])
add(a=158, kind="checklist", bg="bg-canvas", title=None,
    items=[("상대가 괜찮다고 하면", 158), ("그때 물어보기", 159)])
add(a=160, kind="quote", bg="soft:br_man_calm",
    quotes=[("사람 만날 때 어떤 순간에|이 사람의 진짜 모습이 나온다고 생각해요?", 161, "예를 들면"),
            ("연애할 때 가장 중요하게 보는 건 뭐예요?", 162, "또는")], mute=[161, 162])
add(a=163, kind="split",
    left=dict(n="그냥 갑자기", head="“이상형이 뭐예요?”", at=165, photo="br_interview"),
    right=dict(n="허락을 구하고", head="훨씬 자연스럽게", at=167, photo="br_man_calm"))
add(a=169, kind="alert", bg="bg-spot", head="질문 자체를 외우면", sub="또 면접이 됩니다", at_sub=170)
add(a=171, kind="cards10", bg="photo:br_interview", title="소개팅에서 갑자기 꺼낸",
    count=10, at=176, stamp="면접", at_stamp=177, mute=[174])
add(a=178, kind="ring", bg="bg-ink", title="지금 대화는 얼마나 깊어졌나", start=0.05, end=0.6,
    at=180, label="질문보다 대화의 깊이", at_label=178)
add(a=181, kind="lamps", bg="bg-teal", title="깊은 질문으로 가도 되는 신호",
    items=[("상대가 자기 이야기를 더 하고", 181), ("나도 내 이야기를 하고", 182), ("서로 편하게 대화한다", 183)])
add(a=184, kind="meter", bg="bg-grid", title="그렇다면", start=0.55, end=0.88, at=184,
    left="얕음", right="깊음", tone="cyan", label="한 단계 더 깊은 질문으로")
add(a=185, kind="rows", bg="bg-ember", title="반대로",
    rows=[("기본 대화도 어색한데", "갑자기 개인적인 이야기", 186, 187),
          ("상대 입장에서는", "부담", 188, (188, 0.6))])
add(a=189, kind="duo", bg="bg-dust", key="ico_lion", title="사자의 태도",
    left="상대를 존중하면서도", right="필요할 땐 한 걸음 더", at_l=191, at_r=193)

# ── conclusion ──────────────────────────────────────────────────────────────
add(a=194, kind="converge", bg="bg-canvas", title="깊어지는 대화의 차이",
    chips=["MBTI", "주말", "영화", "취미", "여행", "음식"], at_chips=196,
    center="주제의 개수가 아니다", at_center=197)
add(a=198, kind="flow", bg="bg-ink", title="같은 주제에서도",
    items=[("상대를 보고", 199, "a"), ("나를 보여주고", 200, "am"), ("한 단계 깊이", 202, "cy")])
add(a=203, kind="cards10", bg="bg-spot", title="외울 필요 없는", count=100, at=204, stamp="불필요",
    at_stamp=1.9)
add(a=205, kind="toggle", bg="bg-teal", lead="스스로에게 물어보세요",
    q1="주제를 찾고 있는가?", q2="이 사람을 알아가고 있는가?", at_q1=206, at_q2=208,
    mute=[206, 208])
add(a=209, kind="kinetic", bg="bg-spot", words=[("질문 하나만 바꿔도", 209, "md"),
                                              ("대화가 달라진다", 210, "xl cy")])
add(a=211, kind="kinetic", bg="bg-ember", words=[("멘트", 211, "lg"), ("보다", 212, "md"),
                                               ("태도", (212, 0.3), "xl am")], shrink=(0, 212))
add(a=213, kind="rows", bg="bg-ink", title=None,
    rows=[("침묵을 견디지 못하면", "새 질문만 찾게 되고", 213, 214),
          ("잘 보여야 한다는 생각", "내 이야기를 숨기고", 215, 216),
          ("거절이 두려우면", "깊은 질문을 못 한다", 217, 218)])
add(a=219, kind="person", bg="bg-teal", key="cut_man_calm", side="left", think=True,
    bubbles=[("대화 소재보다", 220), ("그녀 앞에서 변하는 내 태도", 221)])
add(a=223, kind="cta", bg="photo:br_lecture", head="비공개 특강", sub="이 부분을 더 자세하게 정리했습니다",
    at_sub=224, foot="설명란에서 확인", at_foot=227)
add(a=228, kind="typo", bg="bg-spot", rows=[("태도가 달라지면", 228, "lg"),
                                          ("대화가 달라집니다", 229, "xl cy")])

SCENES = S


def check_forms():
    """Fail the build if any form or still is used more than twice."""
    import re
    from collections import Counter
    forms = Counter(s["kind"] for s in S)
    over = {k: v for k, v in forms.items() if v > 2}
    stills = Counter()
    for s in S:
        stills.update(re.findall(r"\b(br_\w+|ico_\w+|cut_\w+)\b", repr(s)))
    over_s = {k: v for k, v in stills.items() if v > 2}
    assert not over and not over_s, (over, over_s)


check_forms()
