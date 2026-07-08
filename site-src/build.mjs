import { mkdirSync, writeFileSync } from "fs";
import { shell, KAKAO, IMG, logoFull } from "./shell.mjs";
import { columns, columnCats, seedReviews, reviewCats, diagnoses } from "./data.mjs";

const OUT = new URL("../imweb-export/", import.meta.url).pathname;
mkdirSync(OUT, { recursive: true });

const esc = (s) => s.replace(/</g, "&lt;").replace(/>/g, "&gt;");

/* ─────────────────────────── index.html ─────────────────────────── */
const painPoints = [
  "상대가 예전 같지 않다.",
  "연락 빈도가 줄었는데 이유를 모르겠다.",
  "내가 뭘 잘못했는지 계속 생각하게 된다.",
  "붙잡아야 할지, 기다려야 할지 모르겠다.",
  "재회를 원하지만 먼저 연락하면 더 멀어질까 봐 두렵다.",
  "연애할 때마다 비슷한 패턴으로 무너진다.",
];

const programsCards = [
  {
    t: "연애 상담", href: "programs.html#dating",
    who: ["썸에서 관계가 애매해진 분", "연애 중 상대가 식은 것 같은 분", "불안형·회피형 패턴이 반복되는 분", "연락·표현 문제로 자주 다투는 분"],
    q: "지금 관계가 어디서 꼬였는지, 어떤 순서로 풀어야 하는지 진단합니다.",
  },
  {
    t: "재회 상담", href: "programs.html#reunion",
    who: ["이별 후 연락 타이밍을 고민하는 분", "차단·읽씹·무반응 상태인 분", "마지막 연락을 어떻게 할지 모르는 분", "재회 가능성과 방향이 궁금한 분"],
    q: "재회는 감정으로 밀어붙이는 것이 아니라 상대의 심리적 저항을 낮추는 과정입니다.",
  },
  {
    t: "관계 패턴 진단", href: "programs.html#pattern",
    who: ["연애할 때마다 비슷하게 무너지는 분", "항상 내가 더 불안해지는 분", "상대에게 맞추다 지치는 분", "사랑받고 싶은데 매달리게 되는 분"],
    q: "반복되는 연애 문제는 상대만의 문제가 아니라 내 관계 패턴에서 시작되는 경우가 많습니다.",
  },
];

const situations = [
  ["연애 중인데 불안하다", "연애 상담", "programs.html#dating"],
  ["헤어진 지 얼마 안 됐다", "재회 상담", "programs.html#reunion"],
  ["연락을 보내야 할지 모르겠다", "재회 전략 상담", "programs.html#reunion"],
  ["매번 같은 연애를 반복한다", "관계 패턴 진단", "programs.html#pattern"],
  ["카톡을 어떻게 해야 할지 모르겠다", "카톡 분석 상담", "reviews.html"],
];

const diffs = [
  "연락 문장보다 관계 흐름을 먼저 봅니다.",
  "감정 위로보다 현실적인 전략을 제시합니다.",
  "상대 심리와 내 패턴을 함께 분석합니다.",
  "재회 가능성을 무조건 긍정하지 않습니다.",
  "상담 후 바로 실행할 수 있는 방향을 드립니다.",
  "실제 카톡, 이별 과정, 상대 반응을 바탕으로 분석합니다.",
];

const indexBody = `
<section class="section section-white" style="padding-top:72px">
  <div class="container center reveal">
    <div style="margin-bottom:-6px">${logoFull()}</div>
    <span class="chip-badge">누적 6,500건 이상 · 7년간의 연애·재회 상담 분석</span>
    <h1 class="title" style="max-width:660px">연락 한 번을 더 보내기 전에,<br>먼저 관계의 흐름부터 봐야 합니다.</h1>
    <p class="lead" style="max-width:540px">러브백 관계 연구소는 연애, 이별, 재회 상황을<br>감정이 아닌 관계 패턴과 상대 심리로 분석합니다.</p>
    <div class="gap-btns" style="margin-top:6px">
      <a href="apply.html" class="btn btn-navy btn-lg">상담 신청하기</a>
      <a href="reviews.html" class="btn btn-line btn-lg">후기 먼저 보기</a>
    </div>
  </div>
  <div class="container reveal reveal-d1" style="margin-top:52px">
    <div class="img-frame" style="aspect-ratio:16/7">
      <img src="${IMG.studio}" alt="러브백 관계 연구소 상담 공간" loading="lazy" onerror="this.parentElement.style.display='none'">
    </div>
  </div>
</section>

<section class="section">
  <div class="container center reveal">
    <span class="eyebrow">Are you here?</span>
    <h2 class="title">지금 당신이 힘든 이유는<br>연락 때문만이 아닙니다.</h2>
    <hr class="gold-bar">
    <p class="lead">혹시 이런 상황인가요?</p>
  </div>
  <div class="container" style="margin-top:38px">
    <div class="grid grid-2">
      ${painPoints.map((p, i) => `<div class="card card-flat reveal${i % 2 ? " reveal-d1" : ""}" style="display:flex;align-items:center;gap:14px;padding:22px 26px">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#b2935b" stroke-width="2.4" style="flex-shrink:0"><path d="M20 6L9 17l-5-5"/></svg>
        <span style="font-size:15.5px">${p}</span></div>`).join("\n")}
    </div>
  </div>
</section>

<section class="section section-navy">
  <div class="wrap-md center reveal">
    <span class="eyebrow eyebrow-light">Loveback Perspective</span>
    <h2 class="title">연애도 결국,<br>남녀 간의 인간관계입니다.</h2>
    <hr class="gold-bar">
    <p class="lead-light">러브백은 "언제 연락해야 하나요?", "카톡 뭐라고 보내야 하나요?"만 보는 곳이 아닙니다. 관계가 어디서 틀어졌는지, 상대는 지금 어떤 심리 상태인지, 내가 어떤 위치에 서 있는지부터 봅니다.</p>
    <p class="lead-light">연락은 기술이 아니라 결과물입니다.<br>흐름이 정리되지 않은 상태에서 보내는 연락은<br>오히려 상대를 더 멀어지게 만들 수 있습니다.</p>
  </div>
</section>

<section class="section section-white">
  <div class="container center reveal">
    <span class="eyebrow">Programs</span>
    <h2 class="title">지금 상황에 맞는 상담을 찾아보세요</h2>
    <hr class="gold-bar">
  </div>
  <div class="container" style="margin-top:42px">
    <div class="grid grid-3">
      ${programsCards.map((c, i) => `<a href="${c.href}" class="card reveal reveal-d${i}">
        <h3 class="title-sm" style="margin-bottom:16px">${c.t}</h3>
        <ul class="list-plain" style="color:#5a6380;font-size:14.5px;line-height:2">
          ${c.who.map((w) => `<li>· ${w}</li>`).join("")}
        </ul>
        <hr class="divider">
        <p style="font-size:14.5px;font-weight:600;color:#8a6f3e;line-height:1.75">${c.q}</p>
        <p style="margin-top:16px;font-size:14px;font-weight:600;color:#1d2743">자세히 보기 →</p>
      </a>`).join("\n")}
    </div>
  </div>
</section>

<section class="section section-cream">
  <div class="wrap-md center reveal">
    <h2 class="title">내 상황에는 어떤 상담이 맞을까요?</h2>
    <hr class="gold-bar">
  </div>
  <div class="wrap-md reveal reveal-d1" style="margin-top:34px;display:flex;flex-direction:column;gap:12px">
    ${situations.map(([s, t, h]) => `<a href="${h}" class="card card-flat" style="display:flex;justify-content:space-between;align-items:center;gap:10px;padding:20px 26px;flex-wrap:wrap">
      <span style="font-size:15.5px">${s}</span>
      <span style="color:#8a6f3e;font-weight:600;font-size:14.5px;white-space:nowrap">${t} →</span></a>`).join("\n")}
  </div>
</section>

<section class="section section-white">
  <div class="container center reveal">
    <span class="eyebrow">Reviews</span>
    <h2 class="title">나와 비슷한 사람들의 이야기</h2>
    <hr class="gold-bar">
    <p class="lead">후기는 자랑이 아니라, 지금의 내 상황을 대입해보는 공간입니다.</p>
  </div>
  <div class="container" style="margin-top:42px">
    <div class="grid grid-3">
      ${seedReviews.slice(0, 3).map((r, i) => `<a href="reviews.html" class="card reveal reveal-d${i}" style="background:#faf7f0">
        <span class="chip-badge" style="margin-bottom:16px">${reviewCats.find(([v]) => v === r.cat)[1]} 후기</span>
        <p class="serif" style="font-size:16.5px;line-height:1.7;margin-bottom:12px">“${r.title}”</p>
        <p style="font-size:14px;color:#5a6380;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden">${r.content}</p>
        <p style="margin-top:14px;font-size:12.5px;color:#9aa0b4">${r.nick} · ${r.meta}</p>
      </a>`).join("\n")}
    </div>
    <div class="center reveal" style="margin-top:34px">
      <a href="reviews.html" class="btn btn-line">후기 전체 보기</a>
    </div>
  </div>
</section>

<section class="section section-navy">
  <div class="container center reveal">
    <span class="eyebrow eyebrow-light">Why Loveback</span>
    <h2 class="title">상담소가 아니라, 관계 연구소입니다</h2>
    <hr class="gold-bar">
  </div>
  <div class="container" style="margin-top:38px">
    <div class="grid grid-2">
      ${diffs.map((d, i) => `<div class="reveal${i % 2 ? " reveal-d1" : ""}" style="display:flex;gap:16px;align-items:flex-start;border:1px solid rgba(244,241,232,.14);border-radius:6px;padding:22px 26px">
        <span class="serif" style="color:#cbb489;font-size:18px">${String(i + 1).padStart(2, "0")}</span>
        <span style="color:rgba(244,241,232,.88);font-size:15px">${d}</span></div>`).join("\n")}
    </div>
  </div>
</section>

<section class="section section-cream" style="position:relative;overflow:hidden">
  <div class="wrap-md center reveal" style="position:relative;z-index:1">
    <span class="eyebrow">Free Check</span>
    <h2 class="title">내 관계가 지금 회복 가능한<br>흐름인지 알고 싶다면?</h2>
    <hr class="gold-bar">
    <p class="lead">결제 전에, 무료 체크리스트로 현재 상태를 먼저 점검해보세요.</p>
    <a href="diagnosis.html" class="btn btn-navy btn-lg">무료 관계 진단 시작하기</a>
  </div>
</section>

<section class="section section-white">
  <div class="wrap-md center reveal">
    <h2 class="title">지금 이 관계,<br>혼자 고민하지 마세요.</h2>
    <hr class="gold-bar">
    <p class="lead">현재 관계의 흐름, 상대 심리, 내 행동 패턴을 함께 분석해<br>지금 해야 할 선택을 정리해드립니다.</p>
    <div class="gap-btns">
      <a href="apply.html" class="btn btn-navy btn-lg">1:1 상담 신청하기</a>
      <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao btn-lg">카카오톡으로 문의하기</a>
    </div>
  </div>
</section>`;

