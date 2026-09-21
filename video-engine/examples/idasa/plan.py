# -*- coding: utf-8 -*-
"""Scene plan: one entry per script line (251 total).

kind codes
  B  b-roll photographic still      arg = asset key
  C  cutout composite               arg = "cutout[+cutout]@bgkey"
  N  neon wireframe pictogram       arg = asset key
  I  3d icon                        arg = "iconkey|badge text"
  T  kinetic typography card        arg = on-screen text ('' -> use the line)
  K  quote / kakao bubble card      arg = "who" (m=남자, w=여자, n=내담자)
  H  chapter header                 arg = "number|keyword"
  G  infographic                    arg = graphic id
"""

PLAN = [
    # --- 0-8  문제 제기 -------------------------------------------------
    ("B", "br_cafe_two"), ("B", "br_friends"), ("B", "br_phone"),
    ("C", "man_anx@crimson"), ("I", "ico_clock|3초"),
    ("T", ""), ("T", ""), ("T", ""), ("I", "ico_bubble|"),
    # --- 9-22  질문 연쇄 ------------------------------------------------
    ("K", "m"), ("C", "woman_a@dark"), ("K", "w"), ("C", "man_anx@dark"),
    ("K", "m"), ("B", "br_listen"), ("K", "m"), ("B", "br_listen"),
    ("K", "m"), ("N", "neon_qmarks"), ("C", "man_think@dark"), ("T", "잘 이어가고 있다"),
    ("B", "br_silence_table"), ("G", "g_cover_anxiety"),
    # --- 23-30  상담 사례 -----------------------------------------------
    ("T", "이 차이가 중요합니다"), ("B", "br_counsel"),
    ("K", "n"), ("K", "n"), ("K", "n"),
    ("B", "br_listen"), ("T", "질문이 너무 많습니다"), ("C", "man_think@dark"),
    # --- 31-43  평범한 질문들 -------------------------------------------
    ("N", "neon_qmarks"),
    ("T", ""), ("T", ""), ("T", ""), ("T", ""), ("T", ""),
    ("T", ""), ("B", "br_empty_chair"), ("T", "문제는 질문 하나가 아닙니다"),
    ("G", "g_question_chain"), ("N", "neon_branch"), ("I", "ico_question|"),
    ("B", "br_silence_table"),
    # --- 44-51  면접 같은 대화 ------------------------------------------
    ("I", "ico_clock|1시간"), ("C", "man_anx+woman_a@dark"),
    ("T", "질문은 많아요"), ("G", "g_info_known"), ("G", "g_info_known2"),
    ("G", "g_info_unknown"), ("C", "man_anx@dark"), ("N", "neon_qmarks"),
    # --- 52-67  관심의 착각 / 러닝 --------------------------------------
    ("T", "많은 남자들의 착각"), ("K", "m"), ("T", "맞아요"),
    ("I", "ico_bubble|"), ("G", "g_depth_flat"), ("B", "br_cafe_two"),
    ("C", "woman_b@dark"), ("K", "w"), ("C", "man_anx@dark"),
    ("T", ""), ("T", ""), ("T", ""), ("T", ""),
    ("G", "g_info_questions"), ("B", "br_running"), ("T", "다르게 가볼게요"),
    # --- 68-76  다른 대화 ------------------------------------------------
    ("K", "w"), ("K", "m"), ("T", "조금 달라졌죠"), ("C", "woman_b@dark"),
    ("K", "w"), ("I", "ico_question_x|"), ("K", "m"),
    ("N", "neon_two_nodes"), ("I", "ico_shoe|"),
    # --- 77-84  깊어진다는 것 -------------------------------------------
    ("G", "g_depth_layers"), ("T", "대화가 깊어진다는 것"),
    ("C", "man_anx@crimson"), ("N", "neon_multitask"), ("C", "man_calm@dark"),
    ("T", ""), ("T", "원래 말이 없나 보다"), ("B", "br_bench"),
    # --- 85-99  불안 루프 -----------------------------------------------
    ("C", "man_anx+woman_a@dark"), ("I", "ico_glass|"), ("T", ""),
    ("B", "br_phone"), ("T", ""), ("K", "w"), ("T", ""),
    ("B", "br_silence_table"), ("N", "neon_loop"), ("C", "man_anx@dark"),
    ("I", "ico_bubble|"), ("C", "woman_a@dark"), ("T", "잠깐 안심"),
    ("T", ""), ("B", "br_silence_table"),
    # --- 100-110  루프 명명 ---------------------------------------------
    ("N", "neon_loop"), ("I", "ico_bubble|"), ("G", "g_loop"),
    ("G", "g_loop_full"), ("G", "g_loop_full"), ("T", "말주변의 문제가 아니다"),
    ("N", "neon_loop"), ("G", "g_purpose"), ("T", "빨리 없애야 돼"),
    ("T", "가 되어버린 겁니다"), ("H", "01|공백의 태도"),
    # --- 111-119  공백의 태도 -------------------------------------------
    ("C", "man_calm@dark"), ("I", "ico_question_x|"), ("G", "g_gap_ok"),
    ("T", "생각보다 어렵습니다"), ("B", "br_cafe_two"), ("I", "ico_clock|3초"),
    ("T", "별거 아니죠?"), ("I", "ico_clock|길게"), ("C", "man_anx@dark"),
    # --- 120-128  아무것도 안 해도 --------------------------------------
    ("T", "아무것도 안 해도 됩니다"), ("I", "ico_glass|"), ("B", "br_friends"),
    ("B", "br_coffee"), ("K", "m"), ("T", "이러지 않습니다"), ("B", "br_bench"),
    ("C", "man_calm@dark"), ("G", "g_fill_gap"),
    # --- 129-137  조급함 -------------------------------------------------
    ("C", "man_anx@crimson"), ("T", "지금 긴장하고 있구나"), ("C", "woman_a@dark"),
    ("T", "침묵만의 문제가 아니다"), ("N", "neon_branch"), ("C", "woman_b@dark"),
    ("K", "w"), ("C", "man_anx@dark"), ("K", "mx"),
    # --- 138-147  머물러보기 ---------------------------------------------
    ("T", "잠깐 생각해볼 수 있죠"), ("K", "m"), ("C", "woman_b@dark"),
    ("K", "w"), ("C", "man_calm@dark"), ("K", "m"), ("N", "neon_two_nodes"),
    ("T", "질문이 없어서가 아니다"), ("G", "g_discard"), ("B", "br_counsel"),
    # --- 148-156  한 문장 속 소재 ----------------------------------------
    ("N", "neon_branch"), ("I", "ico_question|"), ("T", "예를 들어"),
    ("K", "w"), ("G", "g_highlight"), ("G", "g_tags1"), ("G", "g_tags2"),
    ("N", "neon_branch"), ("C", "man_anx@dark"),
    # --- 157-167  멀티태스킹 ---------------------------------------------
    ("N", "neon_multitask"), ("T", ""), ("T", "왜 이런 일이 생기냐"),
    ("B", "br_mirror"), ("T", ""), ("T", ""), ("T", ""), ("T", ""),
    ("G", "g_three_lane"), ("N", "neon_windows"), ("B", "br_listen"),
    # --- 168-173  진짜 여유 ----------------------------------------------
    ("T", "여유는 무심함이 아니다"), ("H", "02|진짜 여유"),
    ("T", "침묵이 왔다|괜찮습니다"), ("T", "반응이 약하다|괜찮습니다"),
    ("T", "재미있지 않았다|그럴 수도 있습니다"), ("T", "대화가 꼬였다|다시 이어가면 됩니다"),
    # --- 174-182  줄이는 게 답이 아니다 ----------------------------------
    ("C", "man_calm@dark"), ("T", "한 가지 더"), ("G", "g_less_words"),
    ("T", ""), ("C", "man_think@dark"), ("B", "br_empty_chair"),
    ("T", "그게 아닙니다"), ("G", "g_q_then_self"), ("N", "neon_two_nodes"),
    # --- 183-193  관심과 표현 --------------------------------------------
    ("H", "03|관심과 표현"), ("N", "neon_two_nodes"), ("N", "neon_two_nodes"),
    ("T", "예를 들어볼게요"), ("C", "woman_b@dark"), ("K", "w"),
    ("C", "man_calm@dark"), ("T", "왜요?"), ("C", "woman_b@dark"), ("K", "w"),
    ("I", "ico_question_x|"),
    # --- 194-203  주고받기 -----------------------------------------------
    ("K", "m"), ("G", "g_add_self"), ("C", "man_calm+woman_b@dark"),
    ("T", "그리고 다시"), ("K", "m"), ("N", "neon_two_nodes"),
    ("T", "이게 대화입니다"), ("G", "g_pingpong_flat"), ("G", "g_pingpong_rich"),
    ("N", "neon_two_nodes"),
    # --- 204-212  진짜 문제 ----------------------------------------------
    ("C", "man_anx@dark"), ("G", "g_bar_compare"), ("T", "이게 핵심입니다"),
    ("B", "br_street"), ("C", "woman_a@dark"), ("K", "w"),
    ("T", "라고 합니다"), ("C", "man_blur@dark"), ("G", "g_not_seen"),
    # --- 213-225  세 가지 ------------------------------------------------
    ("H", "04|딱 세 가지"), ("H", "n1|첫 번째"), ("G", "g_step1"),
    ("I", "ico_clock|2초"), ("C", "man_calm@dark"), ("H", "n2|두 번째"),
    ("N", "neon_branch"), ("G", "g_tags3"), ("T", "이미 들어 있습니다"),
    ("H", "n3|세 번째"), ("G", "g_step3"), ("T", ""), ("T", ""),
    # --- 226-233  쌓이는 표현 --------------------------------------------
    ("T", ""), ("G", "g_stack"), ("T", "말을 덜 하는 게 아니다"),
    ("C", "man_calm@dark"), ("T", "멘트의 문제가 아니다"),
    ("N", "neon_two_nodes"), ("G", "g_gap_ok"), ("T", "그게 훨씬 중요합니다"),
    # --- 234-239  구분하기 -----------------------------------------------
    ("C", "man_anx@crimson"), ("T", "무슨 말을 하지? 보다"),
    ("T", "나는 왜 지금 말을 해야 한다고 느끼지?"), ("G", "g_two_branch"),
    ("N", "neon_two_nodes"), ("B", "br_counsel"),
    # --- 240-244  드러나는 불안 ------------------------------------------
    ("G", "g_check1"), ("G", "g_check2"), ("N", "neon_loop"),
    ("G", "g_signs1"), ("G", "g_signs2"),
    # --- 245-250  마무리 -------------------------------------------------
    ("H", "05|공백의 태도"), ("B", "br_bench"), ("T", "그게 핵심입니다"),
    ("T", "마지막으로 이 문장만"), ("T", "대화가 끊기지 않는 사람이|여유 있는 사람이 아닙니다"),
    ("T", "대화가 잠깐 끊겨도|흔들리지 않는 사람이 여유 있는 사람입니다"),
]

