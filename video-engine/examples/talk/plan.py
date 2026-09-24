# -*- coding: utf-8 -*-
"""Scene plan for "질문이 끝나면 대화도 끝납니다" — 668 narration lines.

Entries are (kind, arg) or (kind, arg, span). `span` is how many narration
lines the scene covers: this script is written in very short breath units, so
one scene per line would change the screen roughly every 1.4s. A scene holds a
whole thought instead, and the captions keep their own per-line timing under it.

kind codes
  B  photographic b-roll plate       arg = asset alias
  Y  b-roll plate + headline         arg = "alias|headline"
  C  cutout composite                arg = "cutout[+cutout]@bg"
  N  line-drawn diagram              arg = figure key
  I  3d icon (+ caption line)        arg = "iconkey|badge"
  P  pictogram + big line            arg = "mark|words"
  T  kinetic typography              arg = words ('' -> use the line)
  K  single quote bubble             arg = m | w | n
  Q  quote run, one bubble per       arg = "m|w|..." speakers in order
     quoted line in the span
  H  chapter header                  arg = "number|keyword"
  G  infographic                     arg = graphic id
"""

# ── assets generated for this film, alongside the shared library ────────────
_C = "https://d8j0ntlcm91z4.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/"
IMG_EXTRA = {
    "br_search_list_1":  _C + "hf_20260921_155855_2e8be452-43cc-4087-b821-4437ea514a53.png",
    "br_pilates_1":      _C + "hf_20260921_155855_2657d16d-903d-4a99-bd90-dc32ac6f7809.png",
    "br_japan_walk_1":   _C + "hf_20260921_155855_fbb29828-7deb-4ff9-ac4b-1c268ca5a6a5.png",
    "br_seongsu_1":      _C + "hf_20260921_155856_b597ace5-5c6e-4ad3-bba1-a70997ff6038.png",
    "br_home_netflix_1": _C + "hf_20260921_155915_ad0cb3df-bba6-4b4e-bb65-4bcd52dd60ca.png",
    "br_office_late_1":  _C + "hf_20260921_155915_eac5e02e-c796-4e6d-a1dd-2aae09797ad8.png",
    "br_interrogate_1":  _C + "hf_20260921_155915_603740e3-35c1-4f14-87fc-6d10a7f1bb3e.png",
    "br_two_laugh_1":    _C + "hf_20260921_155915_18bdde7e-bdfa-4828-92d9-b88b0001a2ff.png",
    "br_solo_train_1":   _C + "hf_20260921_155932_89a2e7cd-9744-433d-bbba-9a7cb1c9a671.png",
    "br_americano_1":    _C + "hf_20260921_155932_467d0a52-91c2-4674-9688-8a96fea1093d.png",
    "br_lean_listen_1":  _C + "hf_20260921_155932_8ed28837-7fac-486f-9ac4-bdec468e53b6.png",
    "br_review_note_1":  _C + "hf_20260921_155933_91c66c08-ee70-4bd3-90aa-34756b846f42.png",
    "il_multitask_1":    _C + "hf_20260921_155952_9c3a3e47-d933-420a-8fd7-7e8507f1eaae.png",
    "il_dig_layers_1":   _C + "hf_20260921_155952_02b85dc4-cf3b-4573-b362-4e92c321523c.png",
    "il_topic_map_1":    _C + "hf_20260921_155952_6be15c94-0b8b-4af3-b381-9c0aea95a3c3.png",
    # 3d icons — generated with background:transparent, so real alpha already
    "ico_cards_1":       _C + "hf_20260921_155952_da57a65a-53ce-4e2b-8f94-ddb673a8a0d6.png",
    "ico_engine_1":      _C + "hf_20260921_160017_569c197a-a044-41b7-9bee-c44337fa93da.png",
    "ico_layers4_1":     _C + "hf_20260921_160017_0c1ec026-c5f2-4f44-94e3-fa7c40167243.png",
    "ico_magnifier_1":   _C + "hf_20260921_160016_74ce87d0-21fe-40c9-88f2-ef62bfb2e38f.png",
    "ico_notebook_1":    _C + "hf_20260921_160017_31b90774-421d-4934-93e1-3d9d8c5f7f81.png",
    "ico_links_1":       _C + "hf_20260921_160035_9ac28a40-981e-4619-b1a8-f81c7215f38d.png",
    "ico_key_1":         _C + "hf_20260921_160035_6d97b53d-172e-468d-be4f-1fd5563edb0d.png",
    "ico_trash_1":       _C + "hf_20260921_160035_11b8d64f-0d58-492a-b66a-1f9c944cb351.png",
    "ico_stopwatch_1":   _C + "hf_20260921_160035_ffee77f9-987d-4e99-975d-2eaa07935416.png",
    # premium editorial pictograms for P cards (GPT Image 2.5, transparent)
    "pg_stall_1": _C + "hf_20260924_083527_62dcee31-173d-4ada-ba0a-e85891100fa1.png",
    "pg_fullbox_1": _C + "hf_20260924_083528_15323bcf-d9de-427c-904b-803b3290cb60.png",
    "pg_unfold_1": _C + "hf_20260924_083528_3cbd9d82-df94-463a-8e18-471dc4b47f17.png",
    "pg_inside_1": _C + "hf_20260924_083528_71b861e4-f483-490d-94c9-5a0cc26f3efb.png",
    "pg_discard_1": _C + "hf_20260924_083529_2602c187-4e33-4e83-ab3b-f97822d8a30b.png",
    "pg_busymind_1": _C + "hf_20260924_083528_00245346-71bb-43de-bcea-255d4873e500.png",
    "pg_lag_1": _C + "hf_20260924_083528_edd6facc-b1c9-4db3-afa2-ddb0c48b4054.png",
    "pg_emptycards_1": _C + "hf_20260924_083528_68a263d3-9ec3-47a9-a88c-5168a99b7285.png",
    "pg_sameway_1": _C + "hf_20260924_083528_e4a5d8d0-5029-4684-9776-e43b6c8b0c1b.png",
    "pg_okay_1": _C + "hf_20260924_083528_4b972ddb-dfcf-4bee-8c87-caa724c27593.png",
    "pg_myturn_1": _C + "hf_20260924_083528_eee3d659-f03c-4f95-a17a-45559b2ead84.png",
    "pg_seeeach_1": _C + "hf_20260924_083614_ad10dcef-16cf-420d-ac2b-2639a7decf97.png",
    "pg_mutual_1": _C + "hf_20260924_083613_7df2771f-6875-4ad9-b09d-31788e7fa635.png",
    "pg_infocard_1": _C + "hf_20260924_083613_0beddde2-401b-4b50-9187-76bb52e989f0.png",
    "pg_joinrow_1": _C + "hf_20260924_083614_818a865f-bd76-4272-8562-00ea5e2aa7ec.png",
    "pg_continue_1": _C + "hf_20260924_083613_6b932ead-3747-4f5f-984d-95844274f2e5.png",
    "pg_handed_1": _C + "hf_20260924_083614_bc12a173-3422-4029-8e87-54d3ce71b114.png",
    "pg_nextstep_1": _C + "hf_20260924_083633_6e5985c6-3066-4cbe-b933-bac29ddab2ed.png",
    "pg_tailq_1": _C + "hf_20260924_083633_d614de6f-17de-43d2-97a0-c1d1bf7d9f59.png",
    "pg_receive_1": _C + "hf_20260924_083633_b2b03056-a4b7-462e-9e75-199cb2ab8243.png",
    "pg_attention_1": _C + "hf_20260924_083633_36eea2b7-8fc2-4371-a947-e4f11dd861a2.png",
    "pg_iceberg_1": _C + "hf_20260924_083633_fb65890c-44ac-4809-ac0a-45947ce84f22.png",
    "pg_smoothpath_1": _C + "hf_20260924_083633_3892f453-148d-4ce8-9dbd-ed81b24b12d9.png",
    "pg_linkpoint_1": _C + "hf_20260924_084242_4de5f02f-3815-4844-985e-cd42069e282a.png",
    "pg_pause_1": _C + "hf_20260924_083651_709ed9b7-1848-47c4-bcd9-963451dad0f0.png",
    "pg_target_1": _C + "hf_20260924_083651_5ef7a5e0-15cf-49af-9d7d-289a56fed85e.png",
    "pg_fading_1": _C + "hf_20260924_083650_984869a5-f704-4cce-bdc8-071aa2c4e923.png",
    "pg_events_1": _C + "hf_20260924_083651_717b9521-b14a-4a9d-80b0-73a80195b3ac.png",
    "pg_difftopic_1": _C + "hf_20260924_083650_eb7997b1-4c77-49e9-b018-ff35315ad116.png",
    "pg_diffok_1": _C + "hf_20260924_083708_5a119f9c-5e5a-4e9c-9dd5-62edf520c346.png",
    "pg_erase_1": _C + "hf_20260924_083708_1417ca50-b2cb-46ef-8194-5752ce662c76.png",
    "pg_flatcalm_1": _C + "hf_20260924_083708_43168383-e9f5-454f-bf8a-6cd0c694bdd7.png",
    "pg_bridge_1": _C + "hf_20260924_083708_69099e5f-9a63-45a1-b6c1-2357a2eb2e85.png",
    "pg_fact_1": _C + "hf_20260924_083709_53a97a91-c4e7-49b8-b021-cb7d48c7da25.png",
    "pg_reason_1": _C + "hf_20260924_083708_a025194c-2e5c-405b-b10c-b18ccb0e89b1.png",
    "pg_criteria_1": _C + "hf_20260924_083727_2925c905-44e4-4d73-90ad-730fecd9d4d9.png",
    "pg_selfexpr_1": _C + "hf_20260924_083727_f377da9b-b257-4ee6-9476-dc9f6aa1bdb9.png",
    "pg_pressure_1": _C + "hf_20260924_083728_d7501374-bad4-4885-91b6-c013e0b9838d.png",
    "pg_letgo_1": _C + "hf_20260924_083728_170677f7-0ab4-49dc-968c-b903687f54fd.png",
    "pg_nocram_1": _C + "hf_20260924_083727_113f25f9-7953-4222-a204-a11a013b543b.png",
    "pg_transform_1": _C + "hf_20260924_083729_21c0f7ed-ceaa-46cf-92d5-db8cab9e7921.png",
    "pg_pattern_1": _C + "hf_20260924_083741_676c3cea-b9ea-4304-a9f4-141ec1bf630d.png",
    "pg_spring_1": _C + "hf_20260924_083741_adecb53a-a155-4957-bb98-adb20e0c8d5d.png",
    "pg_metronome_1": _C + "hf_20260924_083741_3bcc559a-d117-487e-a648-c58704d498d5.png",
}
ALIAS_EXTRA = {k[:-2]: [k] for k in IMG_EXTRA}