/* ─────────────────────────── about.html ─────────────────────────── */
const introParas = [
  `안녕하세요. 러브백 관계 연구소의 메릭 코치입니다. 7년간 6,500건이 넘는 연애와 이별, 재회 사연을 최전선에서 해부해 왔습니다. 찾아오시는 분들의 질문은 모두 다릅니다. 썸이 자꾸 흐지부지되는 분, 연애 중 연락 문제로 지친 분, 상대가 식은 것 같아 매일 불안한 분, 헤어진 사람의 마음을 어떻게 되돌릴 수 있을지 묻는 분. 그런데 수천 건의 사연을 듣다 보면 결국 한 지점에서 만나게 됩니다. <b>연애가 힘든 사람들은 사랑이 부족한 사람들이 아니었습니다.</b> 오히려 너무 많이 좋아하고, 너무 빨리 맞춰주고, 너무 오래 참고, 너무 뒤늦게 자신을 지키는 사람들이었습니다.`,
  `그래서 먼저 솔직하게 말씀드립니다. <b>저는 상대의 마음을 조종하는 법을 가르치지 않습니다. "재회시켜드립니다"라는 약속도 하지 않습니다.</b> 사람의 마음은 버튼처럼 조작할 수 있는 것이 아니고, 그런 약속이야말로 이 일에서 가장 무책임한 말이라고 생각하기 때문입니다.`,
  `저도 같은 자리에 있어봤습니다. 이별 통보를 받고 하루에도 수십 번 상대의 프로필을 들여다보던 시절, 지푸라기라도 잡는 심정으로 재회 상담이라는 것을 받아봤습니다. 지침은 정교했지만 저는 무너졌습니다. 그때 깨달았습니다. 지침이 틀린 게 아니라, 그 지침을 손에 쥔 제가 흔들리고 있었다는 것을요. 관계를 망치는 건 대부분 카톡 한 줄이 아니라, <b>그 한 줄을 보내기 전후로 흔들리는 나의 상태</b>였습니다.`,
  `그 답을 감이 아니라 구조로 찾고 싶어서 공부를 시작했습니다. 심리학과 애착이론에서 출발해 발달심리학, 행동경제학, 커뮤니케이션학, 그리고 사람을 가장 강하게 붙잡아두는 심리가 가장 적나라하게 드러나는 도박심리학과 범죄심리학까지 파고들었습니다. 심리상담사 1급을 비롯한 자격을 갖춘 것도 같은 이유에서였습니다. 힘들어하는 사람에게 "그냥 신경 쓰지 마세요", "밀당하세요" 같은 뻔한 말 대신, 왜 불안해지는지, 왜 같은 패턴이 반복되는지, 왜 사랑받고 싶은 마음이 오히려 사랑받기 어려운 행동으로 바뀌는지를 근거를 가지고 설명하고 싶었습니다.`,
  `6,500건의 상담이 가르쳐준 사실은 하나입니다. <b>사람은 자신을 잃어버린 사람에게 안정감을 느끼지 않습니다.</b> 그래서 연애에서 가장 위험한 순간은 상대를 너무 사랑하는 순간이 아니라, 상대를 잃을까 봐 나를 잃기 시작하는 순간입니다. 제가 하는 일은 상대를 내 뜻대로 움직이는 기술을 파는 것이 아니라, 관계 안에서 흔들리던 사람이 자기 자리를 되찾도록 돕는 일입니다. 내가 먼저 바로 서면 관계의 흐름이 달라지고, 상대가 나를 보는 시선도 달라집니다.`,
  `연애가 불안한 이유는 당신이 부족해서가 아닙니다. 아직 내 패턴을 제대로 본 적이 없기 때문입니다. 그리고 그 패턴은, 제대로 보면 바꿀 수 있습니다. 흔들리던 사람이 흔들리지 않는 사람으로 바뀌어 가는 과정, 그것만큼은 제가 끝까지 함께 하겠습니다.`,
];

