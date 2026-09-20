# -*- coding: utf-8 -*-
# Each scene: (key, bg_family, vis_dict, [cues])
# cue = narration string (one TTS clip). "sub" defaults to the cue text.
# vis kinds: hero icons list bubbles photo portrait compare bars scale venn path strike gauge stack split
S = []
def s(key, bg, vis, cues): S.append(dict(key=key, bg=bg, vis=vis, cues=cues))

s("s01","ember", dict(kind="hero", big="첫 1분", sup="소개팅", icon="stopwatch", ring=True),
  ["소개팅 첫 1분만에 여자에게 감점되는 남자들이 있습니다"])

s("s02","charcoal", dict(kind="strike", target="대화 실력", note="문제는 여기가 아닙니다"),
  ["대화를 못해서가 아닙니다"])

s("s03","blue", dict(kind="gauge", title="잘 보이고 싶은 마음", lo="약함", hi="강함", value=92,
                     caption="평소에는 하지 않던 행동이 나온다"),
  ["오히려 잘 보이고 싶은 마음이 너무 커져서 평소에는 하지 않던 행동들이 나오기 때문입니다"])

s("s04","charcoal", dict(kind="hero", big="예를 들어볼게요", small=True, icon="play"),
  ["예를 한번 들어볼게요"])

s("s05","photo_cafe", dict(kind="photo", img="cafe", center="소개팅 장소 도착"),
  ["소개팅 장소에 도착했습니다"])

s("s06","photo_cafe", dict(kind="portrait", img="woman_enter", label="상대가 들어온다"),
  ["상대가 들어와요"])

s("s07","ember", dict(kind="gauge", title="첫인상 호감도", lo="보통", hi="매우 높음", value=96,
                      caption="사진보다 훨씬"),
  ["사진보다 훨씬 마음에 듭니다"])

s("s08","violet", dict(kind="icons", title="머리가 갑자기 바빠진다",
                       items=[("brain","생각 과부하"),("spark","계산 시작"),("eye","반응 확인")]),
  ["그 순간부터 갑자기 머리가 바빠집니다"])

s("s09","violet", dict(kind="bubbles", tone="thought", title="머릿속",
                       items=["잘 보여야 되는데.","재밌게 해야 되는데.","첫인상 망치면 안 되는데."]),
  ["잘 보여야 되는데.","재밌게 해야 되는데.","첫인상 망치면 안 되는데."])

s("s10","teal", dict(kind="bubbles", tone="say", title="인사", ok=True, items=["안녕하세요."]),
  ["그리고 인사를 합니다","안녕하세요.","여기까지는 아무 문제 없어요"])

s("s11","charcoal", dict(kind="hero", big="여기서부터", sub2="조금씩 달라진다", icon="fork"),
  ["근데 그다음부터 조금씩 달라지기 시작합니다"])

s("s12","slate", dict(kind="bubbles", tone="say", title="첫 5분 동안 한 말", dense=True,
                      items=["오는 길 괜찮으셨어요?","여기 찾기 어렵진 않으셨어요?","뭐 드실래요?",
                             "저는 아무거나 괜찮아요.","편하신 걸로 드세요.","사진보다 훨씬 예쁘시네요."]),
  ["오는 길 괜찮으셨어요?","여기 찾기 어렵진 않으셨어요?","뭐 드실래요?",
   "저는 아무거나 괜찮아요.","편하신 걸로 드세요.","사진보다 훨씬 예쁘시네요."])

s("s13","teal", dict(kind="icons", title="말 자체는 문제가 없다",
                     items=[("check","이상한 말 없음"),("heart","친절함"),("hands","배려도 있음")]),
  ["각각의 말을 하나씩 보면 이상한 건 없습니다","오히려 친절해요","상대도 배려하고 있고요"])

s("s14","ember", dict(kind="compare", title="무엇이 전달되는가",
                      left=("무슨 말을 했느냐","말의 내용",38),
                      right=("그 말을 하는 사람의 상태","태도와 상태",94)),
  ["근데 중요한 건 무슨 말을 했느냐보다 그 말을 하고 있는 사람의 상태입니다"])

s("s15","blue", dict(kind="icons", title="계속 반응을 확인한다",
                     items=[("radar","반응 스캔"),("eye","표정 확인"),("loop","다시 확인")]),
  ["상대가 너무 마음에 드는 순간부터 남자가 계속 여자 반응을 확인하고 있는 거예요"])

s("s16","blue", dict(kind="list", title="머릿속 체크리스트", mark="q",
                     items=["내가 웃기면 웃는지","표정이 굳지는 않았는지","내가 마음에 드는 것 같은지"]),
  ["내가 웃기면 웃는지","표정이 굳지는 않았는지","내가 마음에 드는 것 같은지"])

s("s17","violet", dict(kind="path", title="답을 고르는 순서",
                       a="내 생각", b="상대가 좋아할 답", pick="b"),
  ["그래서 자기 생각보다 상대가 좋아할 만한 답을 먼저 찾습니다"])

s("s18","charcoal", dict(kind="hero", big="첫인상", sub2="보통은 외모부터 떠올린다", icon="mirror"),
  ["우리가 첫인상이라고 하면 보통 외모부터 생각합니다"])

s("s19","slate", dict(kind="icons", title="외모 항목", grid4=True,
                      items=[("shirt","옷"),("hair","머리"),("ruler","키"),("wave","목소리")]),
  ["옷을 잘 입었는지","머리가 괜찮은지","키가 어떤지","목소리가 어떤지"])

s("s20","slate", dict(kind="hero", big="물론 다 포함됩니다", small=True, icon="check"),
  ["물론 다 첫인상에 들어갑니다"])

s("s21","teal", dict(kind="hero", big="그것만 보고 있지는 않다", small=True, icon="eye"),
  ["근데 실제로 사람을 만나면 그것만 보고 있지는 않아요"])

s("s22","teal", dict(kind="list", title="같이 읽히는 것들", mark="dot",
                     items=["말을 얼마나 급하게 하는지","내가 말할 때 얼마나 기다려주는지","자기 의견이 있는지",
                            "어색해졌을 때 어떻게 반응하는지","실수했을 때 얼마나 크게 흔들리는지"]),
  ["이 사람이 말을 얼마나 급하게 하는지","내가 말할 때 얼마나 기다려주는지","자기 의견이 있는지",
   "조금 어색해졌을 때 어떻게 반응하는지","실수했을 때 얼마나 크게 흔들리는지"])

s("s23","teal", dict(kind="hero", big="이런 것도 같이 인식된다", small=True, icon="radar"),
  ["이런 것들도 같이 인식됩니다"])

s("s24","ember", dict(kind="strike", target="첫인상 = 외모", note="저는 그렇게 보지 않습니다"),
  ["그래서 저는 첫인상을 단순히 외모의 문제라고 생각하지 않습니다"])

s("s25","ember", dict(kind="quote", big="마음에 드는 사람을 만났을 때\n나는 어떤 사람이 되는가"),
  ["오히려 이런 질문에 더 가깝다고 봐요",
   "마음에 드는 사람을 만났을 때 나는 어떤 사람이 되는가"])

s("s26","charcoal", dict(kind="hero", big="한번 생각해보세요", small=True, icon="brain"),
  ["이걸 한번 생각해보세요"])
