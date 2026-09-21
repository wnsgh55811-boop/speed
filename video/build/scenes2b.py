# -*- coding: utf-8 -*-
from scenes2a import S2, sc

sc(85,85,"ember", dict(kind="bars", title="소개팅에서 더 중요하게 여기는 것", lo="적음", hi="많음",
                       rows=[("좋은 평가를 받는 것",92,"pink"),("판단할 재료를 주는 것",24,"amber")]))
sc(86,89,"violet",dict(kind="scale", title="관계의 구조가 기울어진다", img="i3_balance",
                       up="상대 : 평가하는 사람", down="나 : 평가받는 사람"))
sc(90,90,"violet",dict(kind="hero3d", img="i3_clipboard", big="내가 지원자가 된다", small=True))
sc(91,94,"blue",  dict(kind="list", title="그래서 생기는 긴장", mark="minus", bgphoto="ph_alone_phone",
                       items=["실수하면 안 될 것 같고","정답을 말해야 할 것 같고","좋아하는 모습을 보여줘야 할 것 같다"]))
sc(95,96,"blue",  dict(kind="strike", target="소개팅 = 면접", note="이 구조부터 바꿔야 합니다"))
sc(97,101,"teal", dict(kind="list", title="여러분도 상대를 봅니다", mark="q",
                       items=["나랑 대화가 잘 맞는 사람인지","내가 실제로 좋아할 만한 사람인지",
                              "사람을 대하는 태도가 어떤지","연애를 바라보는 기준이 비슷한지"]))
sc(102,103,"teal",dict(kind="mutual", title="서로 본다", a="나", b="상대"))
sc(104,104,"photo",dict(kind="photo", img="ph_hands_cup", center="메뉴를 고른다"))
sc(105,106,"slate",dict(kind="bubbles", tone="her", title="상대", portrait="p_woman_arms",
                        items=["뭐 드실래요?"]))
sc(107,112,"slate",dict(kind="beforeafter", title="대답을 바꾸면",
                        before="저는 아무거나 괜찮아요. 드시고 싶은 걸로 하세요.",
                        after="저는 커피 마실 건데 혹시 드시고 싶은 거 있어요?"))
sc(113,113,"slate",dict(kind="mutual", title="둘 다 남는다", a="내 선택", b="상대의 선택"))
sc(114,115,"photo",dict(kind="photo", img="ph_restaurant", center="저는 사람 많은 곳 진짜 싫어해요"))
sc(116,118,"ember",dict(kind="bubbles", tone="say", title="나", portrait="p_man_settled", pw=430,
                        items=["저는 오히려 조금 북적거리는 데가 좋던데","완전 반대네요."]))
sc(119,119,"teal",dict(kind="hero", big="이게 공격적인가요?"))
sc(120,120,"teal",dict(kind="hero", big="전혀 아닙니다"))
sc(121,123,"teal",dict(kind="bubbles", tone="mix", title="오히려 대화가 생긴다", bgphoto="ph_woman_laugh",
                       items=["왜 그런 데 좋아하세요?","저는 조용하면 오히려 어색하더라고요."]))
sc(124,124,"teal",dict(kind="portrait", img="p_woman_smile", label="이제 서로를 알아간다"))
sc(125,127,"blue",dict(kind="hero3d", img="i3_lock", big="다르면 안 맞는 것 같다",
                       sup="많은 남자들이 두려워하는 것", small=True))
sc(128,129,"violet",dict(kind="venn", title="관계에서 중요한 것", a="나", b="상대",
                         mid="편하게 말할 수 있는가"))
sc(130,131,"ember",dict(kind="hero3d", img="i3_mic", big="과한 해명", sup="첫 만남에서 자주 나오는 것"))
sc(132,135,"slate",dict(kind="bubbles", tone="say", portrait="p_man_laugh",
                        items=["아 말 꼬였네요."]))
