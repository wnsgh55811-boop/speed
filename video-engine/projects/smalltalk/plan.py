# -*- coding: utf-8 -*-
"""스몰토크가 쉬워지는 방법 — scene plan (Fish Audio take, 557.14s, 411 spoken lines).

Each scene starts on line `a` and runs until the next scene's first line.
`at`: int = onset of that spoken line, float = seconds into the scene,
(line, s) = s seconds after that line's onset.
`mute`: lines whose words are already on screen verbatim (chat bubbles,
quotes, search results), so the bottom caption is dropped for them.
"""
TOTAL = 557.14
AUDIO = "assets/audio/voice.wav"

S = []
add = lambda **k: S.append(k)  # noqa: E731

# ── 0  hook: the promise, then the habit that breaks it ────────────────────
# the cold open is the photo and the voice; only the caption carries words
add(a=0, kind="photo", bg="photo:br_date_pause")
add(a=2, kind="flow", bg="bg-ink", title="대부분의 사람들은",
    items=[("어색할까 봐", 3, ""), ("질문부터", 4, "q")])
add(a=5, kind="chat", bg="soft:br_interview_date", title="흔한 첫 질문",
    msgs=[("m", "무슨 일 하세요?", 5), ("m", "주말에는 뭐 하세요?", 6), ("m", "취미가 뭐예요?", 7)],
    mute=[5, 6, 7])
add(a=8, kind="flow", bg="bg-canvas", title="문제는",
    items=[("질문", 9, "q"), ("질문", (9, 0.45), "q"), ("또 질문", (9, 0.9), "q")],
    foot="그래도 편해지지 않는다", at_foot=10)
add(a=11, kind="lines", bg="bg-grid", title="대답이 짧아질수록", xlab="대화 시간", ylab="정도",
    series=[("상대 대답", "M0 60 C220 90 420 230 620 330 S880 420 1000 432", "cyan", 11, 30, 20),
            ("다음 질문 찾기", "M0 420 C250 410 460 300 640 190 S880 60 1000 40", "amber", 12, 990, -2)])
add(a=13, kind="icon", bg="bg-spot", key="ico_blank", title="머릿속이 하얘진다", at_title=14,
    flash=(14, 0.15), size=440)
add(a=15, kind="typo", bg="bg-ink", rows=[("“이제 무슨 얘기하지?”", 15, "xl")], mute=[15])
add(a=16, kind="cards", bg="bg-canvas", title="오늘 이야기할 것",
    cards=[dict(n="WHY", head="스몰토크가 어려워지는 이유", at=17),
           dict(n="HOW", head="질문 없이도 이어가는 법", at=18, tone="hot")])

# ── 1  the two-second silence ───────────────────────────────────────────────
add(a=20, kind="chapter", bg="bg-spot", num="1", word="소개팅의 2초")
add(a=22, kind="photo", bg="photo:br_her_laugh", chip="잘 이어지던 대화", at_chip=23)
add(a=24, kind="timer", bg="bg-ink", title="상대가 말을 끝낸 뒤", secs=2, at=26,
    label="아무 말도 나오지 않는다", at_label=27)
add(a=28, kind="icon", bg="bg-ember", key="ico_alarm", title="머릿속 비상벨", shake=29,
    size=500, side=True)
add(a=30, kind="person", bg="bg-dust", key="cut_man_anx", side="left", think=True,
    bubbles=[("뭐라도 말해야 하는데", 30), ("분위기 싸해지는 거 아니야?", 31), ("다음 질문 뭐 하지?", 32)],
    mute=[30, 31, 32])
add(a=33, kind="chat", bg="soft:br_date_pause", title="결국, 가장 익숙한 질문",
    msgs=[("m", "주말에는 뭐 하세요?", 35), ("w", "그냥 친구 만나거나 쉬어요.", 37)], mute=[35, 37])
add(a=38, kind="chat", bg="bg-canvas", title="다시 조용해지고, 또",
    msgs=[("m", "여행 좋아하세요?", 40), ("w", "네 좋아해요.", 42)], mute=[40, 42])
