# -*- coding: utf-8 -*-
"""하이에나의 태도 vs 사자의 태도 — scene plan for emit_v2.py.

SCENES = [(first_line, last_line, kind, opts)]; the ranges tile lines.json.
Asset keys resolve through library.json (downloaded by fetch_assets.py).
Format is chosen by what the line means: a feeling → photo/clip, logic →
graph/diagram, an abstract idea → pictogram/3D object, a real exchange → chat,
the claim itself → typography. No photo/clip carries more than two scenes.
"""
import json
import os

ASSETS = json.load(open(os.path.join(os.path.dirname(__file__), "library.json")))
PLAN = None          # build.py imports this name; the v2 plan lives in SCENES
END_HOLD = 2.6

SCENES = [
    # ── HOOK ────────────────────────────────────────────────────────────────
    (0, 1, "media", dict(clip="vid_hyena", tint="center", kicker="좋아하는 여자 앞에서만",
                         title="기준이 무너지는 남자", amber=None)),
    (2, 3, "cut", dict(figs=["cut_think"], thoughts=[(3, "이 사람은 어떤 남자를 좋아하지?", "r")])),
    (4, 7, "chips", dict(head="여자가 좋아하는 남자?", items=[
        (4, "깔끔한 남자", "neat"), (5, "재미있는 남자", "fun"),
        (6, "다정한 남자", "kind"), (7, "자기관리", "fit")], nocap=[4, 5, 6])),
    (8, 8, "search", dict(query="여자가 좋아하는 남자 스타일",
                          results=["호감 가는 남자 특징 7가지", "소개팅에서 먹히는 말투", "여자 심리 총정리"])),
    (9, 14, "media", dict(photo="ph_study", tint="right", focus="30% 50%", tags_side="right", tags=[
        (10, "여자들이 좋아하는 옷", "cyan"), (11, "헤어스타일", "cyan"),
        (12, "소개팅 대화법", "cyan"), (13, "카톡 보내는 법", "cyan"),
        (14, "공부 완료", "solid")])),
    (15, 18, "graph", dict(head="그런데 이상하죠", ylab="수준", xlab="공부한 시간",
                           levels=["낮음", "보통", "높음"], series=[
        dict(name="아는 것", tone="cyan", at=16, pts=[(0, .08), (.3, .3), (.6, .62), (.92, .92)]),
        dict(name="그녀 앞의 나", tone="amber", at=17, pts=[(0, .2), (.3, .22), (.6, .19), (.92, .21)])],
        marks=[dict(at=18, pt=(.6, .19), text="또 똑같다")])),
    (19, 20, "media", dict(clip="vid_phone", tint="left", tags_side="left", tags=[
        (19, "말이 많아지고", "amber"), (20, "답장 하나에 신경", "amber")])),
    (21, 21, "media", dict(photo="ph_date", tint="center", kicker="데이트 장소 하나에도",
                           title="상대 눈치")),
    (22, 25, "media", dict(photo="ph_bed", tint="left", focus="60% 50%",
                           thoughts=[(23, "내 외모가 부족한가?", "l"),
                                     (24, "여자는 원래 나쁜 남자를 좋아하나?", "l")])),
    (26, 28, "rows", dict(icon="ico_magnifier", head="문제를 다르게 보면", rows=[
        (27, "외모가 중요하지 않다", "x", ""), (28, "대화 기술이 필요 없다", "x", "")],
        nocap=[])),
    (29, 30, "type", dict(parts=[(29, "진짜 문제는", "kick"), (30, "그녀 앞에서", "mid"),
                                 (30, "내 태도가 어떻게 바뀌느냐", "amber")], impact=30)),
    (31, 32, "cut", dict(figs=["cut_calm", ("cut_woman", 32)], kicker="평소엔 괜찮던 남자")),
    (33, 35, "rows", dict(icon="ico_compass", head="그녀 앞에만 가면", rows=[
        (33, "자기 기준이 사라지고", "arrow"), (34, "상대 반응에 흔들리고", "arrow"),
        (35, "관계를 혼자 끌고 간다", "arrow")])),
    (36, 36, "media", dict(photo="ill_split", tint="", kicker="두 가지 태도",
                           title="하이에나 vs 사자")),
    (37, 39, "media", dict(clip="vid_hyena", tint="left", focus="60% 50%", tags_side="left", tags=[
        (37, "반응을 쫓고", "amber"), (38, "인정받으려 하고", "amber"), (39, "거절이 두렵다", "red")])),
    (40, 40, "level", dict(head="내 기준을 하나씩 포기한다", drops=None)),
    (41, 41, "media", dict(photo="ph_hyena", tint="left", focus="62% 50%", side="left",
                           kicker="이런 태도를", title="하이에나의 태도")),
    (42, 44, "media", dict(clip="vid_lion", tint="left", focus="62% 50%", tags_side="left", tags=[
        (43, "상대를 좋아해도", "cyan"), (44, "내 중심은 유지", "cyan")])),
    (45, 47, "diagram", dict(fig="boundary", head="표현은 하되", bound_at=46)),
    (48, 48, "media", dict(photo="ph_lion", tint="left", focus="64% 50%", side="left",
                           kicker="이런 태도를", title="사자의 태도")),
    (49, 49, "icon", dict(icon="ico_hourglass", labels=[(49, "차이는 사소한 순간에", "big")])),
    # ── 01 내 기준 ──────────────────────────────────────────────────────────
    (50, 51, "chapter", dict(num="1", word="내 기준이 있는가", sub="첫 번째 차이")),
    (52, 53, "media", dict(photo="ph_food", tint="", tags_side="bottom", tags=[
        (52, "소개팅", "cyan"), (53, "사실은 고기가 먹고 싶다", "solid")])),
    (54, 59, "chat", dict(msgs=[(55, "m", "뭐 드시고 싶으세요?"), (57, "w", "저는 아무거나 괜찮아요."),
                                (59, "m", "진짜 먹고 싶은 거 없어요?")])),
    (60, 60, "type", dict(picto="q", parts=[(60, "왜 이럴까요?", "big")], nocap=[60])),
    (61, 63, "iceberg", dict(icon="pic_iceberg", top=(61, "겉: 배려"), bot=(63, "속: 선택이 두렵다"))),
    (64, 65, "cut", dict(figs=["cut_anx"], thoughts=[(64, "내가 고른 곳이 별로면?", "l"),
                                                     (65, "괜히 마이너스되면?", "r")])),
    (66, 66, "diagram", dict(fig="handoff", head="선택권을 전부 넘긴다")),
    (67, 70, "rows", dict(icon="ico_scale", head="한 번으로 끝나지 않는다", rows=[
        (68, "장소도", "arrow", "상대에게"), (69, "시간도", "arrow", "상대에게"),
        (70, "대화도", "arrow", "상대 반응에")])),
    (71, 72, "quiz", dict(q="상대가 원하는 정답은?", opts=["고기", "파스타", "아무거나", "당신이 원하는 곳"])),
    (73, 74, "diagram", dict(fig="venn", head="사자는 나도 관계 안에 놓는다", join_at=74)),
    (75, 75, "chat", dict(msgs=[(75, "m", "저는 고기 먹고 싶은데 그쪽은 어때요?")])),
    (76, 78, "media", dict(photo="ph_ots", tint="left", focus="60% 50%", tags_side="left", tags=[
        (77, "상대를 존중하지만", "cyan"), (78, "나까지 지우지 않는다", "solid")])),
    # ── 02 흔들림 ───────────────────────────────────────────────────────────
    (79, 80, "chapter", dict(num="2", word="반응에 흔들리는가", sub="두 번째 차이")),
    (81, 81, "media", dict(clip="vid_silence", tint="", tags_side="bottom",
                           tags=[(81, "대화가 잠깐 끊겼다", "amber")])),
    (82, 83, "media", dict(photo="ph_friends", tint="right", focus="40% 50%", tags_side="right", tags=[
        (82, "친한 친구 앞이라면", "cyan"), (83, "그냥 물 마시면 끝", "cyan")])),
    (84, 85, "timer", dict(icon="ico_stopwatch", label="2초가 길다", label_at=85)),
    (86, 88, "cut", dict(figs=["cut_anx2"], thoughts=[(87, "분위기 망했나?", "l"),
                                                      (88, "내가 재미없나?", "r")])),
    (89, 93, "chat", dict(msgs=[(90, "m", "취미가 뭐예요?"), (91, "m", "여행 좋아하세요?"),
                                (93, "m", "주말엔 보통 뭐 하세요?")],
                          note=(92, "하나가 끝나면, 또 하나"))),
    (94, 98, "type", dict(parts=[(94, "문제는 질문이 아니라", "mid"), (95, "질문하는 이유", "big"),
                                 (96, "궁금해서", "strike"), (97, "침묵이 불안해서", "amber")],
                          strike_at=97, impact=97)),
    (99, 103, "phone", dict(name="그녀", msg="오늘 즐거웠어요 :)", clock=["21:12", "22:05", "23:40"],
                            clock_at=[(100, "22:05"), (102, "23:40")],
                            thoughts=[(101, "왜 답장이 없지?"), (102, "내가 뭔가 잘못했나?")])),
    (104, 105, "graph", dict(ylab="내 감정", xlab="상대의 반응", levels=["불안", "보통", "안정"],
                             series=[dict(name="내 감정", tone="red", at=104, dur=1.6,
                                          pts=[(0, .55), (.12, .85), (.24, .2), (.38, .78), (.52, .12),
                                               (.66, .7), (.8, .08), (.92, .5)])],
                             marks=[dict(at=105, pt=(.38, .78), dy=-44, text="전체가 흔들린다")])),
    (106, 106, "media", dict(photo="ph_hyena", tint="right", focus="40% 50%", side="right",
                             title="이게 하이에나")),
    (107, 110, "diagram", dict(fig="steps", head="상대가 멀어질수록", at=[107, 108, 109, 110])),
    (111, 112, "diagram", dict(fig="center", head="사자도 반응은 본다", wave_at=111, label_at=112)),
    (113, 115, "icon", dict(icon="ico_compass", labels=[(113, "반응은 보지만", "big"),
                                                        (115, "중심까지 내주지 않는다", "cyan")])),
    (116, 118, "graph", dict(ylab="수준", xlab="오늘", levels=["낮음", "보통", "높음"], series=[
        dict(name="상대의 반응", tone="dim", at=116, pts=[(0, .7), (.3, .66), (.55, .22), (.92, .3)]),
        dict(name="내 가치", tone="cyan", at=117, pts=[(0, .82), (.92, .82)])],
        marks=[dict(at=118, pt=(.55, .82), text="그대로")])),
    # ── 03 혼자 끌고 가기 ───────────────────────────────────────────────────
    (119, 120, "chapter", dict(num="3", word="혼자 끌고 가는가", sub="세 번째 차이")),
    (121, 121, "media", dict(photo="ph_alonecafe", tint="right", focus="35% 50%", side="right",
                             kicker="정말 많은 남자들의", title="공통점")),
    (122, 127, "bars", dict(head="누가 관계를 만들고 있나", me="내가", you="상대가", you_v=.12,
                            steps=[(123, .3), (124, .5), (125, .7), (127, .95)])),
    (128, 130, "media", dict(photo="ph_bed", tint="right", focus="40% 50%",
                             quote=(130, "저는 진짜 많이 노력했는데요."))),
    (131, 134, "type", dict(parts=[(131, "맞습니다", "kick"), (132, "많이 노력했습니다", "big"),
                                   (134, "혼자서만", "amber")], nocap=[131, 132, 134], impact=134)),
    (135, 138, "diagram", dict(fig="recip", head="관계는 한 사람이 만들지 않는다", head_at=135, rows=[
        (136, "내가 질문하면", "상대도 궁금해하고"), (137, "내가 시간을 쓰면", "상대도 시간을"),
        (138, "내가 마음을 열면", "상대도 들어온다")])),
    (139, 141, "diagram", dict(fig="fill", head="하이에나는", fill_at=141)),
    (142, 144, "rows", dict(icon="ico_phone", rows=[
        (142, "연락이 없으면", "arrow", "다시 연락"), (143, "약속이 안 잡히면", "arrow", "다시 제안"),
        (144, "반응이 약하면", "arrow", "더 잘해준다")])),
    (145, 149, "cut", dict(figs=["cut_calm2"], kicker="사자의 태도는 다르다", tags_side="right", tags=[
        (146, "내 표현은 한다", "cyan"), (147, "먼저 연락", "cyan"), (148, "애프터 제안", "cyan"),
        (149, "호감 표현", "cyan")])),
    (150, 150, "media", dict(photo="ill_chairs", tint="", tags_side="bottom",
                             tags=[(150, "상대가 들어올 공간", "amber")])),
    (151, 152, "diagram", dict(fig="space", head="할 만큼 하고", glow_at=152)),
    (153, 158, "compare", dict(photo="ill_split", tint="",
                               l=(155, "하이에나", "선택받으려 나를 바꾼다"),
                               r=(157, "사자", "좋아해도 나를 잃지 않는다"))),
    (159, 161, "type", dict(parts=[(159, "연애의 갑과 을", "kick"), (160, "누가 더 많이 좋아하느냐", "strike"),
                                   (161, "누가 먼저 기준을 포기하느냐", "amber")],
                            strike_at=161, nocap=[161], impact=161)),
    (162, 164, "chat", dict(msgs=[(163, "n", "그럼 이제부터 갑이 되어야겠네")],
                            note=(164, "또 이상해집니다"))),
    (165, 167, "media", dict(photo="ph_mask", tint="left", focus="62% 50%", tags_side="left", tags=[
        (165, "일부러 늦은 답장", "red"), (166, "관심 없는 척", "red"), (167, "먼저 올 때까지 버티기", "red")])),
    (168, 169, "icon", dict(icon="ico_rope", labels=[(168, "그건 사자가 아니다", "big"),
                                                     (169, "여전히 반응에 묶여 있다", "amber")])),
    (170, 171, "media", dict(clip="vid_phone", tint="right", focus="40% 50%", tags_side="right", tags=[
        (170, "일부러 2시간 늦게", "amber"), (171, "2시간 내내 핸드폰만", "red")])),
    (172, 173, "type", dict(parts=[(172, "여유", "strike"), (173, "불안을 연기하는 것", "amber")],
                            strike_at=172, nocap=[173])),
    (174, 177, "rows", dict(icon="ico_heart", head="사자는", rows=[
        (175, "관심이 있으면 표현하고", "check"), (176, "좋으면 좋다고 말하고", "check"),
        (177, "만나고 싶으면 먼저 제안한다", "check")])),
    (178, 179, "media", dict(photo="ph_decline", tint="left", focus="62% 50%", side="left",
                             kicker="거절당해도", title="나를 부정하지 않는다", title_at=179)),
    (180, 180, "type", dict(parts=[(180, "이 차이가", "mid"), (180, "연애에서 정말 중요합니다", "big")],
                            nocap=[180])),
    (181, 184, "rows", dict(icon="pic_flash", head="많은 남자들이 바꾸려는 것", rows=[
        (182, "카톡 잘 하는 법", "tick"), (183, "대화법", "tick"), (184, "행동", "tick")])),
    (185, 185, "iceberg", dict(icon="pic_iceberg", top=(185, "멘트 · 행동"), bot=(185, "그 아래의 태도"))),
    (186, 187, "media", dict(photo="ph_mask", tint="right", focus="45% 50%", tags_side="right", tags=[
        (186, "속은 여전히 불안", "red"), (187, "겉으로만 여유", "cyan")])),
    (188, 192, "chips", dict(items=[(188, "말투", "mouth"), (189, "표정", "face"), (190, "눈빛", "eye")],
                             after=(192, "결국 티가 납니다"), nocap=[188, 189, 190, 192])),
    (193, 194, "type", dict(parts=[(193, "바뀌어야 하는 건", "kick"), (194, "기술보다", "mid"),
                                   (194, "그 기술을 쓰는 사람의 태도", "big")], nocap=[194], impact=194)),
    (195, 198, "media", dict(photo="ph_backlit", tint="center", kicker="스스로에게 물어보세요",
                             title="그녀 앞에서 나는|어떤 태도로 변하는가?", title_at=197, amber=1,
                             nocap=[197, 198])),
    (199, 203, "check", dict(head="좋아할수록", items=[(200, "내 기준이 사라지는지"),
                                                       (201, "상대 반응에 흔들리는지"),
                                                       (202, "관계를 혼자 끌고 가는지")],
                             nocap=[200, 201, 202])),
    (204, 206, "media", dict(photo="ph_womanphone", tint="left", focus="62% 50%", side="left",
                             kicker="애프터에서 끊기고, 썸이 흐지부지라면", kicker_at=204,
                             title="멘트보다 먼저|태도", title_at=206, amber=1)),
    # ── ENDING ──────────────────────────────────────────────────────────────
    (207, 208, "cta", dict(title="여자 앞에서 드러나는 태도")),
    (209, 210, "takeaway", dict(clip="vid_lion", tint="center", title="태도를 바꾸면|연애가 쉬워진다")),
]