sc(136,137,"slate",dict(kind="bubbles", tone="say", title="불안하면 바로 설명한다", portrait="p_man_shrug",
                        items=["제가 원래 말은 잘하는데 오늘 좀 긴장했나 봐요."]))
sc(138,142,"blue",dict(kind="bubbles", tone="say", dense=True, pile=True, title="덧붙이기 시작한다",
                       items=["아 물론 그런 뜻으로 말한 건 아니고요.","사람마다 다르긴 하죠.",
                              "제가 표현을 좀 이상하게 했네요."]))
sc(143,143,"blue",dict(kind="growdot", title="상황의 크기",
                       small_l="상대가 느낀 크기", big_l="내가 키운 크기"))
sc(144,144,"violet",dict(kind="hero3d", img="i3_question", big="왜 그럴까요?", small=True))
sc(145,145,"violet",dict(kind="compare", title="진짜 두려운 것",
                         left=("실수 자체","",26), right=("나를 안 좋게 볼까 봐","",94)))
sc(146,146,"violet",dict(kind="hero3d", img="i3_mask", big="이미지를 복구하려고 한다", small=True))
sc(147,147,"ember",dict(kind="bars", title="불안이 더 크게 보이는 쪽", lo="적게 보임", hi="크게 보임",
                        rows=[("급하게 수습하는 태도",90,"pink"),("실제 실수",30,"amber")]))
sc(148,148,"photo",dict(kind="photo", img="ph_window", center="공백의 태도"))
sc(149,152,"slate",dict(kind="list", title="공백을 못 견딜 때", mark="minus",
                        items=["침묵이 생기면 질문한다","실수하면 해명한다",
                               "표정이 애매하면 수습한다","의견이 다르면 수정한다"]))
sc(153,153,"slate",dict(kind="hero3d", img="i3_pause", big="아무것도 안 해도 되는 순간",
                        sub2="그걸 못 견디는 것"))
sc(154,154,"ember",dict(kind="hero", big="중요한 건 멋진 멘트가 아닙니다", small=True))
sc(155,156,"blue",dict(kind="chapter", num="01", big="나를 낮추지 않기"))
sc(157,158,"blue",dict(kind="split", title="이건 전혀 다른 얘기입니다",
                       a="상대가 매력적이다", b="내가 더 낮은 사람이다", cross_b=True))
sc(159,160,"blue",dict(kind="portrait", img="p_man_calm", label="나를 낮출 필요는 없다"))
sc(161,162,"teal",dict(kind="chapter", num="02", big="조금씩 나를 보여주기"))
sc(163,166,"teal",dict(kind="bubbles", tone="say", crossed=True, loud=True, title="이런 말은 필요 없습니다", portrait="p_man_away",
                       items=["저는 책임감 있는 남자입니다.","저는 여자친구한테 정말 잘합니다."]))
sc(167,171,"teal",dict(kind="bubbles", tone="say", ok=True, dense=True, title="작은 취향이면 충분합니다",
                       items=["저는 이건 좋아해요.","저는 그건 좀 별로예요.",
                              "저는 여행할 때 이런 스타일이에요.","저는 주말은 이렇게 보내는 게 좋더라고요."]))
sc(172,172,"teal",dict(kind="gauge", title="사람이 보이는 정도", lo="흐릿함", hi="또렷함", value=86,
                       caption="작은 정보가 쌓이면서"))
sc(173,174,"violet",dict(kind="chapter", num="03", big="반응보다 조금 느리게"))
sc(175,180,"violet",dict(kind="list", title="바로 안 해도 됩니다", mark="pause",
                         items=["조용해졌다고 바로 질문할 필요 없습니다","표정이 바뀌었다고 바로 수습하지 않아도 됩니다",
                                "의견이 다르다고 바로 철회하지 않아도 됩니다"]))
sc(181,183,"violet",dict(kind="steps", title="이 순서로",
                         items=["한 번 듣고","한 번 생각하고","그다음 반응한다"]))