add(a=43, kind="flow", bg="bg-teal", title="그리고 또 침묵",
    items=[("질문", 43, "q"), ("짧은 대답", (43, 0.35), "a"), ("침묵", (43, 0.7), "dim")], loop=True)
add(a=45, kind="photo", bg="photo:br_walk_home", quote="여자랑 스몰토크하는 게|왜 이렇게 재미가 없지?",
    at_quote=46, who="m", mute=[46])
add(a=47, kind="search", bg="soft:br_phone_list", title="다음 소개팅 전에", query="소개팅 질문 리스트",
    at_query=48, results=[("여자와 대화 소재 100가지", 49), ("첫 만남에서 하면 좋은 질문", 50),
                          ("MBTI별 대화법", 51)], mute=[49, 50, 51])
add(a=53, kind="typo", bg="bg-spot", kicker=("그런데 이건", 53),
    rows=[("문제를 잘못 본 것", 54, "xl am")])
add(a=55, kind="typo", bg="bg-ink", kicker=("스몰토크가 어려운 이유", 55),
    rows=[("대화 소재 부족", 56, "lg"), ("유머 부족", 57, "lg")],
    strike=[(0, (56, 0.7)), (1, (57, 0.6))])
add(a=58, kind="icon", bg="bg-teal", key="ico_qcards", title="머릿속은 소재로 가득", at_title=59,
    sub="정작 눈앞의 사람은 보지 못한다", at_sub=60, size=460, side=True)

# ── 2  with a friend it is easy ─────────────────────────────────────────────
add(a=62, kind="chapter", bg="bg-spot", num="2", word="친구와는 왜 쉬울까")
add(a=65, kind="chat", bg="soft:br_friends_meal", title="친구에게 이렇게 묻나요?",
    msgs=[("m", "너 취미가 뭐야?", 66), ("m", "주말에는 뭐 해?", 67), ("m", "여행 좋아해?", 68)],
    xout=69, mute=[66, 67, 68])
add(a=70, kind="typo", bg="bg-canvas", kicker=("질문 대신", 70),
    rows=[("눈앞에 있는 걸로 말한다", (70, 0.4), "lg cy")])
add(a=71, kind="photo", bg="photo:br_suit", quote="너 오늘 어디 면접 보러 가냐?", at_quote=72,
    who="m", mute=[72])
add(a=74, kind="photo", bg="photo:br_sneakers", quote="오 흰 신발이면 밟아줘야지?", at_quote=75,
    who="m", pos="high", mute=[75])
add(a=77, kind="flow", bg="bg-ink", title="별거 아닌 한마디에서",
    items=[("한마디", 78, "a"), ("대화가 이어진다", 79, "cy")])
add(a=80, kind="typo", bg="bg-spot", kicker=("왜 그럴까?", 80),
    rows=[("재미있는 말을 준비해서", 81, "md dim"), ("눈앞의 사람을 보고 있어서", 82, "lg cy")],
    strike=(0, (81, 1.0)))
add(a=83, kind="person", bg="bg-ember", key="cut_man_think", side="right", think=True,
    head=("잘하려 할수록, 머릿속으로", 83),
    bubbles=[("다음에는 뭐라고 하지?", 86), ("이 질문 괜찮나?", 87), ("재미없는 사람처럼 보이면 어떡하지?", 88)],
    mute=[86, 87, 88])
add(a=89, kind="cards", bg="bg-canvas", title="그런데 이렇게 되면", vs=True,
    cards=[dict(n="겉으로는", head="상대를 보는 중", at=90),
           dict(n="실제로는", head="상대를 못 보는 중", at=91, tone="hot")])
add(a=92, kind="checklist", bg="bg-ember", title="놓치고 있는 것",
    items=[("상대의 표정", 92), ("방금 강조한 말", 93), ("둘 사이의 분위기", 94)],
    empty_at=95, empty_text="잘 보이지 않는다")