const aboutBody = `
<section class="section section-white" style="padding-bottom:0">
  <div class="wrap-md center reveal">
    <span class="eyebrow">About Loveback</span>
    <h1 class="title">저는 상대의 마음을<br>조종하는 법을 가르치지 않습니다.</h1>
    <hr class="gold-bar">
    <p class="lead">7년, 6,500건의 사연이 가르쳐준 러브백의 방식</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div style="display:grid;gap:44px;align-items:start" class="about-grid">
      <div class="reveal">
        <!-- ── 코치 프로필 사진 ──
             아임웹에서: 아래 img의 src를 본인 사진 주소로 바꾸면 됩니다.
             (아임웹 편집기에서 이미지 업로드 → 주소 복사 → src에 붙여넣기) -->
        <div style="background:linear-gradient(165deg,#1b2542 0%,#22305a 100%);border-radius:10px;padding:34px 30px 30px;box-shadow:0 24px 60px rgba(29,39,67,.18);position:sticky;top:96px">
          <div style="border-radius:8px;overflow:hidden;aspect-ratio:4/4.4;background:linear-gradient(180deg,#25335e,#1b2542);display:flex;align-items:flex-end;justify-content:center">
            <img id="coachPhoto" src="coach.jpg" alt="메릭 코치"
              style="width:100%;height:100%;object-fit:cover"
              onerror="this.outerHTML='<svg viewBox=\\'0 0 200 220\\' style=\\'width:72%;opacity:.5\\' fill=\\'none\\'><circle cx=\\'100\\' cy=\\'74\\' r=\\'38\\' stroke=\\'#8fa0cc\\' stroke-width=\\'3\\'/><path d=\\'M30 210c8-46 38-70 70-70s62 24 70 70\\' stroke=\\'#8fa0cc\\' stroke-width=\\'3\\'/></svg>'">
          </div>
          <div style="text-align:center;margin-top:22px">
            <p class="serif" style="color:#f4f1e8;font-size:20px;letter-spacing:.04em">메릭 코치</p>
            <p style="color:#cbb489;font-size:12px;letter-spacing:.24em;margin-top:4px">LOVEBACK LAB DIRECTOR</p>
            <hr style="border:none;border-top:1px solid rgba(244,241,232,.16);margin:18px 0">
            <p style="color:rgba(244,241,232,.72);font-size:13.5px;line-height:1.9">누적 6,500건 이상 상담 분석<br>연애·이별·재회 케이스 연구 7년</p>
          </div>
        </div>
      </div>
      <div class="reveal reveal-d1" style="display:flex;flex-direction:column;gap:26px">
        ${introParas.map((p) => `<p style="font-size:16px;line-height:2.05;color:#39415e">${p}</p>`).join("\n")}
        <div style="border-left:3px solid #b2935b;background:#faf7f0;padding:24px 28px;border-radius:0 8px 8px 0">
          <p class="serif" style="font-size:17px;line-height:1.9;color:#1d2743">"연애를 잘한다는 건 상대를 더 잘 조종하는 것이 아닙니다.<br>관계 안에서 나를 잃지 않는 것입니다."</p>
        </div>
      </div>
    </div>
  </div>
</section>
<style>
@media(min-width:880px){.about-grid{grid-template-columns:340px 1fr}}
</style>

<section class="section section-cream">
  <div class="wrap-md center reveal">
    <h2 class="title">이런 분들이 찾아오시면 좋겠습니다</h2>
    <hr class="gold-bar">
  </div>
  <div class="wrap-md reveal reveal-d1" style="margin-top:34px">
    <div class="grid grid-2">
      ${[
        "썸이 자꾸 흐지부지 끝나는 분",
        "상대가 식은 것 같아 매일 불안한 분",
        "연애를 시작하면 늘 을이 되는 분",
        "연락 하나에 하루 기분이 무너지는 분",
        "서운함을 말하지 못하고 혼자 쌓아두는 분",
        "상대에게 맞추다 나 자신을 잃어버린 분",
        "다른 곳에서 상담받고도 안 됐던 분",
        "이번 관계만큼은 예전과 다르게 하고 싶은 분",
      ].map((t) => `<div class="card card-flat" style="display:flex;align-items:center;gap:13px;padding:19px 24px">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#b2935b" stroke-width="2.4" style="flex-shrink:0"><path d="M20 6L9 17l-5-5"/></svg>
        <span style="font-size:15px">${t}</span></div>`).join("\n")}
    </div>
  </div>
</section>

<section class="section section-navy">
  <div class="wrap-md center reveal">
    <p class="serif" style="font-size:clamp(18px,3vw,23px);line-height:1.9;color:#f4f1e8">흔들리던 사람이 흔들리지 않는 사람으로<br>바뀌어 가는 과정, 끝까지 함께 하겠습니다.</p>
    <div class="gap-btns" style="margin-top:10px">
      <a href="apply.html" class="btn btn-gold btn-lg">상담 신청하기</a>
      <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-line-light btn-lg">카카오톡으로 문의하기</a>
    </div>
  </div>
</section>`;

/* ─────────────────────────── programs.html ─────────────────────────── */
const steps = [
  ["사전 상담지 작성", "상담 전 현재 상황, 관계 흐름, 이별 원인, 대화 내용, 상대 반응 등을 작성합니다."],
  ["관계 흐름 분석", "단순히 사건만 보는 것이 아니라 관계가 어떤 단계에서 무너졌는지 분석합니다."],
  ["상대 심리 분석", "상대가 왜 멀어졌는지, 지금 어떤 감정 상태인지, 어떤 접근에 저항이 생기는지 봅니다."],
  ["내 패턴 진단", "내가 어떤 방식으로 관계를 밀거나 당겼는지, 불안·회피·집착·과잉배려 패턴이 있었는지 봅니다."],
  ["실행 전략 제시", "연락 여부와 시점, 메시지 방향, 대화 방식, 기다림의 기준, 관계 회복 루트를 정리합니다."],
  ["상담 후 정리", "핵심 방향과 실행 가이드를 정리해 혼자서도 다시 흐름을 잡을 수 있게 합니다."],
];

const fields = [
  {
    id: "dating", t: "연애 상담",
    who: "썸에서 관계가 애매해진 분 · 연애 중 상대가 식은 것 같은 분 · 불안형, 회피형 패턴으로 반복되는 분 · 연락, 표현, 서운함 문제로 자주 싸우는 분",
    q: "지금 관계가 어디서 꼬였는지, 어떤 순서로 풀어야 하는지 진단합니다.",
  },
  {
    id: "reunion", t: "재회 상담",
    who: "이별 후 연락 타이밍을 고민하는 분 · 차단/읽씹/무반응 상태인 분 · 마지막 연락을 어떻게 해야 할지 모르는 분 · 재회 가능성과 방향성을 알고 싶은 분",
    q: "재회는 감정으로 밀어붙이는 것이 아니라 상대의 심리적 저항을 낮추는 과정입니다.",
  },
  {
    id: "pattern", t: "관계 패턴 진단",
    who: "연애할 때마다 비슷하게 무너지는 분 · 항상 내가 더 불안해지는 분 · 상대에게 맞추다가 지치는 분 · 사랑받고 싶은데 오히려 매달리게 되는 분",
    q: "반복되는 연애 문제는 상대만의 문제가 아니라 내 관계 패턴에서 시작되는 경우가 많습니다.",
  },
];