# All of the above are quality:high / resolution:2k. The first pass ran at the
# model's defaults (low, 1k) and was too soft to carry a 1080p frame.


# ── graphics for this film ──────────────────────────────────────────────────
# Declared as data, not lambdas: plan.py is imported *by* emit.py, so it must
# not reach back into it. emit.py maps the leading key onto its primitive.
GRAPHICS_EXTRA = {
 "g_branch_trip": ("branches", "하나의 소재가 여러 방향으로", "여행", ["왜 좋아해요?", "어떤 분위기?", "혼자 vs 같이", "계획형 vs 즉흥형"]),
 "g_ladder2": ("ladder", ["사실", "이유", "취향과 기준"], 1, 2, "대화의 깊이"),
 "g_ladder1": ("ladder", ["사실", "이유", "취향과 기준"], 0, 1, "대화의 깊이"),
 "g_facts_flat": ("facts", "사실만 오가면", ["일본 여행 좋아해요", "일본 어디가 제일 좋았어요?", "오사카요", "몇 번 가봤어요?", "……"]),
 "g_jump_trip": ("jump", "카페", "여행"),
 "g_asked_done":   ("rows", "이미 물어본 것", ["직업", "사는 곳", "취미", "여행"], (0, 1, 2, 3), None),
 "g_search_terms": ("chips", None, ["여자랑 할 대화 주제", "소개팅 질문 리스트"], (), (0, 1)),
 "g_topic_jump":   ("chain", ["러닝", "여행"]),
 "g_run_deeper":   ("rows", "이 한 문장 안에", ["왜 시작했는지", "뛸 때 어떤 기분인지", "혼자 뛰는 걸 좋아하는지"], (), None),
 "g_one_topic":    ("bars", "소재 하나로 갈 수 있는 거리",
                    [("정보만 물으면", .22, "calm"), ("생각과 감정까지", .94, "cool-hot")],
                    ("짧게 끝남", "오래 이어짐")),
 "g_four_given": ("chips", None, ["친구", "성수", "카페", "주말"], ()),
 "g_20_40":        ("bars", "질문을 준비하면", [("준비 없이", .33, "calm"), ("질문 스무 개", .66, "cool")],
                    ("20분", "40분")),
 "g_three_down":   ("rows", None, ["이유", "감정", "기준"], (), None),
 "g_fact_q":       ("chips", "사실 질문", ["어디", "언제", "몇 번", "얼마나"], ()),
 "g_four_steps": ("bars", "대화의 네 단계", [("정보", 0.25, "cool"), ("이유", 0.52, "cool"), ("기준", 0.76, "cool"), ("자기 표현", 0.98, "cool-hot")], ("얕음", "깊음"), (0, 1, 2, 3), (0, 4)),
 "g_info_exchange": ("twobranch", "대화를 무엇으로 쓰는가", "정보 교환", "사람을 알아가기"),
 "g_pilates_web":  ("chips", "필라테스 하나로", ["운동", "습관", "자기관리", "스트레스", "몸", "생활 패턴"], ()),
 "g_words_six":    ("chips", "이 한 문장 안에", ["주말", "집", "쉬는 것", "친구", "성수", "카페"], ()),
 "g_discover":     ("twobranch", "이야깃거리는", "새로 만들어낸다", "상대 말에서 발견한다"),
 "g_q_react_self": ("chain", ["질문", "반응", "자기표현"]),
 "g_interest_know": ("twobranch", "질문을 많이 하면", "관심은 보인다", "제대로 알아가기는 어렵다"),
 "g_bar_interest": ("bars", "계속 물으면",
                    [("관심 있어 보임", .88, "cool-hot"), ("서로에 대한 이해", .18, "cool")],
                    ("낮음", "높음")),
 "g_understand":   ("rows", "계속 물으면", ["관심 있어 보인다", "이해는 그대로다"], (1,), None),
 "g_move_trait":   ("chain", ["여행", "성향"]),
 "g_topic_chain":  ("vflow", ["여행", "계획", "성격", "일상", "연애"]),
 "g_drift":        ("rows", None, ["음식 얘기 → 연애 얘기", "직장 얘기 → 가치관 얘기"], (), None),
 "g_cards_end":    ("rows", None, ["여행 끝", "취미 끝", "직업 끝", "음식 끝"], (0, 1, 2, 3), None),
 "g_engine_swap":  ("twobranch", "대화의 엔진", "질문 리스트", "상대의 이야기"),
 "g_gap_link":     ("rows", None, ["대화 소재 문제", "공백의 태도"], (), None),
 "g_bar_ease":     ("bars", "여유 있어 보이는 쪽",
                    [("할 말이 많은 사람", .30, "calm"), ("공백이 괜찮은 사람", .98, "cool-hot")],
                    ("보통", "10배")),
 "g_three_find":   ("rows", "한 문장에서 찾을 것", ["사실", "감정", "기준"], (), None),
 "g_fact_row":     ("rows", "사실", ["회사 일이 많다"], (), None),
 "g_emotion_row":  ("rows", "감정", ["피곤하고 지쳐 있다"], (), None),
 "g_std_missing":  ("rows", "기준", ["아직 안 보인다"], (0,), "q"),
 "g_difference":   ("twobranch", "이제 둘이 달라졌다", "예측 가능성", "한꺼번에 몰리는 것"),
 "g_events":       ("chips", "보통 소재라고 생각하는 것", ["여행", "영화", "음식", "직업", "취미"], ()),
 "g_nonevents":    ("chips", "실제로는 이것도 소재", ["생각", "감정", "차이", "경험"], ("차이",)),
 "g_home_web":     ("chips", "집순이냐 아니냐를 넘어서",
                    ["혼자 있는 시간", "스트레스 푸는 방식", "사람 관계", "성향"], ()),
 "g_mirror_yes":   ("rows", None, ["좋아한다고 하면 나도 좋아한다", "싫다고 하면 나도 싫다"], (0, 1), None),
 "g_exchange_ok":  ("twobranch", "대화가 잘 통한다는 건", "모든 게 같은 상태", "다르게 주고받는 상태"),
 "g_center1":      ("rows", None, ["상대에게 관심은 있지만", "내 생각까지 지우지 않는 것"], (), None),
 "g_center2":      ("rows", None, ["상대 이야기를 듣지만", "전부 맞춰주지는 않는 것"], (), None),
 "g_center3":      ("rows", None, ["상대와 다를 때 불안해하지 않는 것"], (), None),
 "g_flow_five":    ("vflow", ["사실", "이유", "기준", "나", "다시 상대"]),
 "g_depth_step":   ("vflow", ["정보", "이유", "생각 · 기준"]),
 "g_depth_walk":   ("vflow", ["정보 얘기", "조금 이유를 묻고", "편하게 얘기하면", "생각이나 기준으로"]),
 "g_depth_up":     ("rows", None, ["반응이 짧으면", "다시 가벼운 이야기로"], (), None),
 "g_long_short":   ("bars", "상대의 반응도 정보다",
                    [("길게 이야기하는 소재", .86, "cool-hot"), ("짧게 끝나는 소재", .22, "cool")],
                    ("짧음", "김")),
 "g_depth_wave":   ("wave",),
 "g_practice3":    ("rows", "연습할 건 세 가지",
                    ["상대가 한 말에서 단어를 잡기", "그 단어에서 이유와 감정을 보기",
                     "내 생각을 하나 붙이기"], (), None),
 "g_review4":      ("rows", "소개팅이 끝난 뒤",
                    ["어떤 질문에서 길게 말했는지", "언제 갑자기 주제를 바꿨는지",
                     "내 이야기를 얼마나 했는지", "공백에서 얼마나 급했는지"], (), None),
 "g_result_only":  ("rows", "결과만 보면", ["애프터가 됐다", "안 됐다"], (0, 1), None),
 "g_data_stack":   ("bars", "무엇이 쌓이는가",
                    [("결과만 볼 때", .18, "calm"), ("장면을 볼 때", .92, "cool-hot")],
                    ("배움 없음", "경험이 됨")),
 "g_five_things":  ("rows", "이 다섯 가지",
                    ["상대가 말한 사실", "그 이유", "그때 느낀 감정",
                     "중요하게 보는 기준", "그에 대한 나의 생각"], (), None),
}