add(a=96, kind="typo", bg="bg-ink", kicker=("머릿속에는 계속", 96),
    rows=[("“다음에 무슨 말 하지?”", 97, "xl")], mute=[97])

# ── 3  look first, then say what you felt ──────────────────────────────────
add(a=99, kind="chapter", bg="bg-spot", num="3", word="질문보다 관찰")
add(a=101, kind="morph", bg="bg-teal", title="막혔을 때", x="질문 하나 더", y="눈앞을 한번 보기",
    at_y=102)
add(a=104, kind="flow", bg="bg-canvas", title="질문부터 하지 말고",
    items=[("보고", 105, "a"), ("느낀 걸", (105, 0.55), ""), ("먼저 표현", 106, "cy")])
add(a=107, kind="photo", bg="photo:br_syrup", chip="시럽 세 번 추가", at_chip=109, pos="high")
add(a=110, kind="cards", bg="bg-ink", vs=True,
    cards=[dict(n="보통은", head="“단 거 좋아하세요?”", body="틀린 질문은 아니다", at=111, tone="muted"),
           dict(n="이렇게도", head="“커피보다 디저트에 가까운데요?”", at=114, tone="hot")],
    mute=[111])
add(a=115, kind="person", bg="bg-dust", key="cut_woman_smile", side="left",
    bubbles=[("제가 원래 엄청 달게 먹어요.", 116), ("오늘만 그래요. 좀 피곤해서요.", 118)],
    mute=[116, 118])
add(a=120, kind="tree", bg="bg-grid", root="커피 한 잔에서",
    branches=[("단 걸 좋아하는 이야기", None, 121), ("오늘 피곤한 이유", None, 122),
              ("요즘 바빴던 이야기", None, 123)])
add(a=124, kind="icon", bg="bg-teal", key="ico_coffee", title="질문이 아니라",
    sub="대화할 공간을 만든 것", at_sub=126, size=430, side=True)
add(a=127, kind="photo", bg="photo:br_keyring_bag", chip="키링 두세 개", at_chip=129, pos="high")
add(a=130, kind="toggle", bg="bg-canvas", lead="보통은 · 이렇게도",
    q1="이런 거 좋아하세요?", q2="가방보다 키링이 주인공 같은데요?", at_q1=131, at_q2=134,
    mute=[131, 134])
add(a=135, kind="person", bg="bg-ember", key="cut_woman_talk", side="right",
    bubbles=[("제가 이런 거 모으는 거 좋아해요.", 136)], mute=[136])
add(a=138, kind="icon", bg="bg-spot", key="ico_keyring", title="억지 질문이 필요 없다",
    at_title=139, size=430, side=True)
add(a=140, kind="checklist", bg="bg-ink", title="자연스럽게 나오는 이야기",
    items=[("어디서 샀는지", 140), ("왜 좋아하는지", 141), ("언제부터 모았는지", 142),
           ("좋아하는 캐릭터", 143)])
add(a=145, kind="typo", bg="bg-canvas", kicker=("중요한 건", 145),
    rows=[("웃긴 말 만들기", 146, "lg"), ("엄청난 관찰력", 147, "lg")],
    strike=[(0, (146, 0.8)), (1, (147, 0.9))])
add(a=148, kind="flow", bg="bg-teal", title="그냥",
    items=[("한번 보고", 149, "a"), ("실제로 느낀 걸", 150, ""), ("조금 표현", 151, "cy")])

# ── 3b  question vs observation ────────────────────────────────────────────
add(a=152, kind="morph", bg="bg-teal", title="차이가 하나 있다", x="질문", y="관찰 + 표현", op="vs",
    at_y=(152, 0.9))
add(a=154, kind="scale", bg="bg-spot", title="질문은 답을 요구한다", left="상대", right="나",
    tilt_at=155)
