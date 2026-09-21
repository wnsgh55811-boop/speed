# -*- coding: utf-8 -*-
# (beat_from, beat_to_inclusive, background family, visual spec)
S2=[]
def sc(a,b,bg,v): S2.append(dict(a=a,b=b,bg=bg,vis=v))

sc(0,0,"ember",   dict(kind="hero3d", img="i3_stopwatch", big="첫 1분", sup="소개팅"))
sc(1,1,"charcoal",dict(kind="strike", target="대화 실력", note="문제는 여기가 아닙니다"))
sc(2,2,"blue",    dict(kind="gauge", title="잘 보이고 싶은 마음", lo="약함", hi="강함", value=92,
                       caption="평소에는 하지 않던 행동이 나온다"))
sc(3,3,"charcoal",dict(kind="hero3d", img="i3_plane", big="예를 들어볼게요", small=True))
sc(4,4,"photo",   dict(kind="photo", img="ph_cafe_window", center="소개팅 장소"))
sc(5,5,"photo",   dict(kind="photo", img="ph_door_open", center="상대가 들어온다"))
sc(6,6,"ember",   dict(kind="portrait", img="p_woman_enter", label="사진보다 훨씬"))
sc(7,7,"violet",  dict(kind="hero3d", img="i3_brain", big="머리가 바빠진다"))
sc(8,8,"violet",  dict(kind="bubbles", tone="thought", title="머릿속",
                       items=["잘 보여야 되는데","재밌게 해야 되는데","첫인상 망치면 안 되는데"]))
sc(9,9,"teal",    dict(kind="hero3d", img="i3_bubble", big="인사", small=True))
sc(10,10,"teal",  dict(kind="bubbles", tone="say", ok=True, title="첫마디", items=["안녕하세요."]))
sc(11,11,"charcoal",dict(kind="hero3d", img="i3_door", big="여기서부터", sub2="조금씩 달라진다"))
sc(12,14,"slate", dict(kind="bubbles", tone="say", title="첫 5분 동안 한 말",
                       items=["오는 길 괜찮으셨어요?","여기 찾기 어렵진 않으셨어요?","뭐 드실래요?"]))
sc(15,17,"slate", dict(kind="bubbles", tone="say", title="첫 5분 동안 한 말",
                       items=["저는 아무거나 괜찮아요.","편하신 걸로 드세요.","사진보다 훨씬 예쁘시네요."]))
sc(18,19,"teal",  dict(kind="list", title="말 자체는 문제가 없다", mark="check",
                       items=["이상한 말은 없다","오히려 친절하다","상대도 배려하고 있다"]))
sc(20,20,"ember", dict(kind="compare", title="무엇이 전달되는가",
                       left=("무슨 말을 했느냐","말의 내용",34),
                       right=("그 말을 하는 사람의 상태","태도와 상태",94)))
sc(21,21,"blue",  dict(kind="hero3d", img="i3_eye", big="계속 반응을 확인한다", small=True))
sc(22,24,"blue",  dict(kind="list", title="머릿속 체크리스트", mark="q",
                       items=["내가 웃기면 웃는지","표정이 굳지는 않았는지","내가 마음에 드는 것 같은지"]))
sc(25,25,"photo", dict(kind="photo", img="ph_mirror", center="상대가 좋아할 답을 먼저 찾는다"))
sc(26,26,"slate", dict(kind="hero3d", img="i3_mirror", big="첫인상", sub2="보통은 외모부터 떠올린다"))
sc(27,30,"slate", dict(kind="chips", title="외모 항목", items=["옷","머리","키","목소리"]))
sc(31,31,"slate", dict(kind="hero", big="물론 다 포함됩니다", small=True))
sc(32,32,"photo", dict(kind="photo", img="ph_two_talking", center="그것만 보고 있지는 않다"))
sc(33,37,"teal",  dict(kind="list", title="같이 읽히는 것들", mark="dot",
                       items=["말을 얼마나 급하게 하는지","얼마나 기다려주는지","자기 의견이 있는지",
                              "어색할 때 어떻게 반응하는지","실수했을 때 얼마나 흔들리는지"]))