const programsBody = `
<section class="section section-white" style="padding-bottom:56px">
  <div class="wrap-md center reveal">
    <span class="eyebrow">Programs</span>
    <h1 class="title">러브백 1:1 상담 프로그램</h1>
    <hr class="gold-bar">
    <p class="lead">상담은 감으로 진행되지 않습니다.<br>아래 6단계 흐름으로 관계를 구조적으로 분석합니다.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap-md" style="display:flex;flex-direction:column;gap:16px">
    ${steps.map(([t, d], i) => `<div class="card reveal" style="display:flex;gap:24px;align-items:flex-start;padding:26px 30px">
      <span class="serif" style="font-size:30px;color:#b2935b;line-height:1.2;min-width:52px">${String(i + 1).padStart(2, "0")}</span>
      <div><h3 style="font-size:17px;font-weight:700;margin-bottom:6px">Step ${i + 1}. ${t}</h3>
      <p style="color:#5a6380;font-size:15px">${d}</p></div></div>`).join("\n")}
  </div>
</section>

<section class="section section-cream">
  <div class="container center reveal">
    <span class="eyebrow">Fields</span>
    <h2 class="title">내 상황에 맞는 상담 분야</h2>
    <hr class="gold-bar">
  </div>
  <div class="container" style="margin-top:38px;display:flex;flex-direction:column;gap:22px">
    ${fields.map((f) => `<div id="${f.id}" class="card reveal" style="scroll-margin-top:90px;padding:34px 36px">
      <h3 class="title-sm" style="margin-bottom:14px">${f.t}</h3>
      <p style="font-size:12px;font-weight:700;letter-spacing:.18em;color:#b2935b;margin-bottom:8px">이런 분께 추천합니다</p>
      <p style="color:#5a6380;font-size:15px;line-height:1.95">${f.who}</p>
      <hr class="divider">
      <p style="font-weight:600;color:#8a6f3e;font-size:15px">${f.q}</p>
    </div>`).join("\n")}
  </div>
</section>

<section class="section section-navy">
  <div class="wrap-md center reveal">
    <h2 class="title">내게 맞는 상담과 비용이 궁금하다면</h2>
    <a href="pricing.html" class="btn btn-gold btn-lg" style="margin-top:8px">가격 안내 보기</a>
  </div>
</section>`;

/* ─────────────────────────── pricing.html ─────────────────────────── */
const plans = [
  {
    t: "연애/썸 관계 진단 상담", time: "60분", price: "197,000원",
    who: "현재 연애 중이거나 썸 단계에서 관계 흐름이 불안한 분",
    items: ["현재 관계 흐름 분석", "상대 심리 분석", "내 대화·태도 패턴 진단", "앞으로의 접근 전략 제시", "연락·만남·표현 방식 가이드"],
  },
  {
    t: "재회 전략 상담", time: "60분", price: "197,000원", featured: true,
    who: "이별 후 재회를 원하지만 연락 타이밍과 방향을 모르는 분",
    items: ["이별 원인 분석", "상대의 현재 심리 상태 분석", "재회 가능성 판단", "연락 타이밍·메시지 방향 설계", "하지 말아야 할 행동 정리", "상황별 대응 전략"],
  },
  {
    t: "프리미엄 관계 분석 상담", time: "90분", price: "269,000원",
    who: "단순 답변이 아니라 내 연애 패턴 자체를 깊게 바꾸고 싶은 분",
    items: ["전체 연애 패턴 분석", "애착 유형 기반 관계 진단", "반복되는 관계 문제 구조화", "상대 선택 기준 정리", "장기적인 관계 개선 전략", "상담 후 실행 가이드 제공"],
  },
];

const pricingBody = `
<section class="section section-white" style="padding-bottom:52px">
  <div class="wrap-md center reveal">
    <span class="eyebrow">Pricing</span>
    <h1 class="title">상담 프로그램 안내</h1>
    <hr class="gold-bar">
    <p class="lead">모든 상담은 사전 신청서 검토 후 1:1로 진행됩니다.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="grid grid-3" style="align-items:stretch">
      ${plans.map((p, i) => `<div class="card reveal reveal-d${i}" style="display:flex;flex-direction:column;padding:36px 32px;${p.featured ? "border:2px solid #b2935b;box-shadow:0 18px 50px rgba(178,147,91,.16)" : ""}">
        ${p.featured ? `<span class="chip-badge" style="background:#b2935b;color:#fff;align-self:flex-start;margin-bottom:16px">가장 많이 찾는 상담</span>` : `<span style="height:43px"></span>`}
        <h2 class="title-sm">${p.t}</h2>
        <p style="font-size:13.5px;color:#8a92a9;margin:10px 0 20px;line-height:1.8">${p.who}</p>
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:6px">
          <span class="serif" style="font-size:32px;font-weight:600;color:#1d2743">${p.price}</span>
          <span style="color:#8a92a9;font-size:14px">/ ${p.time}</span>
        </div>
        <hr class="divider">
        <ul class="list-plain" style="flex:1;color:#39415e;font-size:14.5px;line-height:2.15">
          ${p.items.map((it) => `<li style="display:flex;gap:10px"><span style="color:#b2935b">·</span>${it}</li>`).join("")}
        </ul>
        <a href="apply.html" class="btn ${p.featured ? "btn-gold" : "btn-navy"} btn-block" style="margin-top:24px">신청하기</a>
      </div>`).join("\n")}
    </div>
    <p class="reveal" style="text-align:center;margin-top:30px;color:#8a92a9;font-size:13.5px">결제 및 일정 안내는 신청서 확인 후 카카오톡으로 개별 안내드립니다.</p>
  </div>
</section>

<section class="section section-cream">
  <div class="wrap-md center reveal">
    <h2 class="title">어떤 상담이 맞을지 모르겠다면</h2>
    <hr class="gold-bar">
    <p class="lead">신청서에 현재 상황을 적어주시면, 코치가 확인 후<br>가장 적합한 프로그램을 안내해드립니다.</p>
    <div class="gap-btns">
      <a href="apply.html" class="btn btn-navy btn-lg">상담 상품 추천받기</a>
      <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao btn-lg">카카오톡으로 문의하기</a>
    </div>
  </div>
</section>`;

/* ─────────────────────────── reviews.html ─────────────────────────── */
const reviewsBody = `
<section class="section section-white" style="padding-bottom:48px">
  <div class="wrap-md center reveal">
    <span class="eyebrow">Reviews</span>
    <h1 class="title">상담 후기</h1>
    <hr class="gold-bar">
    <p class="lead">나와 비슷한 상황의 사람들이 상담을 통해<br>무엇이 달라졌는지 확인해보세요.</p>
    <div class="gap-btns">
      <button class="btn btn-navy" onclick="toggleWrite()">이곳에 후기 남기기</button>
      <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao">카카오톡으로 후기 보내기</a>
    </div>
  </div>
</section>

<section style="padding-bottom:84px">
  <div class="container">
    <div id="writeBox" style="display:none;max-width:620px;margin:0 auto 46px">
      <div class="card" style="padding:34px">
        <h3 class="title-sm" style="margin-bottom:6px;text-align:center">후기 작성</h3>
        <p style="text-align:center;color:#8a92a9;font-size:13px;margin-bottom:24px">작성하신 후기는 바로 아래 목록에 등록됩니다.</p>
        <form id="reviewForm">
          <div class="field"><label>상담 분야<span class="req">*</span></label>
            <select id="rCat" required>${reviewCats.map(([v, l]) => `<option value="${v}">${l}</option>`).join("")}</select></div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
            <div class="field"><label>닉네임<span class="req">*</span></label><input id="rNick" required maxlength="20" placeholder="예: 하늘달"></div>
            <div class="field"><label>간단 정보 (선택)</label><input id="rMeta" maxlength="30" placeholder="예: 20대 여성 · 이별 후 3주"></div>
          </div>
          <div class="field"><label>후기 제목<span class="req">*</span></label><input id="rTitle" required maxlength="80"></div>
          <div class="field"><label>후기 내용<span class="req">*</span></label>
            <textarea id="rContent" rows="5" required maxlength="2000" placeholder="상담 전 상황 → 가장 도움 됐던 부분 → 상담 후 달라진 점 순서로 적어주시면 좋아요."></textarea></div>
          <button type="submit" class="btn btn-navy btn-block">후기 등록하기</button>
        </form>
      </div>
    </div>

    <div class="chips reveal" id="rChips" style="justify-content:center;margin-bottom:36px">
      <button class="chip active" data-cat="all">전체</button>
      ${reviewCats.map(([v, l]) => `<button class="chip" data-cat="${v}">${l}</button>`).join("")}
    </div>

    <div class="grid grid-3" id="rGrid"></div>
    <p id="rEmpty" style="display:none;text-align:center;color:#8a92a9;padding:50px 0">해당 분야의 후기가 아직 없습니다.</p>
  </div>
</section>

<section class="section section-navy">
  <div class="wrap-md center reveal">
    <h2 class="title">지금 이 상황, 나만 겪는 게 아닙니다</h2>
    <hr class="gold-bar">
    <p class="lead-light">비슷한 상황에서 달라진 사람들처럼,<br>내 상황도 1:1 상담으로 정리해보세요.</p>
    <a href="apply.html" class="btn btn-gold btn-lg">상담 신청하기</a>
  </div>
</section>`;