add(a=156, kind="chat", bg="bg-canvas", title="질문이 이어지면",
    msgs=[("m", "취미가 뭐예요?", 156), ("w", "(뭔가 답해야 한다)", 158),
          ("m", "여행 좋아하세요?", 159), ("w", "(또 대답해야 한다)", 161)], mute=[156, 159])
add(a=162, kind="meter", bg="bg-ink", title="대화는 이어지지만, 알맹이는", start=0.55, end=0.08,
    at=163, left="없음", right="가득", tone="amber")
add(a=164, kind="chat", bg="soft:br_her_laugh", title="관찰 + 표현 = 내 생각이 들어간다",
    msgs=[("m", "오늘 되게 바빴던 사람처럼 보여요.", 166, "내 생각"),
          ("m", "가방보다 키링이 더 눈에 들어오는데요?", 167, "내 생각"),
          ("m", "이 정도면 커피보다는 디저트죠.", 168, "내 생각")], mute=[166, 167, 168])
add(a=169, kind="tree", bg="bg-grid", root="상대의 반응",
    branches=[("“맞아요”", None, 170), ("“아니에요”", None, 171), ("“그게 왜냐면…”", None, 172)])
add(a=173, kind="scale", bg="bg-teal", title="대화를 이어갈 책임", left="상대", right="나",
    tilt_at=173, level_at=174)

# ── 4  both are nervous ─────────────────────────────────────────────────────
add(a=176, kind="chapter", bg="bg-spot", num="4", word="소개팅에서 특히")
add(a=178, kind="cards", bg="bg-canvas", title="소개팅에서는",
    cards=[dict(n="나만", head="긴장하는 게 아니다", at=179, photo="br_man_nervous"),
           dict(n="상대도", head="나를 처음 보는 중", at=180, photo="br_couple_close", tone="hot")])
add(a=182, kind="person", bg="bg-dust", key="cut_woman_tense", side="right", think=True,
    head=("상대 역시", 182),
    bubbles=[("무슨 말을 해야 하지?", 183), ("너무 말이 없으면 이상해 보일까?", 184), ("뭘 물어봐야 하지?", 185)],
    mute=[183, 184, 185])
add(a=187, kind="chat", bg="soft:br_interview_date", title="남자는 계속 질문",
    msgs=[("m", "어디 사세요?", 189), ("m", "무슨 일 하세요?", 190), ("m", "주말에는 뭐하세요?", 191)],
    mute=[189, 190, 191])
add(a=193, kind="icon", bg="bg-ember", key="ico_qcards", title="계속 괜찮은 답을",
    sub="꺼내놔야 하는 상대", at_sub=195, size=420, side=True)
add(a=196, kind="rows", bg="bg-ink", title="답할 때마다 고민",
    rows=[("너무 짧게 말하면", "성의 없어 보이고", 196, 197),
          ("너무 길게 말하면", "혼자 말하는 것 같고", 198, 199)])
add(a=200, kind="meter", bg="bg-canvas", title="매 질문마다 쌓이는 피로", start=0.12, end=0.9,
    at=201, left="여유", right="지침", tone="red", label="생각보다 사람을 지치게 만든다", at_label=202)
add(a=203, kind="bars", bg="bg-grid", title="시간이 지날수록, 답변 길이", at=(203, 0.3),
    bars=[("1번째", 0.92), ("2번째", 0.7), ("3번째", 0.48), ("4번째", 0.3), ("5번째", 0.14)],
    axis=("짧음", "김"))
add(a=205, kind="person", bg="bg-ember", key="cut_man_tense", side="left", think=True,
    bubbles=[("나한테 관심이 없나?", 206), ("더 열심히 질문해야지", 207)], mute=[206])
add(a=208, kind="distance", bg="bg-teal", title="둘 다 잘해보려 했는데", gap_from=260, gap_to=780,
    at=209, note="점점 불편해진다", at_note=210)

# ── 5  hyena and lion ───────────────────────────────────────────────────────
add(a=211, kind="chapter", bg="bg-spot", num="5", word="기술보다 태도")
add(a=214, kind="flow", bg="bg-ember", title="불안의 고리",
    items=[("침묵", 214, "dim"), ("불안", 215, "am"), ("다음 질문", 217, "q")], loop=True)