# ── the plan ────────────────────────────────────────────────────────────────
PLAN = [
    ("I", "ico_stopwatch|처음 20분은 쉽습니다", 3),                     # 0-2
    ("Q", "m|m|m", 3),                                          # 3-5
    ("B", "br_cafe_two", 1),                                    # 6
    ("P", "pg_stall|문제는 그 다음입니다", 1),                           # 7
    ("G", "g_asked_done", 4),                                   # 8-11
    ("C", "man_think@dark", 1),                                 # 12
    ("T", "", 1),                                               # 13
    ("B", "br_silence_table", 1),                               # 14
    ("N", "neon_fan", 1),                                       # 15
    ("Q", "m", 1),                                              # 16
    ("N", "neon_cutoff", 2),                                    # 17-18
    ("C", "man_anx@dark", 1),                                   # 19
    ("T", "", 1),                                               # 20
    ("B", "br_street", 3),                                      # 21-23
    ("B", "br_search_list", 1),                                 # 24
    ("G", "g_search_terms", 3),                                 # 25-27
    ("H", "01|소재의 착각", 2),                                      # 28-29
    ("P", "pg_fullbox|소재가 부족한 게 아닙니다", 2),                      # 30-31
    ("I", "ico_trash|너무 빨리 버립니다", 2),                           # 32-33
    ("Q", "w", 3),                                              # 34-36
    ("Q", "m|m", 3),                                            # 37-39
    ("N", "neon_queue", 2),                                     # 40-41
    ("G", "g_topic_jump", 1),                                   # 42
    ("Y", "br_running|이 한 문장 안에", 3),                           # 43-45
    ("P", "pg_unfold|할 얘기가 굉장히 많습니다", 1),                       # 46
    ("G", "g_run_deeper", 3),                                   # 47-49
    ("N", "neon_tree", 1),                                      # 50
    ("G", "g_one_topic", 1),                                    # 51
    ("P", "pg_inside|새 주제를 몰라서가 아닙니다", 2),                      # 52-53
    ("Y", "br_lean_listen|>방금 한 말 안에서|다음 이야기를 발견하지 못합니다", 2),   # 54-55
    ("T", "~이 차이가 큽니다", 1),                                     # 56
    ("B", "br_counsel", 2),                                     # 57-58
    ("N", "neon_cutoff", 2),                                    # 59-60
    ("Q", "w", 3),                                              # 61-63
    ("Q", "m", 3),                                              # 64-66
    ("Q", "w", 3),                                              # 67-69
    ("Q", "m", 2),                                              # 70-71
    ("G", "g_jump_trip", 1),                                    # 72
    ("T", "방금 상대가 준 것", 1),                                     # 73
    ("G", "g_four_given", 4),                                   # 74-77
    ("P", "pg_discard|네 가지를 다 버렸습니다", 2),                       # 78-79
    ("I", "ico_clock|10분 뒤", 1),                                # 80
    ("T", "", 1),                                               # 81
    ("T", "~>할 말이 없는 게 아닙니다|상대가 계속 할 말을 주고 있는데|그걸 놓치고 있는 겁니다", 3),  # 82-84
    ("H", "02|듣지 못하는 이유", 1),                                   # 85
    ("P", "pg_busymind|화술의 문제가 아닙니다", 2),                       # 86-87
    ("B", "br_cafe_two", 2),                                    # 88-89
    ("G", "g_three_lane", 2),                                   # 90-91
    ("C", "woman_a@dark", 1),                                   # 92
    ("Q", "m", 3),                                              # 93-95
    ("Q", "m", 3),                                              # 96-98
    ("Q", "m", 3),                                              # 99-101
    ("C", "man_blur@dark", 2),                                  # 102-103
    ("Y", "il_multitask|동시에 다섯 개", 3),                          # 104-106
    ("P", "pg_lag|당연히 버벅입니다", 1),                               # 107
    ("B", "br_counsel", 1),                                     # 108
    ("Q", "m", 3),                                              # 109-111
    ("G", "g_20_40", 2),                                        # 112-113
    ("P", "pg_emptycards|질문이 끝나면 다시 제자리", 2),                   # 114-115
    ("P", "pg_sameway|대화 방식은 그대로", 1),                          # 116
    ("H", "03|한 단계 내려가기", 2),                                   # 117-118
    ("I", "ico_layers4|사실에서 멈추지 않기", 2),                        # 119-120
    ("G", "g_three_down", 3),                                   # 121-123
    ("Y", "il_dig_layers|여기까지", 2),                             # 124-125
    ("Q", "w", 2),                                              # 126-127
    ("Q", "m", 2),                                              # 128-129
    ("G", "g_fact_q", 2),                                       # 130-131
    ("Q", "w", 3),                                              # 132-134
    ("Q", "m", 3),                                              # 135-137
    ("P", "pg_okay|이것도 괜찮습니다", 1),                              # 138
    ("G", "g_facts_flat", 2),                                   # 139-140
    ("G", "g_ladder1", 1),                                      # 141
    ("Q", "m", 1),                                              # 142
    ("T", "이유", 1),                                             # 143
    ("Q", "w", 3),                                              # 144-146
    ("G", "g_ladder2", 1),                                      # 147
    ("Q", "m|m", 2),                                            # 148-149
    ("T", "취향과 기준", 1),                                         # 150
    ("Q", "w|w|w", 5),                                          # 151-155
    ("Y", "br_japan_walk|이 사람의 여행 방식", 1),                      # 156
    ("P", "pg_myturn|여기가 중요합니다", 2),                            # 157-158
    ("Q", "m|m|m|m", 4),                                        # 159-162
    ("C", "woman_b@dark", 1),                                   # 163
    ("Q", "w", 2),                                              # 164-165
    ("Q", "m", 1),                                              # 166
    ("B", "br_two_laugh", 1),                                   # 167
    ("P", "pg_seeeach|서로 사람이 보였습니다", 2),                        # 168-169
    ("T", "네 단계", 1),                                           # 170
    ("G", "g_four_steps", 6),                                   # 171-176
    ("G", "g_branch_trip", 2),                                  # 177-178
    ("P", "pg_mutual|상대도 나를 알게 됩니다", 2),                        # 179-180
    ("T", "이게 중요합니다", 1),                                       # 181
    ("G", "g_info_exchange", 4),                                # 182-185
    ("B", "br_pilates", 1),                                     # 186
    ("Q", "w", 2),                                              # 187-188
    ("T", "정보 질문만 하면", 1),                                      # 189
    ("Q", "m|m|m", 4),                                          # 190-193
    ("P", "pg_infocard|물론 필요합니다", 1),                           # 194
    ("N", "neon_bridge", 1),                                    # 195
    ("Q", "m|m", 2),                                            # 196-197
    ("Q", "w|w", 4),                                            # 198-201
    ("Q", "m|m", 4),                                            # 202-205
    ("Q", "w", 3),                                              # 206-208
    ("Q", "m|m", 3),                                            # 209-211
    ("T", "감정", 1),                                             # 212
    ("Q", "m|m", 3),                                            # 213-215
    ("P", "pg_joinrow|여러분 이야기도 들어갑니다", 1),                      # 216
    ("T", "필라테스 하나로", 1),                                       # 217
    ("G", "g_pilates_web", 6),                                  # 218-223
    ("P", "pg_continue|계속 이어집니다", 1),                           # 224
    ("C", "man_anx@dark", 1),                                   # 225
    ("Q", "w", 2),                                              # 226-227
    ("Q", "m", 2),                                              # 228-229
    ("I", "ico_trash|또 버립니다", 1),                               # 230
    ("H", "04|단어 세 개", 3),                                      # 231-233
    ("I", "ico_magnifier|단어 세 개를 잡기", 2),                       # 234-235
    ("Q", "w|w", 4),                                            # 236-239
    ("T", "이미 여러 개가 있습니다", 1),                                  # 240
    ("G", "g_words_six", 6),                                    # 241-246
    ("T", "하나만 잡으면 됩니다", 1),                                    # 247
    ("Q", "m", 2),                                              # 248-249
    ("Y", "br_seongsu|성수를 자주 가는 이유", 2),                        # 250-251
    ("Q", "m", 2),                                              # 252-253
    ("P", "pg_handed|밖에서 가져올 필요가 없습니다", 2),                     # 254-255
    ("T", "이미 상대가 던져줬습니다", 1),                                  # 256
    ("B", "br_listen", 2),                                      # 257-258
    ("G", "g_discover", 2),                                     # 259-260
    ("B", "br_listen", 2),                                      # 261-262
    ("Q", "w", 3),                                              # 263-265
    ("P", "pg_nextstep|한 단계 더", 1),                             # 266
    ("Q", "m", 3),                                              # 267-269
    ("P", "pg_tailq|그것도 아닙니다", 2),                              # 270-271
    ("Y", "br_interrogate|취조", 1),                              # 272
    ("Q", "w", 2),                                              # 273-274
    ("Q", "m|m|m|m|m", 5),                                      # 275-279
    ("Y", "br_interrogate|인터뷰", 2),                             # 280-281
    ("G", "g_q_react_self", 2),                                 # 282-283
    ("C", "woman_a@dark", 1),                                   # 284
    ("P", "pg_receive|바로 다음 질문 대신", 2),                         # 285-286
    ("Q", "w", 3),                                              # 287-289
    ("Q", "m", 2),                                              # 290-291
    ("Q", "m|m", 4),                                            # 292-295
    ("Q", "m|m", 4),                                            # 296-299
    ("T", "이게 대화입니다", 1),                                       # 300
    ("G", "g_pingpong_rich", 5),                                # 301-305
    ("G", "g_pingpong_flat", 5),                                # 306-310
    ("H", "05|관심과 이해", 2),                                      # 311-312
    ("G", "g_interest_know", 2),                                # 313-314
    ("P", "pg_attention|관심 있어 보입니다", 2),                        # 315-316
    ("P", "pg_iceberg|깊게 알게 되는 건 아닙니다", 2),                     # 317-318
    ("Q", "m|w|m|w|m|w|m", 8),                                  # 319-326
    ("G", "g_bar_interest", 2),                                 # 327-328
    ("G", "g_understand", 2),                                   # 329-330
    ("N", "neon_lens", 1),                                      # 331
    ("Q", "m", 2),                                              # 332-333
    ("Q", "w|w", 3),                                            # 334-336
    ("Y", "br_solo_train|한 문장만으로도", 2),                         # 337-338
    ("Q", "m", 3),                                              # 339-341
    ("Q", "w", 3),                                              # 342-344
    ("G", "g_move_trait", 1),                                   # 345
    ("Q", "m", 2),                                              # 346-347
    ("T", "지금 둘의 상황으로", 2),                                     # 348-349
    ("Q", "w", 3),                                              # 350-352
    ("P", "pg_smoothpath|억지로 바꾼 게 아닙니다", 2),                    # 353-354
    ("Y", "il_topic_map|흘러간 겁니다", 2),                           # 355-356
    ("B", "br_counsel", 2),                                     # 357-358
    ("T", "바꾸는 게 아니라 이동", 2),                                   # 359-360
    ("G", "g_topic_chain", 6),                                  # 361-366
    ("B", "br_two_laugh", 1),                                   # 367
    ("G", "g_drift", 4),                                        # 368-371
    ("P", "pg_linkpoint|뜬금없지 않습니다", 2),                         # 372-373
    ("T", "반대로", 1),                                            # 374
    ("G", "g_cards_end", 4),                                    # 375-378
    ("I", "ico_cards|독립된 카드", 2),                               # 379-380
    ("T", "카드가 다 떨어지면", 2),                                     # 381-382
    ("T", "질문이 끝나면 대화도 끝납니다", 3),                               # 383-385
    ("I", "ico_engine|대화의 엔진", 3),                              # 386-388
    ("G", "g_engine_swap", 2),                                  # 389-390
    ("H", "06|2초의 공백", 1),                                      # 391
    ("B", "br_cafe_two", 2),                                    # 392-393
    ("G", "g_fill_gap", 2),                                     # 394-395
    ("C", "woman_b@dark", 1),                                   # 396
    ("I", "ico_clock|2초", 2),                                   # 397-398
    ("N", "neon_asktoss", 2),                                   # 399-400
    ("Q", "w", 3),                                              # 401-403
    ("Q", "m", 3),                                              # 404-406
    ("Q", "m", 2),                                              # 407-408
    ("G", "g_gap_ok", 1),                                       # 409
    ("Q", "w", 3),                                              # 410-412
    ("T", "자기 이야기를 더 하고 싶어 합니다", 2),                            # 413-414
    ("N", "neon_repeatstrip", 2),                               # 415-416
    ("B", "br_bench", 2),                                       # 417-418
    ("P", "pg_pause|질문을 덜 하는 게 아닙니다", 2),                       # 419-420
    ("P", "pg_target|더 정확한 순간에", 2),                            # 421-422
    ("G", "g_gap_link", 2),                                     # 423-424
    ("G", "g_bar_ease", 4),                                     # 425-428
    ("B", "br_review_note", 2),                                 # 429-430
    ("I", "ico_notebook|질문 목록을 내려놓기", 2),                       # 431-432
    ("Q", "m", 3),                                              # 433-435
    ("P", "pg_fading|눈앞의 사람을 놓칩니다", 1),                         # 436
    ("H", "07|사실 · 감정 · 기준", 2),                                # 437-438
    ("I", "ico_magnifier|한 문장에서 세 가지", 2),                      # 439-440
    ("G", "g_three_find", 3),                                   # 441-443
    ("Q", "w", 2),                                              # 444-445
    ("G", "g_fact_row", 2),                                     # 446-447
    ("G", "g_emotion_row", 2),                                  # 448-449
    ("G", "g_std_missing", 2),                                  # 450-451
    ("Q", "m|m", 2),                                            # 452-453
    ("Q", "w", 3),                                              # 454-456
    ("Q", "m|m", 3),                                            # 457-459
    ("T", "예측해봅니다", 1),                                         # 460
    ("Q", "w", 2),                                              # 461-462
    ("T", "기준", 1),                                             # 463
    ("Y", "br_office_late|예측 가능성", 2),                          # 464-465
    ("T", "여러분도 말할 수 있습니다", 1),                                 # 466
    ("Q", "m|m|m", 3),                                          # 467-469
    ("G", "g_difference", 2),                                   # 470-471
    ("Q", "m", 1),                                              # 472
    ("N", "neon_rally", 1),                                     # 473
    ("P", "pg_events|소재를 사건으로만 봅니다", 3),                        # 474-476
    ("G", "g_events", 5),                                       # 477-481
    ("T", "사건만 있는 게 아닙니다", 2),                                  # 482-483
    ("G", "g_nonevents", 4),                                    # 484-487
    ("T", "이 모든 게 소재입니다", 1),                                   # 488
    ("P", "pg_difftopic|다르다는 것도 소재입니다", 2),                     # 489-490
    ("Q", "w", 3),                                              # 491-493
    ("Q", "m", 3),                                              # 494-496
    ("Q", "m|m|m", 4),                                          # 497-500
    ("Q", "w|w", 4),                                            # 501-504
    ("Y", "br_home_netflix|혼자 있는 시간", 2),                       # 505-506
    ("Q", "m|m", 3),                                            # 507-509
    ("T", "집순이냐 아니냐를 넘어서", 1),                                  # 510
    ("G", "g_home_web", 4),                                     # 511-514
    ("T", "계속 이동합니다", 1),                                       # 515
    ("P", "pg_diffok|달라도 문제가 없습니다", 2),                         # 516-517
    ("T", "차이가 소재가 됩니다", 1),                                    # 518
    ("C", "man_anx@dark", 2),                                   # 519-520
    ("P", "pg_erase|차이를 없애버립니다", 1),                            # 521
    ("G", "g_mirror_yes", 4),                                   # 522-525
    ("P", "pg_flatcalm|갈등은 없습니다", 2),                           # 526-527
    ("Q", "m", 3),                                              # 528-530
    ("P", "pg_bridge|같은 상태가 아닙니다", 2),                          # 531-532
    ("G", "g_exchange_ok", 3),                                  # 533-535
    ("H", "08|중심의 태도", 2),                                      # 536-537
    ("G", "g_center1", 2),                                      # 538-539
    ("G", "g_center2", 2),                                      # 540-541
    ("G", "g_center3", 1),                                      # 542
    ("T", "대화도 깊어집니다", 1),                                      # 543
    ("I", "ico_layers4|질문은 세 종류", 3),                           # 544-546
    ("P", "pg_fact|첫 번째 · 사실 질문", 1),                           # 547
    ("Q", "m|m|m", 3),                                          # 548-550
    ("T", "시작할 때 필요합니다", 1),                                    # 551
    ("P", "pg_reason|두 번째 · 이유 질문", 1),                         # 552
    ("Q", "m|m|m", 3),                                          # 553-555
    ("T", "사람의 생각이 나옵니다", 1),                                   # 556
    ("P", "pg_criteria|세 번째 · 기준 질문", 1),                       # 557
    ("Q", "m|m|m|m", 4),                                        # 558-561
    ("T", "가치관이 나옵니다", 1),                                      # 562
    ("P", "pg_selfexpr|마지막은 자기표현", 2),                          # 563-564
    ("Q", "m|m|m", 3),                                          # 565-567
    ("T", "왔다 갔다 하면 됩니다", 1),                                   # 568
    ("G", "g_flow_five", 5),                                    # 569-573
    ("T", "기본 흐름입니다", 2),                                       # 574-575
    ("T", "다 깊게 할 필요는 없습니다", 3),                                # 576-578
    ("Q", "m", 2),                                              # 579-580
    ("P", "pg_pressure|부담스럽습니다", 1),                            # 581
    ("Y", "br_americano|갑자기 철학 시험", 2),                         # 582-583
    ("G", "g_depth_step", 2),                                   # 584-585
    ("G", "g_depth_walk", 4),                                   # 586-589
    ("G", "g_depth_up", 2),                                     # 590-591
    ("T", "상대의 편안함을 같이 봅니다", 2),                                # 592-593
    ("G", "g_long_short", 3),                                   # 594-596
    ("T", "길게 말하는 소재에 머물기", 2),                                 # 597-598
    ("P", "pg_letgo|짧게 끝나면 놓아주기", 2),                           # 599-600
    ("G", "g_depth_wave", 2),                                   # 601-602
    ("P", "pg_nocram|100개를 외울 필요가 없습니다", 2),                    # 603-604
    ("T", "연습할 건 세 가지", 1),                                     # 605
    ("G", "g_practice3", 3),                                    # 606-608
    ("P", "pg_transform|대화가 꽤 달라집니다", 2),                       # 609-610
    ("I", "ico_notebook|복기", 2),                                # 611-612
    ("G", "g_review4", 4),                                      # 613-616
    ("P", "pg_pattern|대화 패턴이 보입니다", 1),                         # 617
    ("Q", "m|m", 3),                                            # 618-620
    ("G", "g_result_only", 2),                                  # 621-622
    ("B", "br_mirror", 1),                                      # 623
    ("Q", "m|m|m", 3),                                          # 624-626
    ("G", "g_data_stack", 2),                                   # 627-628
    ("H", "09|오늘의 정리", 1),                                      # 629
    ("Q", "m", 3),                                              # 630-632
    ("T", "새로운 소재부터 찾지 마세요", 1),                                # 633
    ("N", "neon_askagain", 3),                                  # 634-636
    ("Y", "br_lean_listen|거기에 이미 있습니다", 2),                     # 637-638
    ("G", "g_five_things", 5),                                  # 639-643
    ("T", "이 다섯 가지면", 1),                                       # 644
    ("P", "pg_spring|쉽게 바닥나지 않습니다", 2),                         # 645-646
    ("T", "많이 준비한 사람이 아닙니다", 2),                                # 647-648
    ("T", "한마디에서 여러 이야기를 보는 사람", 2),                            # 649-650
    ("P", "pg_metronome|센스보다 연습입니다", 1),                        # 651
    ("Q", "m", 3),                                              # 652-654
    ("Y", "br_review_note|30분이 지나면", 2),                        # 655-656
    ("I", "ico_key|비공개 특강", 2),                                 # 657-658
    ("T", "대화 소재 100개가 아닙니다", 2),                               # 659-660
    ("T", "여유와 태도", 2),                                         # 661-662
    ("T", "마지막으로 이 문장만", 1),                                    # 663
    ("T", "질문이 부족한 게 아닙니다", 2),                                 # 664-665
    ("T", "대화의 구조를 아직 모르는 겁니다", 2),                             # 666-667
]


# ── exposure ────────────────────────────────────────────────────────────────
# Measured on the generated stills: the 90th-percentile luminance of each one.
# Several came back with a p90 in the 70s, and the plate already multiplies by
# 0.86 and lays a tint over it, so a face in those would have sunk to black —
# the one thing the brief is most explicit about. The gain here brings each
# still up to a p90 of about 145 before the plate touches it; the stills that
# already sit there are left alone.
EXPOSURE = {
    "br_search_list": 1.95,
    "br_japan_walk":  1.80,
    "br_home_netflix": 1.70,
    "br_office_late": 2.40,
    "br_interrogate": 1.55,
    "br_review_note": 1.60,
    "il_multitask":   1.30,
    "il_dig_layers":  1.30,
    "il_topic_map":   1.75,
}