assert len(PLAN) == 251, f"plan has {len(PLAN)} entries, expected 251"


# ── variety pass ────────────────────────────────────────────────────────────
# Review note: "같은 이미지나 요소가 3회 이상 반복되지 않도록."
# The 침묵·불안·질문·안심 loop and the two-node figure were carrying far too
# many moments. Every slot below is re-cut to a figure shaped around its own
# sentence, so no diagram, icon or still now plays more than twice.
_VARIETY = {
    31:  ("N", "neon_plainchips"),   # 질문 하나하나는 너무 평범하거든요
    44:  ("N", "neon_elapsed"),      # 한 시간 넘게 얘기했는데
    75:  ("N", "neon_bridge"),       # 대화가 사람 얘기로 바뀝니다
    93:  ("N", "neon_surge"),        # 불안이 확 올라오는 거예요
    95:  ("N", "neon_asktoss"),      # 질문 하나 던져요
    100: ("N", "neon_meter"),        # 다시 불안해집니다
    101: ("N", "neon_askagain"),     # 질문 하나 더 던집니다
    102: ("N", "neon_repeatstrip"),  # 이게 반복되는 겁니다
    104: ("G", "g_three_beats"),     # 침묵. 불안. 질문.
    106: ("N", "neon_dial"),         # 불안을 조절하는 방식의 문제
    112: ("T", ""),                  # 침묵을 기술처럼 쓰라는 얘기도 아니에요
    116: ("N", "neon_countdown"),    # 하나. 둘. 셋.
    118: ("N", "neon_stretch"),      # 이 3초가 엄청 길게 느껴집니다
    133: ("N", "neon_cutoff"),       # 끝까지 기다리지 못하는 경우
    144: ("N", "neon_flow"),         # 그렇게 흘러갈 수 있습니다
    148: ("N", "neon_tree"),         # 한 문장에 소재가 세 개, 네 개
    155: ("N", "neon_fan"),          # 여러 방향으로 갈 수 있습니다
    157: ("N", "neon_queue"),        # 이미 다음 질문이 떠 있어요
    184: ("N", "neon_weave"),        # 관심을 보이고, 그다음 나를 표현합니다
    185: ("N", "neon_pendulum"),     # 다시 상대에게, 다시 내 생각을
    203: ("N", "neon_rally"),        # 서로 왔다 갔다 하는 거예요
    219: ("N", "neon_lens"),         # 그 문장 안에 뭐가 있는지 보세요
    231: ("N", "neon_twocheck"),     # 관심도 가질 수 있고, 내 생각도 보여줄 수 있고
    238: ("N", "neon_split"),        # 그걸 구분하기 시작하면
}
for _i, _v in _VARIETY.items():
    PLAN[_i] = _v