const reviewsJs = `
var CATS = ${JSON.stringify(Object.fromEntries(reviewCats))};
var SEED = ${JSON.stringify(seedReviews)};
var LS_KEY = 'lb_reviews_v1';
function loadLocal(){ try{ return JSON.parse(localStorage.getItem(LS_KEY)||'[]'); }catch(e){ return []; } }
function saveLocal(a){ try{ localStorage.setItem(LS_KEY, JSON.stringify(a)); }catch(e){} }
function allReviews(){ return loadLocal().concat(SEED); }
function escHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
var curCat = 'all';
function render(){
  var grid = document.getElementById('rGrid');
  var list = allReviews().filter(function(r){ return curCat==='all' || r.cat===curCat; });
  document.getElementById('rEmpty').style.display = list.length ? 'none':'block';
  grid.innerHTML = list.map(function(r,i){
    return '<div class="card" style="background:#faf7f0;cursor:pointer" onclick="this.querySelector(\\'.r-body\\').classList.toggle(\\'r-open\\')">'
      + '<span class="chip-badge" style="margin-bottom:14px">'+ (CATS[r.cat]||'상담') +' 후기</span>'
      + (r.mine ? '<span class="chip-badge chip-badge-navy" style="margin-left:6px;margin-bottom:14px">내가 쓴 후기</span>' : '')
      + '<p class="serif" style="font-size:16.5px;line-height:1.7;margin-bottom:10px">“'+ escHtml(r.title) +'”</p>'
      + '<p class="r-body" style="font-size:14px;color:#5a6380;line-height:1.95;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden">'+ escHtml(r.content) +'</p>'
      + '<p style="margin-top:14px;font-size:12.5px;color:#9aa0b4">'+ escHtml(r.nick) + (r.meta? ' · '+escHtml(r.meta):'') +'</p>'
      + '<p style="margin-top:6px;font-size:12.5px;color:#b2935b;font-weight:600">눌러서 전체 보기</p>'
      + '</div>';
  }).join('');
}
var st = document.createElement('style'); st.textContent = '.r-open{display:block!important;-webkit-line-clamp:unset!important}'; document.head.appendChild(st);
document.getElementById('rChips').addEventListener('click', function(e){
  var b = e.target.closest('.chip'); if(!b) return;
  document.querySelectorAll('#rChips .chip').forEach(function(c){c.classList.remove('active')});
  b.classList.add('active'); curCat = b.dataset.cat; render();
});
function toggleWrite(){
  var w = document.getElementById('writeBox');
  w.style.display = w.style.display==='none' ? 'block':'none';
  if(w.style.display==='block') w.scrollIntoView({behavior:'smooth',block:'start'});
}
document.getElementById('reviewForm').addEventListener('submit', function(e){
  e.preventDefault();
  var r = { cat:document.getElementById('rCat').value, nick:document.getElementById('rNick').value.trim(),
    meta:document.getElementById('rMeta').value.trim(), title:document.getElementById('rTitle').value.trim(),
    content:document.getElementById('rContent').value.trim(), mine:true, ts:Date.now() };
  if(!r.nick||!r.title||!r.content) return;
  var arr = loadLocal(); arr.unshift(r); saveLocal(arr);
  e.target.reset(); document.getElementById('writeBox').style.display='none';
  curCat='all';
  document.querySelectorAll('#rChips .chip').forEach(function(c){c.classList.toggle('active', c.dataset.cat==='all')});
  render();
  alert('후기가 등록되었습니다. 소중한 후기 감사합니다!');
});
render();
`;

/* ─────────────────────────── columns.html ─────────────────────────── */
const columnsBody = `
<section class="section section-white" style="padding-bottom:48px">
  <div class="wrap-md center reveal">
    <span class="eyebrow">Column</span>
    <h1 class="title">러브백 칼럼</h1>
    <hr class="gold-bar">
    <p class="lead">연애, 재회, 카톡 대화, 관계 심리에 대한<br>러브백의 분석을 읽어보세요.</p>
  </div>
</section>

<div id="listView">
  <section style="padding-bottom:90px">
    <div class="container">
      <div class="chips reveal" id="cChips" style="justify-content:center;margin-bottom:36px">
        <button class="chip active" data-cat="all">전체</button>
        ${columnCats.map(([v, l]) => `<button class="chip" data-cat="${v}">${l}</button>`).join("")}
      </div>
      <div class="grid grid-3" id="cGrid"></div>
    </div>
  </section>
</div>

<div id="articleView" style="display:none">
  <section style="padding:56px 0 90px">
    <div class="wrap-md">
      <button class="btn btn-line btn-sm" onclick="closeArticle()" style="margin-bottom:34px">← 칼럼 목록으로</button>
      <span class="chip-badge" id="aCat"></span>
      <h1 class="title" id="aTitle" style="margin:18px 0 10px"></h1>
      <p id="aDate" style="color:#9aa0b4;font-size:13.5px;margin-bottom:36px"></p>
      <div id="aBody" style="display:flex;flex-direction:column;gap:24px;font-size:16px;line-height:2.05;color:#39415e"></div>
      <div style="margin-top:52px;border:1px solid #ece6d8;background:#faf7f0;border-radius:8px;padding:36px 30px;text-align:center">
        <p class="serif" style="font-size:18px;color:#1d2743;margin-bottom:10px">"내 상황도 여기에 해당되는 것 같다"는 생각이 드셨나요?</p>
        <p style="color:#5a6380;font-size:14.5px;line-height:1.9;max-width:440px;margin:0 auto 22px">관계는 상황마다 흐름이 다르고, 상대의 심리적 저항도 다릅니다.<br>혼자 연락 타이밍만 고민하지 마세요. 현재 관계의 흐름과 상대 심리,<br>내 행동 패턴을 함께 분석해 지금 해야 할 선택을 정리해드립니다.</p>
        <div class="gap-btns">
          <a href="apply.html" class="btn btn-navy">1:1 상담 신청하기</a>
          <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao">카카오톡 문의</a>
        </div>
      </div>
      <div style="text-align:center;margin-top:34px">
        <button class="btn btn-line btn-sm" onclick="closeArticle()">← 다른 칼럼 보기</button>
      </div>
    </div>
  </section>
</div>`;

