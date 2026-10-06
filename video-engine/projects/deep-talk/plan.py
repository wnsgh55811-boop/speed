# -*- coding: utf-8 -*-
"""대화가 깊어지는 사람 — scene plan (Fish Audio take, 342.3s, 230 spoken lines).

Each scene starts on line `a` and runs until the next scene's first line.
`at`: int = onset of that spoken line, float = seconds into the scene.
`mute`: lines whose words are already on screen verbatim (chat bubbles,
the hook quote), so the bottom caption is dropped for them.
"""
TOTAL = 343.0
AUDIO = "assets/audio/voice.wav"

S = []
add = lambda **k: S.append(k)  # noqa: E731

# ── 0  cold open ────────────────────────────────────────────────────────────
add(a=0, kind="hook", bg="photo:br_date_stuck", quote="“이제 무슨 얘기하지?”", at_quote=2,
    mute=[2])
add(a=3, kind="checklist", bg="bg-ink", title="처음 만난 그녀에게 물어본 것",
    items=[("직업", 4), ("취미", 5), ("여행", 6), ("좋아하는 음식", 7)])
add(a=8, kind="meter", bg="bg-canvas", title="남은 대화 소재", start=0.82, end=0.08, at=8,
    left="바닥", right="충분", tone="amber", label="새로운 주제 찾기 시작", at_label=9)
add(a=10, kind="chat", bg="soft:br_date_wide", title="새 주제 찾는 중",
    msgs=[("m", "MBTI는 뭐예요?", 10), ("m", "주말에는 뭐 해요?", 11), ("m", "영화 좋아하세요?", 12)],
    mute=[10, 11, 12])
add(a=13, kind="lines", bg="bg-grid", title="이어지는 대화, 그대로인 거리",
    xlab="대화 시간", ylab="정도",
    series=[("대화량", "M0 430 C200 380 420 250 620 170 S880 60 1000 40", "cyan", 13, 760, 60),
            ("친밀감", "M0 420 C250 418 500 412 720 414 S900 410 1000 408", "amber", 14, 770, 385)])
add(a=15, kind="icon", bg="bg-teal", key="ico_iceberg", title="표면에서만 맴도는 대화",
    orbit=True, size=470)
add(a=17, kind="typo", bg="bg-spot",
    rows=[("왜 그럴까?", 17, "lg"), ("대화 주제가 부족해서", 18, "md dim")], strike=(1, 18))
add(a=19, kind="depth", bg="bg-ink", title="같은 주제, 다른 깊이",
    levels=[("같은 주제", 19), ("조금 더", 20), ("훨씬 더 깊게", (20, 0.9))])
add(a=21, kind="cards", bg="bg-canvas", title="오늘 이야기할 두 가지",
    cards=[dict(n="처음 만난 사람", head="어색함을 줄이고", at=22, photo="br_date_wide"),
           dict(n="조금 친해진 사람", head="더 가까워지는", at=23, photo="br_couple_close", tone="hot")])
add(a=26, kind="chapter", bg="bg-spot", num="1", word="주제에서 사람으로")

# ── 1  topic → person ───────────────────────────────────────────────────────
add(a=28, kind="chat", bg="soft:br_quiet_cafe", title="흔한 대화",
    msgs=[("w", "저 카페 가는 거 좋아해요.", 29), ("m", "어떤 카페 좋아하세요?", 31),
          ("w", "조용한 카페 좋아해요.", 33), ("m", "커피는 뭐 좋아하세요?", 35)],
    mute=[29, 31, 33, 35])
add(a=36, kind="cards", bg="bg-dust", title="그래서 알게 된 것",
    cards=[dict(n="카페에 대해", head="조용한 곳 · 커피 취향", at=37),
           dict(n="그 사람에 대해", head="거의 없음", at=39, tone="muted")], vs=True)
add(a=41, kind="morph", bg="bg-teal", title="한 단계만 바꾸면", x="질문 하나 더", y="한 단계 깊게",
    at_y=(41, 0.9))
add(a=42, kind="chat", bg="soft:br_busy_cafe", title="한 단계 바꾼 대화",
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
           dict(n="즉흥형?", head="가서 정하는 편", at=67, photo="br_travel_free")], vs=True,
    mute=[])
add(a=69, kind="chat", bg="soft:br_travel_plan",
    msgs=[("w", "저는 계획 다 짜놓는 편이에요.", 70)], title="그녀의 대답", mute=[70])
add(a=72, kind="meter", bg="bg-teal", title="이 한마디에 담긴 정보", start=0.12, end=0.92,
    at=73, left="여행 정보", right="사람에 대한 정보", tone="cyan")
add(a=74, kind="sliders", bg="bg-canvas", title="평소에는 어떤 사람일까",
    rows=[("계획적", "즉흥적", 0.16, 74), ("통제 선호", "흐름에 맡김", 0.22, 75),
          ("새로운 것", "익숙한 것", 0.5, 76)])