add(a=218, kind="icon", bg="bg-dust", key="ico_hyena", title="하이에나의 태도", at_title=219,
    size=440, side=True)
add(a=220, kind="morph", bg="bg-canvas", title="하이에나의 목적", x="상대를 알아가기", y="좋은 반응 받아내기",
    at_y=224)
add(a=225, kind="meter", bg="bg-ink", title="하이에나의 불안", start=0.6, end=0.18, at=226,
    then=(0.92, 228), left="안심", right="불안", tone="red")
add(a=229, kind="flow", bg="bg-ember", title="그래서 계속 움직인다",
    items=[("다음 질문", 230, "q"), ("새로운 소재", 231, ""), ("분위기 살리기", 232, "am")])
add(a=233, kind="timer", bg="bg-teal", title="반대로, 침묵이 생겨도", secs=2, at=234, tone="cyan",
    label="조금 기다릴 수 있다", at_label=235)
add(a=236, kind="flow", bg="bg-canvas", title=None,
    items=[("상대의 말을 생각하고", 236, "a"), ("느낀 걸 표현한다", 237, "cy")])
add(a=238, kind="icon", bg="bg-dust", key="ico_lion", title="사자의 태도", at_title=239,
    size=500, side=True)
add(a=240, kind="typo", bg="bg-spot", kicker=("사자라고 해서", 240),
    rows=[("말없이 무게 잡기", 241, "lg"), ("여유 있는 척", 242, "lg")],
    strike=[(0, (241, 0.9)), (1, (242, 1.0))])
add(a=243, kind="checklist", bg="soft:br_window_talk", title="오히려 더 자연스럽게",
    items=[("잘 듣고", 244), ("재미있으면 말하고", 245), ("궁금하면 묻고", 246), ("내 생각도 말한다", 247)])
add(a=248, kind="cards", bg="bg-canvas", vs=True,
    cards=[dict(n="머릿속에서", head="정답 찾기", at=250, tone="muted"),
           dict(n="눈앞의", head="사람에게 집중", at=252, tone="hot")])

# ── 5b  the travel example ──────────────────────────────────────────────────
add(a=254, kind="photo", bg="photo:br_planner", quote="저는 여행 가면|계획을 엄청 많이 세워요.",
    at_quote=257, who="w", mute=[257])
add(a=258, kind="chat", bg="bg-ember", title="하이에나는", icon="ico_hyena",
    msgs=[("m", "여행 좋아하세요?", 260), ("m", "어디 가봤어요?", 261),
          ("m", "가장 좋았던 곳이 어디예요?", 262, "새 정보만 요청")], mute=[260, 261, 262])
add(a=264, kind="chat", bg="bg-teal", title="사자는", icon="ico_lion",
    msgs=[("m", "계획표 없으면 불안한 스타일일 것 같은데", 267, "관찰"),
          ("w", "맞아요. 진짜 싫어요.", 269)], mute=[267, 269])
add(a=271, kind="chat", bg="soft:br_couple_close", title="이제 내 이야기도",
    msgs=[("m", "저는 완전 반대예요.|계획 세워놓으면 그걸 지켜야 할 것 같아서|더 스트레스 받더라고요.", 272,
           "내 이야기")], mute=[272, 273, 274])
add(a=275, kind="morph", bg="bg-canvas", title="이제 더 이상", x="여행지 묻기", y="서로의 성향",
    at_y=277)
add(a=278, kind="depth", bg="bg-ink", title="작은 스몰토크에서",
    levels=[("여행 이야기", 278), ("그 사람의 방식", 280), ("살아가는 모습", 281)],
    top="표면", bottom="사람")
add(a=282, kind="typo", bg="bg-spot", kicker=("대화를 깊게 만드는 건", 282),
    rows=[("새 주제를 계속", 283, "md dim"), ("같은 주제 안에서 사람을 본다", 285, "lg cy")],
    strike=(0, (283, 1.2)))