sc(38,38,"teal",  dict(kind="hero3d", img="i3_magnifier", big="이런 것도 같이 인식된다", small=True))
sc(39,39,"ember", dict(kind="strike", target="첫인상 = 외모", note="저는 그렇게 보지 않습니다"))
sc(40,41,"ember", dict(kind="quote", big="마음에 드는 사람을 만났을 때\n나는 어떤 사람이 되는가"))
sc(42,42,"charcoal",dict(kind="hero3d", img="i3_question", big="한번 생각해보세요", small=True))
sc(43,43,"photo", dict(kind="photo", img="ph_cafe", center="마음에 안 들면 오히려 편하다"))
sc(44,44,"photo", dict(kind="photo", img="ph_menu", center="메뉴를 본다"))
sc(45,45,"slate", dict(kind="bubbles", tone="say", ok=True, title="나",
                       items=["저는 아메리카노 마실게요.","뭐 드실래요?"]))
sc(46,47,"slate", dict(kind="hero3d", img="i3_glass", big="그냥 자연스럽습니다", small=True))
sc(48,48,"teal",  dict(kind="bubbles", tone="her", title="상대",
                       items=["저는 여행할 때 계획 안 짜는 게 좋아요."]))
sc(49,51,"teal",  dict(kind="bubbles", tone="say", ok=True, title="나",
                       items=["진짜요? 저는 계획 엄청 짜는데","완전 반대네요."]))
sc(52,52,"ember", dict(kind="hero3d", img="i3_key", big="상황이 바뀐다",
                       sub2="정말 마음에 드는 사람 앞에서"))
sc(53,54,"ember", dict(kind="bubbles", tone="her", title="상대", portrait="p_woman_listen",
                       items=["저는 여행할 때 계획 많이 짜는 사람이 좋아요."]))
sc(55,55,"violet",dict(kind="compare", title="실제 취향", neutral=True,
                       left=("즉흥 여행","남자의 진짜 취향",90),
                       right=("계획 여행","상대가 말한 취향",22)))
sc(56,57,"violet",dict(kind="bubbles", tone="thought", title="머릿속",
                       items=["나는 계획 잘 안 짜는데","안 맞는 사람처럼 보이려나?"]))
sc(58,60,"violet",dict(kind="bubbles", tone="say", warp=True, title="입 밖으로 나온 말",
                       items=["저도 계획 짜는 편이에요."]))
sc(61,61,"charcoal",dict(kind="hero", big="한 번이면 괜찮습니다", small=True))
sc(62,62,"blue",  dict(kind="portrait", img="p_man_tense", label="사람이 흐릿해진다", fade=True))
sc(63,66,"blue",  dict(kind="list", title="반복되는 대답", mark="loop",
                       items=["좋아한다고 하면 나도 좋아한다고 하고","싫어한다고 하면 나도 별로라고 하고",
                              "장소는 아무 데나 괜찮다고 하고","메뉴도 아무거나 괜찮다고 합니다"]))
sc(67,68,"photo", dict(kind="photo", img="ph_table", center="어떤 사람인지 알기 어려워진다"))
sc(69,69,"ember", dict(kind="hero3d", img="i3_puzzle", big="중요한 차이", small=True))
sc(70,70,"ember", dict(kind="split", title="이건 서로 다른 문제입니다",
                       a="좋은 사람으로 보이는 것", b="나라는 사람이 보이는 것"))
sc(71,74,"slate", dict(kind="list", title="좋은 사람으로 보이려고 하면", mark="minus",
                       items=["싫어할 말을 피하고","의견 충돌을 피하고","이상한 반응이 나오면 바로 수습한다"]))
sc(75,78,"teal",  dict(kind="list", title="나라는 사람이 보이려면", mark="plus",
                       items=["내 취향도 나와야 하고","내 생각도 나와야 하고","다른 부분도 나와야 한다"]))
sc(79,83,"teal",  dict(kind="bubbles", tone="her", dense=True, title="그래야 판단할 수 있다",
                       items=["이 사람은 이런 사람이구나.","이런 건 나랑 잘 맞네.",
                              "이건 나랑 좀 다르네.","근데 이런 부분은 괜찮다."]))
sc(84,84,"photo", dict(kind="photo", img="ph_desk_note", center="사람을 알아가는 과정"))