add(a=78, kind="morph", bg="bg-spot", x="여행 이야기", y="사람 이야기", at_y=79)
add(a=80, kind="typo", bg="bg-ink", rows=[("성격 분석", 80, "lg"), ("이 아닙니다", (81, 0.9), "md dim")],
    strike=(0, (81, 0.6)))
add(a=82, kind="icon", bg="bg-teal", key="ico_iceberg", title="수면 아래까지",
    sub="보이는 사실은 일부일 뿐", at_sub=83, size=450)
add(a=84, kind="depth", bg="bg-dust", title="질문을 한 단계씩",
    levels=[("뭘 좋아해요?", 84), ("왜 좋아해요?", 85), ("평소에도 그런 편이에요?", 86)],
    top="사실", bottom="사람")
add(a=88, kind="flow", bg="bg-grid", items=[("소재 하나", 88, ""), ("그 사람", 89, "cy")],
    foot="훨씬 많이 알 수 있습니다", at_foot=89)

# ── 1b  the common mistake ──────────────────────────────────────────────────
add(a=90, kind="person", bg="bg-ember", key="cut_man_think", side="left", think=True,
    bubbles=[("자주 하는 실수 하나", 91), ("상대 이야기만 끌어내기", 92)])
add(a=93, kind="flow", bg="bg-canvas", title="질문과 대답만 오가는 대화",
    items=[("상대의 말", 93, "a"), ("질문", 94, "q"), ("대답", 95, "a"), ("또 질문", 96, "q")], loop=True)
add(a=97, kind="distance", bg="bg-ink", title="대화는 계속되는데", gap_from=620, gap_to=620, at=97,
    note="거리는 그대로", at_note=98, chatter=True)
add(a=99, kind="scale", bg="bg-spot", title="한쪽만 보여주는 대화", left="상대", right="나",
    tilt_at=100)
add(a=102, kind="flow", bg="bg-teal", title="질문했다면",
    items=[("질문", 102, "q"), ("내 생각", 103, "cy")], foot="같이 들어가야 합니다", at_foot=103)
add(a=104, kind="chat", bg="soft:br_couple_close", title="내 이야기 덧붙이기",
    msgs=[("m", "저는 계획 너무 많이 세우면 오히려 피곤하더라고요.|어디 갈지만 정하고 나머지는 가서 정하는 편이에요.",
           104, "내 생각")], mute=[104, 105])
add(a=106, kind="typo", bg="bg-dust", rows=[("질문에", 106, "md dim"), ("내 이야기 한 스푼", (106, 0.5), "xl am")])
add(a=107, kind="scale", bg="bg-canvas", title="대화는", left="상대", right="나", tilt_at=107,
    level_at=109)
add(a=111, kind="person", bg="bg-dust", key="cut_man_tense", side="left", think=True,
    bubbles=[("마음에 드는 사람 앞에서는", 111), ("잘 안 됩니다", 112)])
add(a=113, kind="meter", bg="soft:br_man_nervous", title="대화를 잘해야 한다는 압박", start=0.18, end=0.94,
    at=114, left="여유", right="압박", tone="red")
add(a=115, kind="person", bg="bg-ink", key="cut_man_tense", side="right", think=True,
    bubbles=[("침묵이 생기면 안 될 것 같고", 115), ("재미없다고 생각하면 어쩌지", 116),
             ("좋게 평가받고 싶다", 117)])
add(a=118, kind="cards", bg="bg-grid", title="질문하는 진짜 이유",
    cards=[dict(n="✕", head="상대가 궁금해서", at=119, tone="muted"),
           dict(n="실제로는", head="대화를 살리려고", at=120, tone="hot")], vs=True)
add(a=121, kind="icon", bg="bg-ember", key="ico_hyena", title="하이에나의 태도",
    sub="반응을 쫓고 불안으로 움직인다", at_sub=122, size=520, side=True)
add(a=125, kind="person", bg="bg-dust", key="cut_man_think", side="right", think=True,
    bubbles=[("“다음에 뭐 말해야 되지?”", 126)], mute=[126])
add(a=128, kind="icon", bg="bg-teal", key="ico_lion", title="사자의 태도",
    sub="침묵이 조금 생겨도 괜찮다", at_sub=129, size=560, side=True)
add(a=130, kind="flow", bg="bg-spot", title="사자의 대화",
    items=[("듣고", 130, "a"), ("잠시 생각하고", 131, ""), ("내 의견도 말하기", 132, "cy")])
add(a=133, kind="morph", bg="bg-canvas", x="억지로 유지", y="서로 알아가기", at_y=134)
add(a=135, kind="chapter", bg="bg-spot", num="2", word="깊은 질문 전에, 허락",
    sub="조금 더 깊은 질문을 할 때")

# ── 2  ask permission first ─────────────────────────────────────────────────
add(a=138, kind="chat", bg="bg-canvas", title="안전한 질문들",
    msgs=[("m", "무슨 일 하세요?", 140), ("m", "취미가 뭐예요?", 141), ("m", "여행 좋아하세요?", 142)],
    mute=[140, 141, 142])
