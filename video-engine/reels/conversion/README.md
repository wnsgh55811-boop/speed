# 릴스 — 마케팅의 핵심은 전환 (9:16, 29초)

1080×1920 / 30fps. 나레이션은 힉스필드 Seed Audio 1.0의 "내-목소리-v4" 보이스(speech_rate 20, 약 1.2배속)로 생성했다.

| 파일 | 내용 |
|---|---|
| `build.py` | 씬 10개와 자막 23개를 정의한다. 자막 폭을 실측해 한 줄을 넘으면 빌드가 실패한다. 결과는 `index.html` |
| `style.css` | 9:16 디자인: 배경 4계열 로테이션, 라임 포인트, 자막 띠 위치 y=1452 |
| `motion.js` | GSAP 타임라인. 시각은 나레이션 쉬는 구간에 맞춰 잡았다 |

## 다시 빌드하기

`assets/fonts`, `vendor`, `assets/audio`는 git에 올리지 않는다.

```bash
npm pack pretendard@1.3.9 && tar xzf pretendard-1.3.9.tgz   # → assets/fonts/Pretendard-{Medium,Bold,ExtraBold,Black}.otf
npm pack gsap@3.12.5 && tar xzf gsap-3.12.5.tgz             # → vendor/gsap.min.js
# 나레이션 → assets/audio/narr.mp3 (힉스필드 결과물 CDN)
python3 build.py
npx hyperframes@0.8.52 render . -o renders/final.mp4 -q delivery -f 30 --no-browser-gpu
```