add(a=286, kind="cards", bg="bg-canvas", title="여행에서도", vs=True,
    cards=[dict(n="어디를 갔는지", head="정보", at=287, photo="br_travel_free", tone="muted"),
           dict(n="어떤 사람인지", head="계획형? 즉흥형?", at=289, photo="br_planner", tone="hot")])
add(a=291, kind="sliders", bg="bg-grid", title="음식 이야기에서도",
    rows=[("뭘 좋아하는지", "어떤 사람인지", 0.85, 292), ("익숙한 맛", "새로운 시도", 0.72, 293)])
add(a=296, kind="typo", bg="bg-ink", rows=[("“대화 주제가 떨어졌다”", 297, "lg")],
    strike=(0, 299), kicker=("그래서", 296), mute=[297])
add(a=300, kind="icon", bg="bg-teal", key="ico_iceberg", title="표면의 정보만 주고받았을 뿐",
    orbit=True, size=420)

# ── 6  not an analysis ─────────────────────────────────────────────────────
add(a=302, kind="chapter", bg="bg-spot", num="6", word="분석이 아니다")
add(a=304, kind="typo", bg="bg-canvas", rows=[("상대를 분석하기", 305, "xl")], strike=(0, (305, 0.8)),
    kicker=("주의할 점", 304))
add(a=306, kind="chat", bg="bg-ember", title="이러기 시작하면",
    msgs=[("m", "물을 왼손으로 드시네요. 왼손잡이세요?", 306), ("m", "검은색 옷 입으셨네요. 검은색 좋아하세요?", 307),
          ("m", "말할 때 머리 만지시네요. 긴장했어요?", 308)], mute=[306, 307, 308])
add(a=309, kind="stamp", bg="photo:br_interview", title="스몰토크가 더 기괴해진다", at_title=311,
    stamp="관찰 면접", at_stamp=310)
add(a=312, kind="morph", bg="bg-ink", title="관찰의 목적", x="정확한 분석", y="가벼운 내 느낌", op="→",
    at_y=315)
add(a=316, kind="typo", bg="bg-spot", rows=[("맞아도 되고", 316, "lg cy"), ("틀려도 된다", 317, "lg am")], mute=[316, 317])
add(a=318, kind="chat", bg="bg-canvas", title="예를 들어",
    msgs=[("m", "오늘 되게 계획적으로|작정하고 오신 것 같은데요?", 319), ("w", "저 완전 즉흥적인데요?", 322)],
    mute=[319, 322])
add(a=324, kind="typo", bg="bg-ember", rows=[("틀렸다", 324, "xl am"), ("그런데 아무 문제 없다", 325, "lg")], mute=[325])
add(a=326, kind="chat", bg="bg-dust", title="오히려",
    msgs=[("m", "진짜요? 완전 반대로 봤네요.", 327, "새 이야기의 시작")], mute=[327])
add(a=330, kind="typo", bg="bg-teal", kicker=("스몰토크는", 330),
    rows=[("정답을 맞추는 시험", 331, "lg")], strike=(0, (331, 1.0)))

# ── 7  looking at yourself instead ─────────────────────────────────────────
add(a=332, kind="chapter", bg="bg-spot", num="7", word="잘 보이려는 마음")
add(a=334, kind="lines", bg="bg-grid", title="좋아하는 사람 앞에서", xlab="압박", ylab="정도",
    series=[("잘해야 한다는 압박", "M0 430 C240 410 460 300 640 180 S880 70 1000 40", "amber", 334, 990, -2),
            ("상대를 보는 정도", "M0 50 C240 70 460 180 640 300 S880 410 1000 430", "cyan", 335, 30, 20)])