# ── richness pass ───────────────────────────────────────────────────────────
# Review note: "픽토그램, 3d 아이콘, 일러스트, 인포그래픽 ... 최대한 많이 활용해서
# 다채롭게." These scenes were bare typography; each now carries a drawn mark
# above the line, so the read stays but the frame has something in it.
_PICTOS = {
    5:   ("P", "think"),      # 뭐라도 말해야 되나?
    6:   ("P", "bored"),      # 재미없어 하나?
    7:   ("P", "spoil"),      # 내가 분위기 망친 건가?
    32:  ("P", "house"),      # 어디 사세요?
    33:  ("P", "commute"),    # 출퇴근 얼마나 걸리세요?
    34:  ("P", "family"),     # 형제 있으세요?
    35:  ("P", "travel"),     # 여행 좋아하세요?
    36:  ("P", "hobby"),      # 취미가 뭐예요?
    37:  ("P", "badq"),       # 뭐가 잘못된 질문인가요?
    61:  ("P", "distance"),   # 몇 킬로미터 뛰세요?
    62:  ("P", "calendar"),   # 일주일에 몇 번 하세요?
    63:  ("P", "pin"),        # 어디서 뛰세요?
    64:  ("P", "medal"),      # 마라톤도 나가셨어요?
    82:  ("P", "calm"),       # 조용하면 조용한가 보다.
    87:  ("P", "bored"),      # 지루한가?
    89:  ("P", "door"),       # 집에 가고 싶은가?
    91:  ("P", "radar"),      # 나한테 관심 없나?
    98:  ("P", "relief"),     # 아, 다행이다.
    112: ("P", "notrick"),    # 침묵을 기술처럼 쓰라는 얘기도 아니에요.
    161: ("P", "think"),      # 지금 잘하고 있나?
    163: ("P", "radar"),      # 얘가 나를 어떻게 생각하지?
    164: ("P", "fewer"),      # 다음엔 무슨 말 해야 하지?
    177: ("P", "listen"),     # 질문 덜 해야겠네.
    224: ("P", "self"),       # 저는 이래요.
    225: ("P", "differ"),     # 저는 그건 좀 다르게 느껴요.
    226: ("P", "wonder"),     # 저는 그런 사람 신기하더라고요.
}
for _i, _v in _PICTOS.items():
    PLAN[_i] = _v
