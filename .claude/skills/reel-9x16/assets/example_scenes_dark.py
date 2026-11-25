# Example scenes.py for assets/reel_dark.html (dating series).
# (anchor, scene) — anchor = the subtitle line where the scene starts (prefix match, spaces/quotes ignored).
# Inside scenes "@line" = time that line starts. None in icons/kakao events = scene start.
# icons(...) events: (at, "w"|"m", text|None|"", append 0/1, mood)
#   text "~..." = thought cloud, "" hides the bubble, None keeps the previous text; emoji-only text shows without a box.
#   moods: neutral smile happy sweat annoyed cool flat
# kakao(...) events: (at, "in"|"out", text)   keep <= 5 bubbles per kakao scene
# meme(name, "‘캡션’", ov=[[x%, y%, w%, "text", px]])  name = memes/<name>.jpg
TITLE = {"t1": "적극적인 남자,", "t2": "여자는 싫어한다?", "end": "@왜 그럴까요?"}

SCENES = [
    ("여자는", meme("surprised_cat", "‘적극적인 남자가 싫다고?!’")),
    ("왜 그럴까요?", text()),
    ("예를 들어", icons((None, "w", "", 0, "smile"), (None, "m", "", 0, "happy"))),
    ("다음 주 금요일에", kakao(("@다음 주 금요일에", "out", "다음 주 금요일에 시간 괜찮으세요?"),
                              ("@그날은 바쁘다고", "in", "아 그날은 좀 바빠서요ㅠ"),
                              ("@그럼 토요일은요?", "out", "그럼 토요일은요?"))),
    ("이렇게 계속", meme("begging_cat", "‘제발 시간 좀…’")),
    ("그런데 여자 입장에서는", icons((None, "w", "~바쁘다고 했는데…", 0, "flat"), (None, "m", "", 0, "happy"))),
    ("왜 그럴까요?", text()),          # anchors are searched forward from the previous scene, so repeated lines just work
                                        # (optional 3rd item n = skip to the n-th match ahead)
    ("하지만 조급한 남자는", meme("vader", "‘내 뜻대로 되어라…’")),
    ("그런데", icons((None, "w", "", 0, "neutral"), (None, "m", "", 0, "cool"))),
    ("태도 하나만 바꿔도", text()),
    ("프로필 링크의", cta(sub="비공개 특강 · 이다사 태도 부트캠프")),
    # comment-keyword CTA with nothing under the pill:
    # ("댓글에", cta(pill='<span class="emo">💬</span>댓글에 ‘마음’', sub="")),
]