add(a=143, kind="meter", bg="bg-ink", title="이어지기는 하지만, 깊이는", start=0.0, end=0.22,
    at=143, left="얕음", right="깊음", tone="cyan")
add(a=145, kind="depth", bg="bg-teal", title="조금 더 개인적인 이야기",
    levels=[("연애관", 147), ("좋아하게 되는 기준", 148), ("관계에서 중요한 것", 149),
            ("과거의 경험", 150)], top="얕음", bottom="깊음")
add(a=151, kind="distance", bg="bg-dust", title="남녀 사이의 거리", gap_from=620, gap_to=150,
    at=152)
add(a=153, kind="meter", bg="bg-ember", title="갑자기 깊은 질문을 던지면", start=0.1, end=0.9,
    at=155, left="편안", right="부담", tone="red")
add(a=156, kind="icon", bg="bg-dust", key="ico_cushion", title="쿠션 멘트 한 번", size=460)
add(a=157, kind="chat", bg="bg-ink", title="먼저 묻기",
    msgs=[("m", "이건 조금 개인적인 질문인데|하나 물어봐도 돼요?", 157, "쿠션 멘트")],
    mute=[157])
add(a=158, kind="checklist", bg="bg-grid", title=None,
    items=[("상대가 괜찮다고 하면", 158), ("그때 물어보기", 159)])
add(a=160, kind="chat", bg="soft:br_man_calm", title="예를 들면",
    msgs=[("m", "사람 만날 때 어떤 순간에|이 사람의 진짜 모습이 나온다고 생각해요?", 161),
          ("m", "연애할 때 가장 중요하게 보는 건 뭐예요?", 162)], mute=[161, 162])
add(a=163, kind="cards", bg="bg-canvas", title="같은 깊이, 다른 온도",
    cards=[dict(n="그냥 갑자기", head="“이상형이 뭐예요?”", at=165, tone="muted"),
           dict(n="허락을 구하고", head="훨씬 자연스럽게", at=167, tone="hot")], vs=True)
add(a=169, kind="typo", bg="bg-spot", rows=[("질문 자체를", 170, "lg"), ("외우면 안 됩니다", (170, 0.8), "lg am")])
add(a=171, kind="cards10", bg="photo:br_interview", title="소개팅에서 갑자기 꺼낸",
    count=10, at=176, stamp="면접", at_stamp=177, mute=[174])
add(a=178, kind="meter", bg="bg-ink", title="지금 대화는 얼마나 깊어졌나", start=0.05, end=0.6,
    at=180, left="얕음", right="깊음", tone="cyan", label="질문보다 대화의 깊이")
add(a=181, kind="checklist", bg="bg-teal", title="깊은 질문으로 가도 되는 신호",
    items=[("상대가 자기 이야기를 더 하고", 181), ("나도 내 이야기를 하고", 182),
           ("서로 편하게 대화한다", 183)])
add(a=184, kind="meter", bg="bg-grid", title="그렇다면", start=0.55, end=0.88, at=184,
    left="얕음", right="깊음", tone="cyan", label="한 단계 더 깊은 질문으로")
add(a=185, kind="rows", bg="bg-ember", title="반대로",
    rows=[("기본 대화도 어색한데", "갑자기 개인적인 이야기", 186, 187),
          ("상대 입장에서는", "부담", 188, (188, 0.6))])
add(a=189, kind="icon", bg="bg-dust", key="ico_lion", title="사자의 태도",
    sub="밀어붙이지 않고, 존중하며 시도한다", at_sub=191, size=520, side=True)

# ── conclusion ──────────────────────────────────────────────────────────────
add(a=194, kind="cards", bg="bg-canvas", title="깊어지는 대화의 차이",
    cards=[dict(n="계속 표면", head="주제를 많이 아는 사람", at=196, tone="muted"),
           dict(n="깊어지는", head="사람을 보는 사람", at=197, tone="hot")], vs=True)
add(a=198, kind="flow", bg="bg-ink", title="같은 주제에서도",
    items=[("상대를 보고", 199, "a"), ("나를 보여주고", 200, "am"), ("한 단계 깊이", 202, "cy")])
add(a=203, kind="cards10", bg="bg-spot", title="외울 필요 없는", count=100, at=204, stamp="불필요",
    at_stamp=1.9)
add(a=205, kind="toggle", bg="bg-teal", lead="스스로에게 물어보세요",
    q1="주제를 찾고 있는가?", q2="이 사람을 알아가고 있는가?", at_q1=206, at_q2=208,
    mute=[206, 208])
add(a=209, kind="typo", bg="bg-spot", rows=[("질문 하나만 바꿔도", 209, "md"),
                                          ("대화가 달라진다", 210, "xl cy")])
add(a=211, kind="morph", bg="bg-ember", x="멘트", y="태도", op="보다", at_y=212,
    title="결국 차이는")
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
