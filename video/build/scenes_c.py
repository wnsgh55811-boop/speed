# -*- coding: utf-8 -*-
from scenes_a import S, s

s("s54","photo_cafe", dict(kind="photo", img="menu2", center="메뉴를 고른다"),
  ["예를 들어 메뉴를 고릅니다"])

s("s55","slate", dict(kind="bubbles", tone="her", title="상대", items=["뭐 드실래요?"]),
  ["여자가 묻습니다","뭐 드실래요?"])

s("s56","slate", dict(kind="beforeafter", title="대답을 바꾸면",
                      before="저는 아무거나 괜찮아요. 드시고 싶은 걸로 하세요.",
                      after="저는 커피 마실 건데 혹시 드시고 싶은 거 있어요?"),
  ["예전에는","저는 아무거나 괜찮아요. 드시고 싶은 걸로 하세요.","라고 했다면","이제는",
   "저는 커피 마실 건데 혹시 드시고 싶은 거 있어요?","라고 하면 됩니다"])

s("s57","slate", dict(kind="mutual", title="둘 다 남는다", a="내 선택", b="상대의 선택"),
  ["내 선택도 있고 상대의 선택도 있습니다"])

s("s58","ember", dict(kind="bubbles", tone="her", title="상대", items=["저는 사람 많은 곳 진짜 싫어해요."]),
  ["여자가 말합니다","저는 사람 많은 곳 진짜 싫어해요."])

s("s59","ember", dict(kind="bubbles", tone="say", title="나", ok=True,
                      items=["저는 오히려 조금 북적거리는 데가 좋던데","완전 반대네요."]),
  ["내가 사람 많은 곳을 좋아한다면","저는 오히려 조금 북적거리는 데가 좋던데 완전 반대네요.","라고 하면 됩니다"])

s("s60","teal", dict(kind="strike", target="이게 공격적인가요?", note="전혀 아닙니다", soft=True),
  ["이게 공격적인가요?","전혀 아니죠"])

s("s61","teal", dict(kind="bubbles", tone="mix", title="오히려 대화가 생긴다",
                     items=["왜 그런 데 좋아하세요?","저는 조용하면 오히려 어색하더라고요."]),
  ["오히려 대화할 게 생깁니다","왜 그런 데 좋아하세요?","저는 조용하면 오히려 어색하더라고요."])

s("s62","teal", dict(kind="mutual", title="서로를 알아간다", a="나", b="상대", glow=True),
  ["이제 둘이 서로를 알아갑니다"])

s("s63","blue", dict(kind="hero", big="다르면 안 맞는 것 같다", sub2="많은 남자들이 두려워하는 지점", icon="fear"),
  ["그런데 많은 남자들은 이런 차이가 생기는 걸 두려워합니다","다르면 안 맞는 것 같거든요"])

s("s64","violet", dict(kind="venn", title="관계에서 중요한 것",
                       a="나", b="상대", mid="차이를 편하게\n말할 수 있는가"),
  ["근데 관계에서 중요한 건 모든 게 같은 사람이 되는 게 아닙니다",
   "서로 다른 두 사람이 그 차이를 편하게 이야기할 수 있느냐가 훨씬 중요합니다"])

s("s65","ember", dict(kind="hero", big="과한 해명", sup="첫 만남에서 자주 나오는 것", icon="megaphone"),
  ["그리고 첫 만남에서 또 하나 굉장히 많이 나오는 게 있습니다","과한 해명입니다"])

s("s66","slate", dict(kind="bubbles", tone="say", title="이러면 끝날 일", ok=True, items=["아 말 꼬였네요."]),
  ["말이 한번 꼬였습니다","그냥","아 말 꼬였네요.","하고 웃으면 끝날 일입니다"])

s("s67","slate", dict(kind="bubbles", tone="say", title="불안하면 바로 설명한다",
                      items=["제가 원래 말은 잘하는데 오늘 좀 긴장했나 봐요."]),
  ["근데 불안한 사람은 바로 설명합니다","제가 원래 말은 잘하는데 오늘 좀 긴장했나 봐요."])

s("s68","blue", dict(kind="bubbles", tone="say", title="덧붙이기 시작한다", dense=True, pile=True,
                     items=["아 물론 그런 뜻으로 말한 건 아니고요.","사람마다 다르긴 하죠.","제가 표현을 좀 이상하게 했네요."]),
  ["여자가 잠깐 표정이 굳었습니다","바로 덧붙입니다","아 물론 그런 뜻으로 말한 건 아니고요.",
   "사람마다 다르긴 하죠.","제가 표현을 좀 이상하게 했네요."])

s("s69","blue", dict(kind="growdot", title="상황의 크기", small_l="상대가 느낀 크기", big_l="내가 키운 크기"),
  ["상대는 별생각 없었는데 본인이 상황을 더 크게 만드는 경우가 있어요"])

s("s70","violet", dict(kind="hero", big="왜 그럴까요?", small=True, icon="question"),
  ["왜 그럴까요?"])

s("s71","violet", dict(kind="compare", title="진짜 두려운 것",
                       left=("실수 자체","",26), right=("그 실수로 나를 안 좋게 볼까 봐","",94)),
  ["실수 자체가 두려운 게 아니라 그 실수 때문에 상대가 나를 안 좋게 볼까 봐 두려운 겁니다"])

s("s72","violet", dict(kind="icons", title="그래서 하는 일",
                       items=[("repair","이미지 복구"),("loop","계속 수습"),("mask","괜찮은 척")]),
  ["그래서 계속 자기 이미지를 복구하려고 합니다"])

s("s73","ember", dict(kind="bars", title="불안이 더 크게 보이는 쪽", lo="적게 보임", hi="크게 보임",
                      rows=[("급하게 수습하는 태도", 90, "pink"),("실제 실수", 30, "amber")]),
  ["근데 아이러니하게도 실제 실수보다 그걸 급하게 수습하려는 태도에서 불안함이 더 크게 보일 때가 있습니다"])

s("s74","charcoal", dict(kind="hero", big="공백의 태도", sup="이전 영상에서 이야기한", icon="pause"),
  ["여기서 제가 이전 영상에서 이야기했던 공백의 태도와도 연결됩니다"])

s("s75","slate", dict(kind="list", title="공백을 못 견딜 때", mark="minus",
                      items=["침묵이 생기면 질문한다","실수하면 해명한다","표정이 애매하면 수습한다","의견이 다르면 수정한다"]),
  ["침묵이 생기면 질문합니다","실수하면 해명합니다","상대 표정이 애매하면 수습합니다","의견이 다르면 수정합니다"])

s("s76","slate", dict(kind="hero", big="아무것도 안 해도 되는 순간", sub2="그걸 못 견디는 것", icon="pause"),
  ["아무것도 하지 않아도 되는 순간을 못 견디는 겁니다"])

s("s77","ember", dict(kind="strike", target="멋있는 첫마디 외우기", note="중요한 건 여기가 아닙니다"),
  ["소개팅 첫 1분에서 중요한 건 멋있는 첫마디를 외우는 게 아닙니다"])

s("s78","ember", dict(kind="hero", big="세 가지", sup="대신 이걸 보세요", icon="three", ring=True),
  ["저는 오히려 세 가지를 봤으면 좋겠습니다"])