const columnsJs = `
var CCATS = ${JSON.stringify(Object.fromEntries(columnCats))};
var COLS = ${JSON.stringify(columns.map((c) => ({ slug: c.slug, cat: c.cat, title: c.title, excerpt: c.excerpt, date: c.date, body: c.body })))};
var cCur = 'all';
function renderCols(){
  var g = document.getElementById('cGrid');
  g.innerHTML = COLS.filter(function(c){return cCur==='all'||c.cat===cCur}).map(function(c){
    return '<div class="card" style="cursor:pointer;display:flex;flex-direction:column" onclick="openArticle(\\''+c.slug+'\\')">'
      + '<span class="chip-badge" style="align-self:flex-start;margin-bottom:14px">'+CCATS[c.cat]+'</span>'
      + '<h3 class="serif" style="font-size:17.5px;line-height:1.6;font-weight:600;margin-bottom:8px">'+c.title+'</h3>'
      + '<p style="font-size:14px;color:#5a6380;flex:1">'+c.excerpt+'</p>'
      + '<p style="margin-top:16px;font-size:12.5px;color:#9aa0b4">'+c.date+' · <span style="color:#b2935b;font-weight:600">칼럼 읽기 →</span></p></div>';
  }).join('');
}
function openArticle(slug){
  var c = COLS.find(function(x){return x.slug===slug}); if(!c) return;
  document.getElementById('aCat').textContent = CCATS[c.cat];
  document.getElementById('aTitle').textContent = c.title;
  document.getElementById('aDate').textContent = c.date + ' · 러브백 관계 연구소';
  document.getElementById('aBody').innerHTML = c.body.map(function(p){return '<p>'+p+'</p>'}).join('');
  document.getElementById('listView').style.display='none';
  document.getElementById('articleView').style.display='block';
  try{ history.replaceState(null,'','#'+slug); }catch(e){}
  window.scrollTo({top:0,behavior:'instant'});
}
function closeArticle(){
  document.getElementById('articleView').style.display='none';
  document.getElementById('listView').style.display='block';
  try{ history.replaceState(null,'',location.pathname+location.search); }catch(e){}
  window.scrollTo({top:0,behavior:'instant'});
}
document.getElementById('cChips').addEventListener('click', function(e){
  var b = e.target.closest('.chip'); if(!b) return;
  document.querySelectorAll('#cChips .chip').forEach(function(c){c.classList.remove('active')});
  b.classList.add('active'); cCur = b.dataset.cat; renderCols();
});
renderCols();
if(location.hash){ openArticle(location.hash.slice(1)); }
`;

/* ─────────────────────────── diagnosis.html ─────────────────────────── */
const diagnosisBody = `
<section class="section section-white" style="padding-bottom:48px">
  <div class="wrap-md center reveal">
    <span class="eyebrow">Free Check</span>
    <h1 class="title">내 관계가 지금 회복 가능한<br>흐름인지 알고 싶다면?</h1>
    <hr class="gold-bar">
    <p class="lead">해당하는 항목을 모두 체크한 뒤 결과를 확인해보세요.</p>
  </div>
</section>

<section style="padding-bottom:90px">
  <div class="wrap-md">
    <div class="chips reveal" id="dTabs" style="justify-content:center;margin-bottom:36px"></div>
    <div id="dArea"></div>
  </div>
</section>

<section class="section section-cream">
  <div class="wrap-md center reveal">
    <h2 class="title">체크리스트는 시작일 뿐입니다</h2>
    <hr class="gold-bar">
    <p class="lead">정확한 진단은 관계의 흐름 전체를 봐야 가능합니다.<br>지금 상황을 1:1로 정리받아 보세요.</p>
    <div class="gap-btns">
      <a href="apply.html" class="btn btn-navy btn-lg">상담 신청하기</a>
      <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao btn-lg">카카오톡으로 문의하기</a>
    </div>
  </div>
</section>`;

const diagnosisJs = `
var DIAG = ${JSON.stringify(diagnoses)};
var dTabs = document.getElementById('dTabs');
var dArea = document.getElementById('dArea');
DIAG.forEach(function(d,i){
  var b = document.createElement('button');
  b.className = 'chip'+(i===0?' active':''); b.textContent = d.title;
  b.onclick = function(){
    document.querySelectorAll('#dTabs .chip').forEach(function(x){x.classList.remove('active')});
    b.classList.add('active'); renderQuiz(i);
  };
  dTabs.appendChild(b);
});
function renderQuiz(idx){
  var d = DIAG[idx];
  var html = '<p style="text-align:center;color:#5a6380;font-size:15px;margin-bottom:26px">'+d.desc+'</p><div id="qList">';
  d.questions.forEach(function(q,i){
    html += '<label style="display:flex;gap:14px;align-items:center;background:#fff;border:1px solid #ece6d8;border-radius:6px;padding:17px 22px;margin-bottom:10px;cursor:pointer;transition:border-color .2s" '
      + 'onmouseover="this.style.borderColor=\\'#b2935b\\'" onmouseout="this.style.borderColor=\\'#ece6d8\\'">'
      + '<input type="checkbox" style="width:17px;height:17px;accent-color:#b2935b;flex-shrink:0">'
      + '<span style="font-size:15px;color:#39415e">'+(i+1)+'. '+q+'</span></label>';
  });
  html += '</div><button class="btn btn-navy btn-lg btn-block" style="margin-top:18px" onclick="showResult('+idx+')">결과 확인하기</button>'
    + '<div id="dResult" style="display:none"></div>';
  dArea.innerHTML = html;
  window.scrollTo({top:dTabs.getBoundingClientRect().top+window.scrollY-110,behavior:'smooth'});
}
function showResult(idx){
  var d = DIAG[idx];
  var n = dArea.querySelectorAll('#qList input:checked').length;
  var band = d.bands.find(function(b){return n<=b.max}) || d.bands[d.bands.length-1];
  document.getElementById('qList').style.display='none';
  dArea.querySelector('button.btn-navy').style.display='none';
  var r = document.getElementById('dResult');
  r.style.display='block';
  r.innerHTML = '<div class="card" style="text-align:center;padding:44px 32px">'
    + '<p style="color:#9aa0b4;font-size:14px;margin-bottom:6px">체크한 항목</p>'
    + '<p class="serif" style="font-size:40px;color:#b2935b;margin-bottom:18px">'+n+'<span style="font-size:18px;color:#9aa0b4"> / '+d.questions.length+'</span></p>'
    + '<h3 class="serif" style="font-size:21px;line-height:1.6;margin-bottom:16px;color:#1d2743">'+band.title+'</h3>'
    + '<p style="color:#5a6380;font-size:15px;line-height:2;max-width:460px;margin:0 auto 26px">'+band.desc+'</p>'
    + '<div class="gap-btns">'
    + '<a href="apply.html" class="btn btn-navy btn-lg">'+band.cta+'</a>'
    + '<button class="btn btn-line" onclick="renderQuiz('+idx+')">다시 체크하기</button>'
    + '</div></div>';
  r.scrollIntoView({behavior:'smooth',block:'center'});
}
renderQuiz(0);
`;