add(a=336, kind="person", bg="bg-dust", key="cut_man_anx", side="right", think=True,
    head=("머릿속은 나로 꽉 차 있다", 337),
    bubbles=[("내가 재미있어 보이려나?", 338), ("내가 말을 이상하게 했나?", 339), ("상대가 나한테 호감이 있을까?", 340)],
    mute=[338, 339, 340])
add(a=341, kind="icon", bg="bg-ember", key="ico_mirror", title="상대의 눈에 비친 나", at_title=345,
    sub="계속 검열하는 중", at_sub=346, size=360, side=True)
add(a=347, kind="photo", bg="photo:br_man_nervous", chip="정작 눈앞의 사람은 못 본다", at_chip=348, pos="high")
add(a=350, kind="morph", bg="bg-canvas", title="먼저 바뀌어야 하는 것", x="대화 기술", y="태도", op="보다",
    at_y=352)

# ── 8  what to do next time ────────────────────────────────────────────────
add(a=353, kind="typo", bg="bg-ink", kicker=("다음에 스몰토크가 끊겼다면", 354),
    rows=[("새 질문부터 찾지 말 것", 356, "lg am")])
add(a=357, kind="radial", bg="bg-teal", key="ico_eye", title="눈앞에 있는 것들",
    items=[("방금 한 말", 357), ("표정", 358), ("행동", 359), ("들고 있는 물건", 360), ("둘이 있는 장소", 361)],
    mute=[358, 359])
add(a=363, kind="meter", bg="bg-canvas", title="대화할 거리", start=0.1, end=0.9, at=364,
    left="없다", right="이미 많다", tone="cyan")
add(a=365, kind="flow", bg="bg-ink", title=None,
    items=[("하나를 보고", 365, "a"), ("질문하기 전에", 366, "dim"), ("느낀 걸 가볍게", 367, "cy")])
add(a=369, kind="morph", bg="bg-spot", title="그 순간부터 스몰토크는", x="질문 이어가기", y="같이 만드는 대화",
    at_y=372)
add(a=373, kind="icon", bg="bg-dust", key="ico_formula", title="이것마저 공식으로", at_title=374,
    sub="외우지 않는다", at_sub=375, size=430, side=True)
add(a=376, kind="typo", bg="bg-canvas", rows=[("“질문하면 안 된다”", 376, "lg"), ("궁금하면 물어보면 된다", 378, "lg cy")],
    strike=(0, 377), mute=[376])
add(a=380, kind="cards", bg="bg-ink", title="중요한 건, 왜 질문하는지", vs=True,
    cards=[dict(n="정말", head="상대가 궁금해서", at=382, tone="hot"),
           dict(n="아니면", head="침묵이 불편해서", at=384, tone="muted")])

# ── 9  final takeaway + CTA ────────────────────────────────────────────────
add(a=387, kind="typo", bg="bg-spot", kicker=("결국 스몰토크가 어려운 이유는", 388),
    rows=[("재미있는 말을 몰라서", 390, "lg")], strike=(0, (390, 1.0)))
add(a=391, kind="scale", bg="bg-teal", title="더 신경 쓰는 쪽", left="내가 어떻게 보일지", right="상대",
    tilt_at=392)
add(a=394, kind="typo", bg="photo:br_window_talk", kicker=("스몰토크가 편해지려면", 394),
    rows=[("재미있는 사람이 되기보다", 395, "md dim"), ("눈앞의 사람에게 관심을", 396, "xl cy")])
add(a=398, kind="person", bg="bg-ember", key="cut_man_tense", side="right", think=True,
    bubbles=[("매번 애매하게 끝난다면", 399), ("대화 기술보다, 내 태도부터", 401)])
add(a=403, kind="cta", bg="photo:br_lecture", head="비공개 특강", sub="이 내용을 더 자세히 정리했습니다",
    at_sub=404, foot="설명란에서 확인하세요", at_foot=407)
add(a=408, kind="typo", bg="bg-spot", rows=[("잘 보이려는 태도에서", 409, "md dim"),
                                          ("눈앞의 사람을 보는 태도로", 410, "xl cy")])

SCENES = S