sc(184,184,"violet",dict(kind="portrait", img="p_man_think", w=560))
sc(185,185,"ember",dict(kind="split", title="완전히 다릅니다",
                        a="선택받으려고 애쓰기", b="서로 선택하기", pick_b=True))
sc(186,187,"ember",dict(kind="compare", title="상대의 반응이 무엇이 되는가", neutral=True,
                        left=("시험 결과","선택받으려고 할 때",88),
                        right=("하나의 정보","서로 선택할 때",88)))
sc(188,191,"slate",dict(kind="bubbles", tone="thought", loud=True, bigbub=True, title="이렇게 생각하면 됩니다",
                        items=["아 이 사람은 이런 걸 별로 안 좋아하는구나."]))
sc(192,194,"slate",dict(kind="bubbles", tone="thought", crossed=True, portrait="p_woman_flat", tight=True, title="여기까지 갈 필요 없습니다",
                        items=["내가 잘못했나?"]))
sc(195,197,"teal",dict(kind="hero3d", img="i3_dial", big="그것도 정보입니다", small=True))
sc(198,198,"charcoal",dict(kind="portrait", img="p_man_full", label="가장 먼저 전달되는 것"))
sc(199,203,"blue",dict(kind="list", title="설명보다 먼저 드러나는 것", mark="dot", bgphoto="ph_over_shoulder",
                       items=["마음에 드는 사람 앞에서도 나로 있을 수 있는지","어색한 순간을 견딜 수 있는지",
                              "다른 의견을 편하게 말할 수 있는지"]))
sc(204,204,"ember",dict(kind="strike", target="첫마디 뭐 하지?", note="여기부터 고민하지 마세요"))
sc(205,206,"ember",dict(kind="quote", big="알아가는 중인가, 평가받는 중인가"))
sc(207,210,"slate",dict(kind="list", title="평가받는 느낌이 든다면", mark="q",
                        items=["너무 많이 맞춰주고 있지는 않은지","자꾸 말을 수습하고 있지는 않은지",
                               "내 의견을 숨기고 있지는 않은지"]))
sc(211,212,"teal",dict(kind="split", title="소개팅은", bgphoto="ph_woman_laugh", a="완벽한 모습을 보여주는 시간",
                       b="서로 알아보기 시작하는 시간", cross_a=True, pick_b=True))
sc(213,215,"charcoal",dict(kind="hero3d", img="i3_stopwatch", big="첫 1분에 결정된다",
                          sub2="이 말의 진짜 의미"))
sc(216,217,"blue",dict(kind="split", title="무엇이 빠르게 드러나는가",
                       a="여러분의 모든 조건", b="마음에 드는 사람 앞에서의 태도",
                       cross_a=True, pick_b=True))
sc(218,220,"photo",dict(kind="photo", img="ph_street_rain", center="아주 빠르게 드러난다"))
sc(221,225,"violet",dict(kind="list", title="반복되는 태도", mark="minus",
                         items=["눈치","과한 배려","과한 해명","조급함"]))
sc(226,227,"violet",dict(kind="hero3d", img="i3_hourglass", big="같은 문제가 반복됩니다",
                         sup="좋은 말을 아무리 준비해도", small=True))
sc(228,229,"photo",dict(kind="photo", img="ph_empty_chair", center="다음 관계로 이어지지 않는다"))
sc(230,231,"slate",dict(kind="bubbles", tone="her", title="반복해서 듣는 말", portrait="p_woman_eval",
                        items=["좋은 사람인데 남자로는 잘 모르겠어요."]))
sc(232,232,"ember",dict(kind="cta", big="무료 비밀 특강", sub2="설명란에서 확인해보세요"))
sc(233,235,"photo",dict(kind="photo", img="ph_walk_two",
                        seq=["바꿔야 할 건", "첫마디가 아니라", "태도입니다"]))