/* ─────────────────────────── apply.html ─────────────────────────── */
const applyBody = `
<section class="section section-white" style="padding-bottom:48px">
  <div class="wrap-md center reveal">
    <span class="eyebrow">Apply</span>
    <h1 class="title">러브백 1:1 상담 신청</h1>
    <hr class="gold-bar">
    <p class="lead">아래 신청서를 작성하시면 내용이 자동으로 복사되고<br>카카오톡 채팅이 열립니다. 붙여넣어 보내주시면 코치가 확인 후 안내드립니다.</p>
  </div>
</section>

<section style="padding-bottom:56px">
  <div class="container">
    <div class="grid grid-3" style="max-width:900px;margin:0 auto">
      ${["신청서 작성 & 카톡 전송", "코치 확인 후 결제·일정 안내", "1:1 상담 진행 & 실행 정리"].map((t, i) => `
      <div class="card card-flat reveal reveal-d${i}" style="text-align:center;padding:24px 18px">
        <p class="serif" style="font-size:26px;color:#b2935b;margin-bottom:8px">${i + 1}</p>
        <p style="font-size:14.5px;font-weight:600">${t}</p>
      </div>`).join("\n")}
    </div>
  </div>
</section>

<section style="padding-bottom:90px">
  <div class="wrap-sm">
    <div class="card reveal" style="padding:38px 34px">
      <form id="applyForm">
        <div class="field"><label>상담 상품<span class="req">*</span></label>
          <select id="aProgram" required>
            <option value="">선택해주세요</option>
            <option>연애/썸 관계 진단 상담 (60분 · 197,000원)</option>
            <option>재회 전략 상담 (60분 · 197,000원)</option>
            <option>프리미엄 관계 분석 상담 (90분 · 269,000원)</option>
            <option>잘 모르겠어요 — 추천받고 싶어요</option>
          </select></div>
        <div class="field"><label>이름 또는 닉네임<span class="req">*</span></label><input id="aName" required maxlength="20"></div>
        <div class="field"><label>상담 희망 시간대 (선택)</label><input id="aTime" placeholder="예: 평일 저녁, 주말 오후"></div>
        <div class="field"><label>현재 상황<span class="req">*</span></label>
          <textarea id="aSituation" rows="6" required placeholder="관계 기간, 이별 시점, 갈등 원인, 마지막 대화, 현재 연락 상태, 상대의 반응 등을 적어주시면 상담에 큰 도움이 됩니다."></textarea></div>
        <div class="field"><label>상담을 통해 원하는 것 (선택)</label><textarea id="aGoal" rows="3"></textarea></div>
        <button type="submit" class="btn btn-navy btn-lg btn-block">신청 내용 복사하고 카카오톡 열기</button>
        <p style="text-align:center;font-size:13px;color:#8a92a9;margin-top:14px">버튼을 누르면 작성 내용이 복사됩니다.<br>열리는 카카오톡 채팅창에 붙여넣기만 해주세요.</p>
      </form>
    </div>
    <div class="center reveal" style="margin-top:30px">
      <p style="color:#5a6380;font-size:14.5px">신청서 작성 없이 먼저 문의하고 싶으시다면</p>
      <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao">카카오톡으로 바로 문의하기</a>
    </div>
  </div>
</section>`;

const applyJs = `
document.getElementById('applyForm').addEventListener('submit', function(e){
  e.preventDefault();
  var txt = '[러브백 상담 신청]\\n'
    + '· 상담 상품: ' + document.getElementById('aProgram').value + '\\n'
    + '· 이름/닉네임: ' + document.getElementById('aName').value + '\\n'
    + '· 희망 시간대: ' + (document.getElementById('aTime').value || '무관') + '\\n'
    + '· 현재 상황: ' + document.getElementById('aSituation').value + '\\n'
    + '· 원하는 것: ' + (document.getElementById('aGoal').value || '-');
  function openKakao(){ window.open('${KAKAO}','_blank'); }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(txt).then(function(){
      alert('신청 내용이 복사되었습니다!\\n카카오톡 채팅창에 붙여넣어 보내주세요.');
      openKakao();
    }).catch(function(){ fallback(); });
  } else { fallback(); }
  function fallback(){
    var ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta);
    ta.select(); try{ document.execCommand('copy'); }catch(e){}
    document.body.removeChild(ta);
    alert('신청 내용이 복사되었습니다!\\n카카오톡 채팅창에 붙여넣어 보내주세요.');
    openKakao();
  }
});
`;

/* ─────────────────────────── faq.html ─────────────────────────── */
const faqs = [
  ["재회 가능성을 정확히 알 수 있나요?", "재회 가능성은 단정할 수 없습니다. 다만 이별 과정, 상대의 반응, 현재 관계 상태, 마지막 연락 내용, 차단 여부, 감정 소모 정도를 바탕으로 현실적인 가능성과 방향을 분석해 드립니다."],
  ["상담받으면 무조건 재회할 수 있나요?", "무조건적인 결과를 약속하지 않습니다. 러브백은 결과를 보장하기보다, 현재 상황에서 가능성을 높이는 방향과 피해야 할 행동을 정리해 드립니다. 그것이 더 정직하고, 결과적으로 더 효과적인 방식이라고 믿습니다."],
  ["카톡 내용도 봐주시나요?", "네. 필요한 경우 실제 대화 흐름을 함께 보며 어떤 지점에서 상대가 부담을 느꼈는지, 어떤 메시지가 관계 흐름을 악화시켰는지 분석합니다."],
  ["상담 전에 무엇을 준비해야 하나요?", "관계 기간, 이별 시점, 갈등 원인, 마지막 대화, 현재 연락 상태, 상대의 반응, 본인의 목표를 정리해 주시면 좋습니다. 신청서 양식에 따라 작성하시면 자연스럽게 정리됩니다."],
  ["상담은 어떻게 진행되나요?", "사전 신청서를 바탕으로 전화 또는 온라인 방식으로 진행됩니다. 상담 방식은 프로그램별로 상세 안내드립니다."],
  ["환불은 가능한가요?", "상담 특성상 사전 분석이 시작된 이후에는 환불이 제한될 수 있습니다. 자세한 기준은 환불규정 페이지에서 확인하실 수 있으며, 신청 전 반드시 안내드립니다."],
];

const faqBody = `
<section class="section section-white" style="padding-bottom:48px">
  <div class="wrap-md center reveal">
    <span class="eyebrow">FAQ</span>
    <h1 class="title">자주 묻는 질문</h1>
    <hr class="gold-bar">
  </div>
</section>

<section style="padding-bottom:90px">
  <div class="wrap-md" id="faqList">
    ${faqs.map(([q, a], i) => `<div class="card card-flat reveal" style="padding:0;margin-bottom:12px;overflow:hidden">
      <button style="width:100%;display:flex;justify-content:space-between;align-items:center;gap:14px;background:none;border:none;padding:22px 26px;cursor:pointer;text-align:left" onclick="tgFaq(this)">
        <span style="font-size:15.5px;font-weight:600;color:#1d2743"><span style="color:#b2935b;margin-right:10px">Q</span>${q}</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9aa0b4" stroke-width="2" style="flex-shrink:0;transition:transform .25s"><path d="M6 9l6 6 6-6"/></svg>
      </button>
      <div class="fa" style="max-height:0;overflow:hidden;transition:max-height .3s ease">
        <p style="padding:0 26px 24px;color:#5a6380;font-size:14.5px;line-height:1.95">${a}</p>
      </div>
    </div>`).join("\n")}
  </div>
</section>

<section class="section section-cream">
  <div class="wrap-md center reveal">
    <p class="lead">더 궁금한 점은 카카오톡으로 편하게 물어보세요.</p>
    <div class="gap-btns">
      <a href="${KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao btn-lg">카카오톡으로 문의하기</a>
      <a href="apply.html" class="btn btn-navy btn-lg">상담 신청하기</a>
    </div>
  </div>
</section>`;

const faqJs = `
function tgFaq(btn){
  var item = btn.parentElement, fa = item.querySelector('.fa'), svg = btn.querySelector('svg');
  var open = fa.style.maxHeight && fa.style.maxHeight !== '0px';
  document.querySelectorAll('#faqList .fa').forEach(function(x){ x.style.maxHeight='0px'; });
  document.querySelectorAll('#faqList svg').forEach(function(x){ x.style.transform=''; });
  if(!open){ fa.style.maxHeight = fa.scrollHeight+'px'; svg.style.transform='rotate(180deg)'; }
}
var first = document.querySelector('#faqList button'); if(first) tgFaq(first);
`;

/* ─────────────────────────── policies ─────────────────────────── */
function policyPage(title, sections) {
  return `
<section class="section section-white" style="padding-bottom:40px">
  <div class="wrap-md center reveal">
    <h1 class="title">${title}</h1>
    <p style="color:#9aa0b4;font-size:13px">시행일: 2026.01.01</p>
  </div>
</section>
<section style="padding-bottom:90px">
  <div class="wrap-md reveal">
    ${sections.map(([h, ...ps]) => `<h2 style="font-size:16.5px;font-weight:700;margin:30px 0 10px">${h}</h2>${ps.map((p) => `<p style="color:#5a6380;font-size:14.5px;line-height:2">${p}</p>`).join("")}`).join("\n")}
    <div style="margin-top:44px"><a href="index.html" class="btn btn-line">홈으로 돌아가기</a></div>
  </div>
</section>`;
}

const termsSections = [
  ["제1조 (목적)", "본 약관은 러브백 관계 연구소(이하 \"회사\")가 제공하는 관계 코칭 상담 서비스(이하 \"서비스\")의 이용조건 및 절차, 이용자와 회사의 권리·의무 및 책임사항을 규정함을 목적으로 합니다."],
  ["제2조 (서비스의 성격)", "회사가 제공하는 서비스는 연애, 이별, 재회 상황에 대한 관계 코칭 및 커뮤니케이션 전략 자문이며, 의료법상 심리치료 또는 정신과적 진단·치료 행위가 아닙니다.", "서비스는 이용자가 제공한 정보를 바탕으로 한 분석과 제안이며, 상담 결과(재회, 관계 개선 등)를 보장하지 않습니다."],
  ["제3조 (이용계약의 성립)", "이용계약은 이용자가 상담 신청서를 작성하고 회사가 안내하는 절차에 따라 결제를 완료함으로써 성립합니다."],
  ["제4조 (회사의 의무)", "회사는 이용자가 제공한 정보를 상담 목적 외로 사용하지 않으며, 관련 법령에 따라 개인정보를 안전하게 관리합니다."],
  ["제5조 (이용자의 의무)", "이용자는 상담 진행을 위해 필요한 정보를 사실에 근거하여 제공해야 하며, 허위 정보 제공으로 인한 불이익은 이용자 본인에게 있습니다."],
  ["제6조 (환불)", "환불 절차 및 기준은 별도의 환불규정 페이지를 따릅니다."],
];

const privacySections = [
  ["1. 수집하는 개인정보 항목", "회사는 상담 신청 및 후기 작성을 위해 다음 정보를 수집합니다.", "· 상담 신청: 이름 또는 닉네임, 연락 수단, 상담 희망 시간대, 이용자가 직접 작성한 상황 및 대화 내용<br>· 후기 작성: 닉네임, 간단 정보(선택), 후기 내용"],
  ["2. 수집 및 이용 목적", "수집한 정보는 상담 신청 확인 및 안내, 상담 진행, 후기 게시판 운영, 서비스 개선 목적으로만 이용하며, 명시한 목적 외의 용도로 사용하지 않습니다."],
  ["3. 보유 및 이용 기간", "상담 신청 정보는 상담 종료 후 관련 법령에 따른 보관 의무 기간 동안 보관 후 파기하며, 후기 게시글은 이용자가 삭제를 요청하기 전까지 보관됩니다."],
  ["4. 제3자 제공", "회사는 이용자의 동의 없이 개인정보를 제3자에게 제공하지 않습니다."],
  ["5. 이용자의 권리", "이용자는 언제든지 본인의 개인정보 열람, 정정, 삭제를 요청할 수 있습니다. 문의는 카카오톡 채널을 통해 접수해주시기 바랍니다."],
  ["6. 문의처", "카카오톡 채널: 러브백 관계 연구소 · 담당: 메릭 코치"],
];

const refundSections = [
  ["1. 상담 전 환불", "결제 완료 후 상담을 위한 사전 분석(신청서 검토, 자료 분석 등)이 시작되기 전까지는 결제 금액의 전액 환불이 가능합니다."],
  ["2. 사전 분석 시작 후 환불", "코치가 상담 신청서를 바탕으로 사전 분석을 시작한 이후에는, 이미 투입된 분석 시간에 대한 비용을 제외하고 부분 환불이 진행됩니다."],
  ["3. 상담 진행 후 환불", "1:1 상담이 완료된 이후에는 서비스 제공이 완료된 것으로 보아 환불이 제한됩니다."],
  ["4. 상담 일정 변경", "상담 일정은 예정일 기준 24시간 전까지 1회에 한해 무료로 변경 가능합니다."],
  ["5. 환불 절차", "환불을 원하실 경우 카카오톡 채널로 결제 내역과 함께 요청해주시면, 확인 후 영업일 기준 3~5일 이내 처리됩니다."],
];

/* ─────────────────────────── write files ─────────────────────────── */
const pages = [
  ["index.html", { title: "러브백 관계 연구소 | 연락을 고민하기 전에, 관계의 흐름부터", desc: "누적 6,500건 이상의 연애·재회 상담 분석. 관계 패턴과 상대 심리로 지금 해야 할 선택을 정리해드립니다.", active: "", body: indexBody }],
  ["about.html", { title: "러브백 소개 | 러브백 관계 연구소", active: "about.html", body: aboutBody }],
  ["programs.html", { title: "상담 프로그램 | 러브백 관계 연구소", active: "programs.html", body: programsBody }],
  ["pricing.html", { title: "가격 안내 | 러브백 관계 연구소", active: "pricing.html", body: pricingBody }],
  ["reviews.html", { title: "상담 후기 | 러브백 관계 연구소", active: "reviews.html", body: reviewsBody, extraJs: reviewsJs }],
  ["columns.html", { title: "칼럼 | 러브백 관계 연구소", active: "columns.html", body: columnsBody, extraJs: columnsJs }],
  ["diagnosis.html", { title: "무료 진단 | 러브백 관계 연구소", active: "diagnosis.html", body: diagnosisBody, extraJs: diagnosisJs }],
  ["apply.html", { title: "상담 신청 | 러브백 관계 연구소", active: "", body: applyBody, extraJs: applyJs }],
  ["faq.html", { title: "FAQ | 러브백 관계 연구소", active: "faq.html", body: faqBody, extraJs: faqJs }],
  ["policy-terms.html", { title: "이용약관 | 러브백 관계 연구소", active: "", body: policyPage("이용약관", termsSections) }],
  ["policy-privacy.html", { title: "개인정보처리방침 | 러브백 관계 연구소", active: "", body: policyPage("개인정보처리방침", privacySections) }],
  ["policy-refund.html", { title: "환불규정 | 러브백 관계 연구소", active: "", body: policyPage("환불규정", refundSections) }],
];

for (const [file, opts] of pages) {
  writeFileSync(OUT + file, shell(opts));
  console.log("built", file);
}
