const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");
const { applyTheme } = require("/root/.claude/skills/synced/6a42ce02-25b2-4315-b192-f10679d67521_6d8e57bc-6871-47bd-afb1-85283a5fdc5f/pptx/scripts/apply_theme.js");

const HEAD = "에스코어 드림 6 Bold";
const BODY = "에스코어 드림 4 Regular";
const HEX = {
  navy: "142340", navy2: "23365E", ink: "0D182E", gold: "C9A24B", goldLt: "EBDDB3",
  bg: "F4F6FA", white: "FFFFFF", mute: "586379", line: "D9DEE8", red: "D6453D", redLt: "FBE9E7", slate: "B8C2D4",
};
const THEME = {
  name: "이다사 OT",
  headFontFace: HEAD,
  bodyFontFace: BODY,
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.navy, lt2: HEX.bg,
    accent1: HEX.gold, accent2: HEX.navy2, accent3: HEX.red, accent4: HEX.slate,
    accent5: HEX.mute, accent6: HEX.goldLt, hlink: HEX.navy2, folHlink: HEX.mute,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "이다사 12주 태도 코칭 OT";
pres.author = "이다사";
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
const C = pres.SchemeColor;
const W = 13.333;

// ---------- layouts ----------
const footer = (dark) => [
  { text: { text: "이다사 · 12주 태도 코칭", options: { x: 0.7, y: 6.95, w: 5, h: 0.3, fontSize: 10, color: dark ? C.accent4 : C.accent5, margin: 0 } } },
];
pres.defineSlideMaster({
  title: "LIGHT",
  background: { color: HEX.bg },
  objects: [
    ...footer(false),
    { placeholder: { options: { name: "eyebrow", type: "body", x: 0.7, y: 0.5, w: 11.9, h: 0.35, fontSize: 14, bold: true, color: C.accent1, fontFace: HEAD, margin: 0, valign: "middle", align: "left" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 0.85, w: 11.9, h: 0.8, fontSize: 32, bold: true, color: C.text2, fontFace: HEAD, margin: 0, valign: "middle", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.1, y: 6.95, w: 0.5, h: 0.3, fontSize: 10, color: C.accent5, align: "right" },
});
pres.defineSlideMaster({
  title: "DARK",
  background: { color: HEX.navy },
  objects: [
    ...footer(true),
    { placeholder: { options: { name: "eyebrow", type: "body", x: 0.7, y: 0.5, w: 11.9, h: 0.35, fontSize: 14, bold: true, color: C.accent1, fontFace: HEAD, margin: 0, valign: "middle", align: "left" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 0.85, w: 11.9, h: 0.8, fontSize: 32, bold: true, color: C.background1, fontFace: HEAD, margin: 0, valign: "middle", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.1, y: 6.95, w: 0.5, h: 0.3, fontSize: 10, color: C.accent4, align: "right" },
});
pres.defineSlideMaster({ title: "COVER", background: { color: HEX.ink }, objects: [] });

// ---------- helpers ----------
const iconCache = {};
async function icon(name, hex, size = 256) {
  const k = name + hex;
  if (iconCache[k]) return iconCache[k];
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(lu[name], { color: "#" + hex, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).resize(size, size).png().toBuffer();
  return (iconCache[k] = "image/png;base64," + buf.toString("base64"));
}
const sh = () => ({ type: "outer", color: "1E2A44", opacity: 0.1, blur: 10, offset: 2, angle: 90 });
let section = "";
function newSlide(master, eyebrow, title, notes) {
  const s = pres.addSlide({ masterName: master, sectionTitle: section });
  if (eyebrow) s.addText(eyebrow, { placeholder: "eyebrow" });
  if (title) s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}
function sec(t) { section = t; pres.addSection({ title: t }); }
function card(s, x, y, w, h, fill = C.background1, name = "card") {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, rectRadius: 0.12, line: { type: "none" }, shadow: sh(), objectName: name });
}
async function iconCircle(s, x, y, d, name, bg, fg) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
  const p = d * 0.26;
  s.addImage({ data: await icon(name, fg), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, altText: name });
}
const T = (s, text, o) => s.addText(text, { isTextBox: true, margin: 0, fontFace: BODY, color: C.text1, fontSize: 16, valign: "top", ...o });
// slot the user replaces with their own proof (photo / capture / number)
async function slot(s, x, y, w, h, label, dark = false) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.1, fill: { color: dark ? HEX.navy2 : "E9EDF4" },
    line: { color: dark ? HEX.slate : "A9B3C6", width: 1.25, dashType: "dash" }, objectName: "교체용 슬롯",
  });
  const d = Math.min(0.5, h * 0.3);
  s.addImage({ data: await icon("LuImage", dark ? HEX.slate : HEX.mute), x: x + w / 2 - d / 2, y: y + h / 2 - d - 0.05, w: d, h: d });
  T(s, label, { x: x + 0.15, y: y + h / 2 + 0.05, w: w - 0.3, h: 0.5, fontSize: 11, align: "center", color: dark ? C.accent4 : C.accent5 });
}
function chip(s, x, y, w, text, fill = C.accent1, color = C.text2) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.36, rectRadius: 0.18, fill: { color: fill }, line: { type: "none" } });
  T(s, text, { x, y, w, h: 0.36, fontSize: 12, bold: true, align: "center", valign: "middle", color, fontFace: HEAD });
}

// curriculum side panel used on the 4 step slides (mentor's "고파사 프로세스" nav)
const STEPS = ["[준비] 진단 · 12주 계획", "[1단계] 나를 세운다", "[2단계] 끌어당긴다", "[3단계] 실전에서 쓴다"];
async function stepNav(s, active) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 4.1, h: 7.5, fill: { color: C.text2 }, line: { type: "none" }, objectName: "커리큘럼 내비" });
  T(s, "이다사 12주 프로세스", { x: 0.6, y: 0.6, w: 3.2, h: 0.4, fontSize: 15, bold: true, color: C.accent1, fontFace: HEAD });
  STEPS.forEach((t, i) => {
    const y = 1.45 + i * 0.8;
    const on = i === active;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.45, y, w: 3.25, h: 0.6, rectRadius: 0.1, fill: { color: on ? HEX.gold : HEX.navy2 }, line: { type: "none" } });
    T(s, t, { x: 0.7, y, w: 2.95, h: 0.6, fontSize: 15, bold: on, valign: "middle", color: on ? C.text2 : C.accent4, fontFace: on ? HEAD : BODY });
  });
}

(async () => {
  // ===================== 1. 훅 =====================
  sec("훅 · 신뢰");
  {
    const s = pres.addSlide({ masterName: "COVER", sectionTitle: section });
    s.addImage({ data: await icon("LuCompass", HEX.navy2), x: 8.4, y: 1.0, w: 5.6, h: 5.6, transparency: 30 });
    T(s, "이다사 · 12주 태도 코칭 오리엔테이션", { x: 0.8, y: 1.0, w: 8, h: 0.4, fontSize: 15, bold: true, color: C.accent1, fontFace: HEAD });
    T(s, "소개팅에서 말은 잘 이어가는데,\n두 번째 만남은 안 잡히나요?", { x: 0.8, y: 1.9, w: 9.5, h: 2.2, fontSize: 44, bold: true, color: C.background1, fontFace: HEAD, lineSpacingMultiple: 1.1 });
    T(s, "이 영상을 끝까지 보시면, 더 이상 ‘소개팅 멘트’를 검색하지 않으셔도 됩니다.", { x: 0.8, y: 4.45, w: 9.5, h: 0.5, fontSize: 18, color: C.accent4 });
    chip(s, 0.8, 5.5, 2.6, "멘트가 아니라, 반응을 바꿉니다");
    s.addNotes("[훅 · 멘토 0:00~0:03 구조] 좋아하는 여자 앞에서만 말이 많아지고, 대화는 이어지는데 두 번째 만남은 안 잡히시나요? 이 영상 끝까지 보시면 더 이상 소개팅 멘트를 검색하지 않으셔도 됩니다.");
  }

  // ===================== 2. 실적 증거 =====================
  {
    const s = newSlide("LIGHT", "먼저 결과부터 보여드리겠습니다", "멘트를 외우지 않고, 반응을 바꾼 결과입니다",
      "[실적 증거 · 멘토 0:03~0:16 구조] 멘토는 '광고비 2만 원 → 매출 2,700만 원'처럼 숫자로 시작합니다. 여기에는 실제 수강생 결과 숫자 3개를 넣으세요. 예: 12주 안에 두 번째 만남 성공 비율, 6주 영상 비교에서 해명 시간이 줄어든 비율, 수강 중 연애 시작 인원. 확인된 숫자만 쓰고, 개인 동의를 받으세요.");
    const stats = [["LuCalendarHeart", "00%", "12주 안에\n두 번째 만남을 직접 제안"], ["LuTimer", "−00초", "평가받는 순간\n해명하는 시간 감소"], ["LuHeartHandshake", "00명", "수강 중\n연애를 시작한 수강생"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.7 + i * 4.05;
      card(s, x, 2.05, 3.75, 3.9);
      await iconCircle(s, x + 0.4, 2.4, 0.75, stats[i][0], HEX.navy, HEX.gold);
      T(s, stats[i][1], { x: x + 0.4, y: 3.4, w: 3.0, h: 1.0, fontSize: 48, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
      T(s, stats[i][2], { x: x + 0.4, y: 4.55, w: 3.0, h: 0.9, fontSize: 16, color: C.accent5 });
      T(s, "실제 수치로 교체", { x: x + 0.4, y: 5.45, w: 3.0, h: 0.3, fontSize: 10, color: C.accent3, bold: true });
    }
    T(s, "새벽까지 멘트를 검색하는 대신, 진단 → 12주 훈련으로 실제 반응을 바꾼 분들의 기록입니다", { x: 0.7, y: 6.25, w: 11.9, h: 0.4, fontSize: 14, color: C.accent5 });
  }

  // ===================== 3. 나는 누구인가 =====================
  {
    const s = newSlide("LIGHT", "이런 말을 하는 저는 누구일까요?", "남자들의 ‘긴장한 순간’만 봐 온 사람입니다",
      "[신뢰 · 멘토 0:16~0:41 구조] 멘토는 경력 7년, 플랫폼 1위, 최고 멘토 3회 선정처럼 객관적인 기록을 빠르게 나열합니다. 내 경력·상담 건수·플랫폼 기록·언론/출간 등을 숫자로 넣으세요. 오른쪽에는 상담 현장 사진이나 프로필 사진을 넣습니다.");
    const rows = [["LuMessagesSquare", "1:1 상담 0,000건", "소개팅 · 연애 고민 직접 상담"], ["LuVideo", "녹화 복기 000시간", "말투 · 표정 · 시선을 장면 단위로 분석"], ["LuTrophy", "[플랫폼 · 수상 기록]", "객관적으로 확인 가능한 기록"], ["LuBookOpen", "[콘텐츠 · 출간 기록]", "유튜브 · 칼럼 · 강의"]];
    for (let i = 0; i < rows.length; i++) {
      const y = 2.05 + i * 1.12;
      await iconCircle(s, 0.7, y, 0.8, rows[i][0], HEX.navy, HEX.gold);
      T(s, rows[i][1], { x: 1.75, y: y + 0.02, w: 5.6, h: 0.42, fontSize: 22, bold: true, color: C.text2, fontFace: HEAD });
      T(s, rows[i][2], { x: 1.75, y: y + 0.46, w: 5.6, h: 0.35, fontSize: 14, color: C.accent5 });
    }
    await slot(s, 7.8, 2.05, 4.8, 4.3, "프로필 · 상담 현장 사진");
  }

  // ===================== 4. 수강생 성과 =====================
  {
    const s = newSlide("LIGHT", "수강생들의 변화", "같은 질문, 같은 조건으로 찍은 영상이 증명합니다",
      "[수강생 성과 · 멘토 0:41~0:52 구조] 멘토는 '비포 애프터 성과'를 화면 가득 보여줍니다. 이다사는 0주·6주·12주 같은 질문 영상이 가장 강력한 증거입니다. 동의받은 수강생의 전후 캡처(얼굴 가림)를 넣고, 아래 한 줄에 무엇이 달라졌는지 적으세요.");
    const cols = [["0주", "출발점", "평가받자 해명이 40초"], ["6주", "중간 점검", "2초 멈추고 내 기준 말하기"], ["12주", "최종 비교", "웃으면서 다음 만남 제안"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.7 + i * 4.05;
      await slot(s, x, 2.05, 3.75, 2.6, "수강생 영상 캡처 (얼굴 가림)");
      T(s, cols[i][0], { x, y: 4.85, w: 1.2, h: 0.5, fontSize: 26, bold: true, color: i === 2 ? C.accent1 : C.text2, fontFace: HEAD });
      T(s, cols[i][1], { x: x + 1.2, y: 4.93, w: 2.5, h: 0.4, fontSize: 14, color: C.accent5 });
      T(s, cols[i][2], { x, y: 5.45, w: 3.75, h: 0.4, fontSize: 15, color: C.text1 });
    }
    T(s, "예시 문구입니다 · 결과는 실행에 따라 다르며 연애 결과를 보장하지 않습니다", { x: 0.7, y: 6.3, w: 11.9, h: 0.35, fontSize: 11, color: C.accent5 });
  }

  // ===================== 5. 감사 후기 =====================
  {
    const s = newSlide("LIGHT", "지금도 도착하는 메시지", "결과가 없었다면, 이런 연락은 오지 않았겠죠",
      "[감사 인사 · 멘토 0:52~1:02 구조] 멘토는 상패·식사 대접 사진으로 '성과가 없었다면 불가능한 일'이라고 말합니다. 수강생 카톡·후기 캡처 4~6장을 넣으세요(이름·프로필 가림).");
    for (let i = 0; i < 4; i++) await slot(s, 0.7 + i * 3.04, 2.05, 2.8, 3.7, "후기 · 카톡 캡처");
    s.addImage({ data: await icon("LuQuote", HEX.gold), x: 0.7, y: 6.0, w: 0.4, h: 0.4 });
    T(s, "“토요일에 같이 가자고 제가 먼저 말했어요. 예전 같으면 상상도 못 했을 거예요.”", { x: 1.25, y: 6.0, w: 11.3, h: 0.45, fontSize: 16, italic: true, color: C.text2, valign: "middle" });
  }

  // ===================== 6. 이다사 정의 =====================
  sec("문제 · 해법");
  {
    const s = newSlide("DARK", "이다사 12주 태도 코칭이란", "진단에서 찾은 내 반응을, 12주 1:1로 바꾸는 과정",
      "[멤버십 정의 · 멘토 1:02~1:08 구조] '고가 상품 파는 사람들, 줄여서 고파사'처럼 이름과 정체를 한 문장으로 정의합니다. 이다사 12주 태도 코칭은 수많은 상담 경험과 녹화 복기 사례를 바탕으로 만든 1:1 태도 훈련 과정입니다. PDF를 받고 영상만 보는 강의가 아닙니다.");
    const items = [["LuStethoscope", "진단", "90분 시뮬레이션으로\n내 반응을 확인"], ["LuUserCheck", "1:1 훈련", "역할극 · 녹화 · 교정을\n12주 동안 반복"], ["LuInfinity", "평생 점검", "썸 · 연애 · 결혼 고민까지\n졸업 후에도 계속"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.7 + i * 4.05;
      card(s, x, 2.15, 3.75, 3.6, C.accent2);
      await iconCircle(s, x + 0.4, 2.5, 0.85, items[i][0], HEX.gold, HEX.navy);
      T(s, items[i][1], { x: x + 0.4, y: 3.6, w: 3.0, h: 0.55, fontSize: 26, bold: true, color: C.background1, fontFace: HEAD });
      T(s, items[i][2], { x: x + 0.4, y: 4.3, w: 3.0, h: 1.0, fontSize: 16, color: C.accent4 });
    }
    T(s, "외운 멘트는 긴장하면 사라지지만, 훈련한 반응은 남습니다", { x: 0.7, y: 6.1, w: 11.9, h: 0.45, fontSize: 18, bold: true, color: C.accent1, fontFace: HEAD });
  }

  // ===================== 7. 핵심 깨달음 =====================
  {
    const s = newSlide("LIGHT", "수많은 상담 끝에 깨달은 진실", null,
      "[핵심 깨달음 · 멘토 1:08~1:16 구조] 멘토: '초보일수록 고가 상품을 팔아야 한다'. 이다사: 연애가 서툰 사람일수록 멘트를 더 외울 게 아니라, 긴장한 순간의 반응을 바꿔야 합니다. 멘트 100개를 외우는 것보다 평가받는 순간 2초 멈추는 반응 하나가 훨씬 쉽고 현실적이기 때문입니다.");
    T(s, "연애가 서툴수록,\n멘트가 아니라 ‘반응’을 바꿔야 합니다", { x: 0.7, y: 1.6, w: 11.9, h: 2.0, fontSize: 40, bold: true, color: C.text2, fontFace: HEAD, align: "center", valign: "middle", lineSpacingMultiple: 1.1 });
    card(s, 1.9, 4.1, 4.3, 2.2);
    T(s, "멘트 100개 외우기", { x: 2.2, y: 4.35, w: 3.7, h: 0.5, fontSize: 20, bold: true, color: C.accent5, fontFace: HEAD, align: "center" });
    T(s, "긴장하는 순간\n전부 사라짐", { x: 2.2, y: 5.0, w: 3.7, h: 1.0, fontSize: 16, color: C.accent3, align: "center" });
    T(s, "<", { x: 6.2, y: 4.7, w: 0.9, h: 0.9, fontSize: 40, bold: true, color: C.accent1, align: "center", valign: "middle" });
    card(s, 7.1, 4.1, 4.3, 2.2, C.text2);
    T(s, "반응 하나 바꾸기", { x: 7.4, y: 4.35, w: 3.7, h: 0.5, fontSize: 20, bold: true, color: C.accent1, fontFace: HEAD, align: "center" });
    T(s, "평가받아도 2초 멈추고\n내 기준을 말한다", { x: 7.4, y: 5.0, w: 3.7, h: 1.0, fontSize: 16, color: C.background1, align: "center" });
  }

  // ===================== 8. 잘못된 대안 =====================
  {
    const s = newSlide("LIGHT", "요즘 넘쳐나는 연애 강의들", "‘이 멘트만 쓰면 된다’는 말, 왜 실전에서는 안 될까요?",
      "[적 · 멘토 1:16~1:39 구조] 멘토는 'AI로 1시간 만에 수익' 강의를 반례로 들고, 플랫폼 정책 하나에 무너진다고 말합니다. 이다사는 멘트 모음·픽업 기술·유튜브 꿀팁을 반례로 듭니다. 상대가 바뀌거나 상황이 조금만 달라져도 외운 멘트는 쓸 수 없습니다. 그래서 오래 연애하려면 상황이 바뀌어도 남는 나만의 태도가 필요합니다.");
    const bads = [["LuMessageSquareText", "멘트 모음 · 카톡 답장 템플릿", "상대 반응이 대본과 다르면\n다음 말이 막힙니다"], ["LuFlame", "픽업 · 밀당 기술", "연기는 오래 못 갑니다\n관계가 시작돼도 불안합니다"], ["LuYoutube", "유튜브 꿀팁 시청", "보는 순간엔 알 것 같지만\n긴장하면 몸이 안 따라옵니다"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.7 + i * 4.05;
      card(s, x, 2.05, 3.75, 3.3);
      await iconCircle(s, x + 0.4, 2.4, 0.75, bads[i][0], HEX.redLt, HEX.red);
      s.addImage({ data: await icon("LuX", HEX.red), x: x + 3.0, y: 2.45, w: 0.45, h: 0.45 });
      T(s, bads[i][1], { x: x + 0.4, y: 3.4, w: 3.1, h: 0.45, fontSize: 18, bold: true, color: C.text2, fontFace: HEAD });
      T(s, bads[i][2], { x: x + 0.4, y: 4.0, w: 3.1, h: 1.0, fontSize: 15, color: C.accent5 });
    }
    card(s, 0.7, 5.65, 11.85, 0.9, C.text2);
    T(s, "상황이 바뀌어도 남는 건 단 하나, 긴장한 순간에도 무너지지 않는 ‘내 태도’입니다", { x: 1.0, y: 5.65, w: 11.3, h: 0.9, fontSize: 18, bold: true, color: C.background1, valign: "middle", fontFace: HEAD });
  }

  // ===================== 9. 커리큘럼 개요 =====================
  sec("커리큘럼");
  {
    const s = newSlide("LIGHT", "이다사 12주 프로세스", "준비 단계와 3단계 훈련으로 진행됩니다",
      "[커리큘럼 개요 · 멘토 1:40~1:43 구조] 멘토는 '준비 + 3단계'를 한 화면에 보여준 뒤 하나씩 강조합니다. 이다사: 준비 단계에서 진단과 12주 계획을 받고, 1단계 나를 세운다(1~4주), 2단계 끌어당긴다(5~8주), 3단계 실전에서 쓴다(9~12주)로 진행합니다.");
    const blocks = [["LuStethoscope", "준비", "진단 · 계획", "90분 시뮬레이션\n고칠 순서 정하기"], ["LuAnchor", "1단계 · 1~4주", "나를 세운다", "흔들리지 않는 기준\n평가받아도 해명 X"], ["LuMagnet", "2단계 · 5~8주", "끌어당긴다", "끌려다니지 않기\n먼저 제안하기"], ["LuCoffee", "3단계 · 9~12주", "실전에서 쓴다", "실제 만남 적용\n관계 안에서 나를 지키기"]];
    for (let i = 0; i < 4; i++) {
      const x = 0.7 + i * 3.04;
      card(s, x, 2.05, 2.8, 4.2, i === 0 ? C.text2 : C.background1);
      await iconCircle(s, x + 0.3, 2.35, 0.75, blocks[i][0], i === 0 ? HEX.gold : HEX.navy, i === 0 ? HEX.navy : HEX.gold);
      T(s, blocks[i][1], { x: x + 0.3, y: 3.3, w: 2.3, h: 0.35, fontSize: 13, bold: true, color: C.accent1, fontFace: HEAD });
      T(s, blocks[i][2], { x: x + 0.3, y: 3.7, w: 2.3, h: 0.5, fontSize: 22, bold: true, color: i === 0 ? C.background1 : C.text2, fontFace: HEAD });
      T(s, blocks[i][3], { x: x + 0.3, y: 4.4, w: 2.3, h: 1.2, fontSize: 15, color: i === 0 ? C.accent4 : C.accent5 });
      if (i < 3) s.addImage({ data: await icon("LuArrowRight", HEX.slate), x: x + 2.82, y: 4.0, w: 0.2, h: 0.2 });
    }
    T(s, "6주 · 12주차에 0주 영상과 같은 조건으로 다시 찍어 비교합니다", { x: 0.7, y: 6.45, w: 11.9, h: 0.35, fontSize: 13, color: C.accent5 });
  }

  // ===================== 10~13. 단계별 =====================
  const stepSlides = [
    {
      nav: 0, eyebrow: "준비 단계", title: "진단 · 12주 계획",
      lead: "90분 시뮬레이션에서\n내가 ‘어디서’ 무너지는지 찾습니다",
      notes: "[준비 단계 · 멘토 1:43~1:50 구조] 이 단계에서 나만의 문제를 정확히 찾고, 어떤 순서로 고칠지 정합니다. AI 여성 영상 기반 대화 시뮬레이션으로 첫 만남, 두 번째 만남 장면을 실제로 해보고 녹화합니다. 진단이 끝나면 바꿀 것, 만들 것, 지킬 것이 정리된 12주 개인 계획을 받습니다.",
      pts: [["LuVideo", "실제 상황 시뮬레이션", "첫 만남 · 두 번째 만남을 직접 해봅니다"], ["LuEye", "녹화 장면 복기", "말투 · 표정 · 시선을 장면 단위로 확인"], ["LuClipboardList", "12주 개인 계획", "바꿀 것 · 만들 것 · 지킬 것 정리"]],
      proof: "진단에서 가장 많이 보이는 반응: 말을 서두른다 · 시선이 빠진다 · 해명이 길어진다",
    },
    {
      nav: 1, eyebrow: "1단계 · 1~4주", title: "나를 세운다",
      lead: "평가받는 순간에도\n해명하지 않는 사람이 됩니다",
      notes: "[1단계 · 멘토 1:50~3:00 구조] 멘토는 1단계(VSL)에서 '시청 지속률 80%' 같은 증거 수치와 '국내에서 저만큼 잘 가르치는 사람은 없다'는 자신감을 보여줍니다. 이다사 1단계는 나를 세우고 흔들리지 않는 구간입니다. 진단에서 가장 많이 보이는 문제, 평가받을 때 해명하는 습관을 다룹니다. 여기에 해명 시간이 줄어든 수강생 데이터를 넣으면 가장 강력합니다.",
      pts: [["LuUser", "1~2주 · 나를 세운다", "과제: 작은 부탁 3번"], ["LuAnchor", "3~4주 · 흔들리지 않는다", "과제: 선 긋기 1번"], ["LuTimer", "매일 1분 루틴", "자세 · 시선 · 2초 공백 연습"]],
      proof: "증거 넣기: 수강생 평균 해명 시간 0주 00초 → 4주 00초",
    },
    {
      nav: 2, eyebrow: "2단계 · 5~8주", title: "끌어당긴다",
      lead: "끌려다니지 않고,\n먼저 제안하는 사람이 됩니다",
      notes: "[2단계 · 멘토 3:00~3:07 구조] 5~6주는 끌려다니지 않는 연습, 7~8주는 끌어당기는 연습입니다. 내 이야기로 대화를 잇고, 호감을 숨기지 않고, 다음 만남을 먼저 제안합니다. 6주차에 0주 영상과 같은 조건으로 중간 점검 영상을 찍습니다.",
      pts: [["LuCompass", "5~6주 · 끌려다니지 않는다", "과제: 먼저 제안 5번"], ["LuMagnet", "7~8주 · 끌어당긴다", "과제: 10분 대화 1번"], ["LuVideo", "6주차 중간 점검", "0주 영상과 같은 질문으로 비교"]],
      proof: "“질문 하나, 내 이야기 하나” · “말한 그 집, 토요일에 같이 가요.”",
    },
    {
      nav: 3, eyebrow: "3단계 · 9~12주", title: "실전에서 쓴다",
      lead: "실제 만남에서 쓰고,\n연애 안에서도 나를 지킵니다",
      notes: "[3단계 · 멘토 3:07~3:23 구조] 멘토: 고가 상품은 상세페이지만으로 팔리지 않기에 1:1 세일즈 실전 교육이 필요하다. 이다사: 연애는 강의만으로 바뀌지 않기에 실제 만남에 쓰는 1:1 실전 구간이 필요합니다. 데이트 코스 답사, 실제 만남 복기, 관계 원칙 7문장까지 만들고 12주차 최종 영상을 찍습니다.",
      pts: [["LuCoffee", "9~10주 · 실제 만남에 쓴다", "과제: 데이트 코스 답사"], ["LuShield", "11~12주 · 연애 안에서 나를 지킨다", "과제: 관계 원칙 7문장"], ["LuTrophy", "12주차 최종 비교", "0 · 6 · 12주 영상 나란히 보기"]],
      proof: "증거 넣기: 실제 만남 복기 캡처 · 수강생 후기 한 줄",
    },
  ];
  for (const st of stepSlides) {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: section });
    s.addNotes(st.notes);
    await stepNav(s, st.nav);
    T(s, st.eyebrow, { x: 4.75, y: 0.5, w: 7.9, h: 0.35, fontSize: 14, bold: true, color: C.accent1, fontFace: HEAD, valign: "middle" });
    T(s, st.title, { x: 4.75, y: 0.85, w: 7.9, h: 0.8, fontSize: 32, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
    T(s, st.lead, { x: 4.75, y: 1.85, w: 7.9, h: 1.1, fontSize: 22, color: C.text1, lineSpacingMultiple: 1.1 });
    for (let i = 0; i < 3; i++) {
      const y = 3.2 + i * 0.95;
      card(s, 4.75, y, 7.85, 0.8);
      await iconCircle(s, 4.95, y + 0.13, 0.54, st.pts[i][0], HEX.navy, HEX.gold);
      T(s, st.pts[i][1], { x: 5.7, y, w: 4.0, h: 0.8, fontSize: 17, bold: true, color: C.text2, valign: "middle", fontFace: HEAD });
      T(s, st.pts[i][2], { x: 9.8, y, w: 2.65, h: 0.8, fontSize: 14, color: C.accent5, valign: "middle" });
    }
    card(s, 4.75, 6.1, 7.85, 0.65, C.background2);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.75, y: 6.1, w: 7.85, h: 0.65, rectRadius: 0.12, fill: { color: HEX.goldLt }, line: { type: "none" } });
    T(s, st.proof, { x: 5.0, y: 6.1, w: 7.4, h: 0.65, fontSize: 13, color: C.text2, valign: "middle" });
  }

  // ===================== 14. 정리 =====================
  {
    const s = newSlide("DARK", "정리하면", "진단부터 실제 연애까지, A부터 Z까지 함께합니다",
      "[정리 · 멘토 3:23~3:35 구조] 이다사 12주 태도 코칭은 진단에서 내 반응을 찾고, 12주 1:1 훈련으로 바꾸고, 졸업 뒤에도 실제 관계에서 점검받는, 연애가 시작될 때까지 함께하는 과정입니다. 단언컨대 녹화 복기로 반응 자체를 교정하는 1:1 연애 코칭은 흔하지 않습니다.");
    const flow = ["진단", "12주 1:1 훈련", "0·6·12주 영상 비교", "졸업 · 평생 회원"];
    for (let i = 0; i < 4; i++) {
      const x = 0.7 + i * 3.04;
      card(s, x, 2.4, 2.8, 1.5, i === 3 ? C.accent1 : C.accent2);
      T(s, String(i + 1).padStart(2, "0"), { x: x + 0.3, y: 2.55, w: 1, h: 0.4, fontSize: 14, bold: true, color: i === 3 ? C.text2 : C.accent1, fontFace: HEAD });
      T(s, flow[i], { x: x + 0.3, y: 3.0, w: 2.3, h: 0.6, fontSize: 19, bold: true, color: i === 3 ? C.text2 : C.background1, fontFace: HEAD });
      if (i < 3) s.addImage({ data: await icon("LuArrowRight", HEX.gold), x: x + 2.82, y: 3.05, w: 0.2, h: 0.2 });
    }
    T(s, "12주 뒤, 이 세 가지를 합니다", { x: 0.7, y: 4.4, w: 11.9, h: 0.45, fontSize: 18, bold: true, color: C.accent1, fontFace: HEAD });
    const goals = ["원하는 걸 말한다", "내 이야기로 대화를 잇는다", "다음 만남을 제안한다"];
    for (let i = 0; i < 3; i++) {
      await iconCircle(s, 0.7 + i * 4.05, 5.05, 0.6, "LuCheck", HEX.gold, HEX.navy);
      T(s, goals[i], { x: 1.45 + i * 4.05, y: 5.05, w: 3.2, h: 0.6, fontSize: 18, color: C.background1, valign: "middle" });
    }
  }

  // ===================== 15. 시장 비교 =====================
  sec("구조 · 가격");
  {
    const s = newSlide("LIGHT", "다른 연애 강의와 무엇이 다를까요?", "듣기만 해서 바뀐다면, 이미 연애를 잘했겠죠",
      "[시장 비교 · 멘토 3:35~3:55 구조] 멘토: 시중 강의는 2개월 주 1회, 1:N이라 피드백이 부족하다. 이다사: 대부분의 연애 강의는 VOD나 단체 코칭이라 내 말투와 표정을 봐주는 사람이 없습니다. 이다사는 무조건 1:1로, 녹화 장면을 함께 보며 교정하고, 졸업 뒤에도 평생 점검합니다. 타사 가격을 쓸 때는 실제 확인 가능한 범위로만 쓰세요.");
    const rows = [["", "일반 연애 강의", "이다사 12주 코칭"], ["방식", "VOD 시청 · 단체 수업", "1:1 역할극 · 녹화 · 교정"], ["피드백", "질문 게시판 · 1:N", "내 영상 장면 단위 피드백"], ["기간", "4~8주 후 종료", "12주 + 졸업 후 평생 점검"], ["증명", "수강 후기", "0 · 6 · 12주 같은 조건 영상 비교"]];
    const tbl = rows.map((r, ri) => r.map((c, ci) => ({
      text: c,
      options: {
        bold: ri === 0 || ci === 0, fontFace: ri === 0 || ci === 0 ? HEAD : BODY, fontSize: ri === 0 ? 17 : 16,
        color: ri === 0 ? (ci === 2 ? C.text2 : C.background1) : ci === 2 ? C.text2 : C.accent5,
        fill: { color: ri === 0 ? (ci === 2 ? C.accent1 : C.text2) : ci === 2 ? C.accent6 : C.background1 },
        valign: "middle", margin: [0, 0.2, 0, 0.2],
      },
    })));
    s.addTable(tbl, { x: 0.7, y: 2.05, w: 11.9, colW: [2.2, 4.6, 5.1], rowH: 0.78, border: { type: "solid", pt: 1, color: HEX.line } });
    T(s, "그래서 이다사는 무조건 1:1로만 진행합니다", { x: 0.7, y: 6.15, w: 11.9, h: 0.45, fontSize: 18, bold: true, color: C.text2, fontFace: HEAD });
  }

  // ===================== 16. 2구간 구조 =====================
  {
    const s = newSlide("LIGHT", "과정은 두 구간으로 나뉩니다", "연애는 12주 뒤에 진짜 시작됩니다",
      "[2구간 구조 · 멘토 3:55~5:21 구조] 멘토: 1구간 집중 코칭(3개월 안에 런칭) → 2구간 실전 멘토링(런칭 후 문제 해결). 집중 구간이 없으면 1년 동안 흐지부지된다. 이다사: 1구간 12주 집중 코칭에서 반응을 바꾸고, 2구간 평생 회원에서 썸·연애·다툼·결혼 고민 같은 실제 관계의 문제를 점검받습니다. 여기에 실제 사례 하나를 짧게 들려주세요. 예: 연애를 시작한 뒤 같은 문제로 다툼이 반복된 수강생이 1:1 점검 후 어떻게 달라졌는지.");
    s.addShape(pres.shapes.LINE, { x: 0.9, y: 2.55, w: 11.5, h: 0, line: { color: HEX.slate, width: 2 } });
    const phases = [
      { x: 0.7, w: 5.6, tag: "1구간 · 12주", name: "집중 코칭", dark: true, body: ["1:1 90분 × 6회 · 역할극과 교정", "강의 28편 · 매일 1분 루틴", "6주 · 12주 영상 비교", "목표: 12주 안에 반응 바꾸기"] },
      { x: 6.95, w: 5.6, tag: "2구간 · 졸업 후", name: "평생 회원 · 실전 점검", dark: false, body: ["매달 사례 라이브", "게시판 주 1회 답변", "6개월 영상 점검 · 1년 안 1:1 점검", "썸 · 연애 · 다툼 · 결혼 고민 때"] },
    ];
    for (const p of phases) {
      s.addShape(pres.shapes.OVAL, { x: p.x + 0.2, y: 2.4, w: 0.3, h: 0.3, fill: { color: p.dark ? HEX.navy : HEX.gold }, line: { type: "none" } });
      card(s, p.x, 2.95, p.w, 3.6, p.dark ? C.text2 : C.background1);
      T(s, p.tag, { x: p.x + 0.4, y: 3.2, w: 4, h: 0.35, fontSize: 14, bold: true, color: C.accent1, fontFace: HEAD });
      T(s, p.name, { x: p.x + 0.4, y: 3.6, w: 4.8, h: 0.55, fontSize: 24, bold: true, color: p.dark ? C.background1 : C.text2, fontFace: HEAD });
      for (let i = 0; i < p.body.length; i++) {
        s.addImage({ data: await icon("LuCheck", HEX.gold), x: p.x + 0.4, y: 4.42 + i * 0.5, w: 0.25, h: 0.25 });
        T(s, p.body[i], { x: p.x + 0.8, y: 4.35 + i * 0.5, w: 4.6, h: 0.4, fontSize: 15, color: p.dark ? C.accent4 : C.accent5, valign: "middle" });
      }
    }
  }

  // ===================== 17. 가격 공개 =====================
  {
    const s = newSlide("LIGHT", "가격", "두 가지 중에서 고르시면 됩니다",
      "[가격 공개 · 멘토 5:26 구조] 멤버십 가격은 화면에 보이는 가격입니다. 12주 집중 코칭은 117만 원, 12주에 평생 회원까지 더하면 149만 원입니다. 혹시 비싸다는 생각이 드시나요? 바로 다음 장에서 비교해 보겠습니다. 모두 VAT 별도이고, 환불 규정은 결제 단계에서 안내합니다.");
    const opts = [
      { x: 0.7, name: "12주 집중 코칭", price: "117만 원", m: "월 약 9.8만 원 · 12개월 할부", dark: false, items: ["진단 + 12주 개인 계획", "강의 28편 · AI 대화 연습", "1:1 90분 × 6회", "실전 복기 · 피드백", "0 · 6 · 12주 영상 비교"] },
      { x: 6.95, name: "12주 + 평생 회원", price: "149만 원", m: "월 약 12.4만 원 · 12개월 할부", dark: true, items: ["12주 집중 코칭 전부 +", "매달 사례 라이브", "게시판 주 1회 답변", "강의 평생 · 새 강의", "반년 점검 · 1년 안 1:1 점검"] },
    ];
    for (const o of opts) {
      card(s, o.x, 1.95, 5.65, 4.6, o.dark ? C.text2 : C.background1);
      if (o.dark) chip(s, o.x + 4.15, 2.2, 1.2, "추천");
      T(s, o.name, { x: o.x + 0.45, y: 2.2, w: 3.6, h: 0.4, fontSize: 18, bold: true, color: o.dark ? C.background1 : C.text2, fontFace: HEAD });
      T(s, o.price, { x: o.x + 0.45, y: 2.7, w: 4.8, h: 0.9, fontSize: 48, bold: true, color: o.dark ? C.accent1 : C.text2, fontFace: HEAD, valign: "middle" });
      T(s, o.m, { x: o.x + 0.45, y: 3.6, w: 4.8, h: 0.35, fontSize: 13, color: o.dark ? C.accent4 : C.accent5 });
      for (let i = 0; i < o.items.length; i++) {
        s.addImage({ data: await icon("LuCheck", HEX.gold), x: o.x + 0.45, y: 4.22 + i * 0.47, w: 0.24, h: 0.24 });
        T(s, o.items[i], { x: o.x + 0.85, y: 4.15 + i * 0.47, w: 4.5, h: 0.38, fontSize: 15, color: o.dark ? C.background1 : C.text1, valign: "middle" });
      }
    }
    T(s, "VAT 별도 · 평생 혜택은 졸업 후 시작 · 환불 규정은 결제 단계에서 안내", { x: 0.7, y: 6.62, w: 9, h: 0.25, fontSize: 10, color: C.accent5 });
  }

  // ===================== 18. 비싼가요? (앵커) =====================
  {
    const s = newSlide("DARK", "혹시 비싸다는 생각이 드시나요?", "1:1로 꾸준히 도움받으려면 원래 비용이 듭니다",
      "[가격 앵커 · 멘토 5:27~5:53 구조] 멘토: 시중 초고가 교육은 1,000~3,000만 원, 1:1 컨설팅은 하루 1,000만 원도 넘는다. 이다사: 회당 15만 원짜리 1:1 상담을 월 4회, 12개월 받으면 48회, 720만 원입니다. 이 계산은 가정이며 시장 평균이 아닙니다. 상담과 코칭은 목적이 다르고, 코칭은 정신건강 치료를 대체하지 않습니다. 149만 원은 그 약 5분의 1입니다.");
    s.addChart(pres.charts.BAR, [{ name: "비용(만 원)", labels: ["1년 정기 1:1 상담 (가정)", "이다사 12주 + 평생 회원", "이다사 12주 코칭"], values: [720, 149, 117] }], {
      x: 0.7, y: 2.0, w: 7.2, h: 4.2, barDir: "bar", catAxisOrientation: "maxMin",
      chartColors: [HEX.slate, HEX.gold, HEX.goldLt], varyColors: true, showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '#,##0"만 원"',
      dataLabelColor: HEX.white, dataLabelFontSize: 14, dataLabelFontFace: "+mn-lt", dataLabelFontBold: true,
      catAxisLabelColor: HEX.slate, catAxisLabelFontSize: 13, catAxisLabelFontFace: "+mn-lt", catAxisLineShow: false,
      valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 60, valAxisMaxVal: 900,
    });
    card(s, 8.4, 2.0, 4.2, 4.2, C.accent2);
    T(s, "회당 15만 원 × 월 4회 × 12개월", { x: 8.75, y: 2.35, w: 3.6, h: 0.4, fontSize: 14, color: C.accent4 });
    T(s, "= 720만 원", { x: 8.75, y: 2.85, w: 3.6, h: 0.75, fontSize: 36, bold: true, color: C.background1, fontFace: HEAD, valign: "middle" });
    T(s, "이다사 평생 코칭은", { x: 8.75, y: 4.1, w: 3.6, h: 0.4, fontSize: 16, color: C.accent4 });
    T(s, "그 5분의 1", { x: 8.75, y: 4.55, w: 3.6, h: 0.75, fontSize: 36, bold: true, color: C.accent1, fontFace: HEAD, valign: "middle" });
    T(s, "회당 15만 원 가정 예시 · 상담과 코칭은 목적이 다릅니다", { x: 0.7, y: 6.4, w: 11.9, h: 0.3, fontSize: 11, color: C.accent4 });
  }

  // ===================== 19. 코치 고용 =====================
  {
    const s = newSlide("LIGHT", "쉽게 말하면", "월 10만 원대로 1년간 ‘내 연애 코치’를 고용하는 겁니다",
      "[코치 고용 리프레임 · 멘토 6:25~6:49 구조] 멘토: 1년간 저를 월 20~40만 원에 고용한다고 보시면 된다, 막힐 때마다 물어볼 사람이 있다는 것만으로 시행착오를 100배 줄인다. 이다사: 117만 원을 12개월로 나누면 한 달 약 9만 8천 원, 상담 한 번 비용보다 적습니다. 그 돈으로 한 달 동안 내 반응을 보고 고쳐주는 코치를 두는 겁니다. 소개팅 한 번에 드는 식사비, 시간, 그리고 혼자 반복한 실패를 생각해 보세요.");
    const eq = [["117만 원", "12개월", "월 약 9.8만 원", "12주 집중 코칭", false], ["149만 원", "12개월", "월 약 12.4만 원", "12주 + 평생 회원", true]];
    for (let i = 0; i < 2; i++) {
      const y = 2.1 + i * 1.25;
      const e = eq[i];
      card(s, 0.7, y, 2.6, 0.95); T(s, e[0], { x: 0.7, y, w: 2.6, h: 0.95, fontSize: 24, bold: true, color: C.text2, align: "center", valign: "middle", fontFace: HEAD });
      T(s, "÷", { x: 3.3, y, w: 0.6, h: 0.95, fontSize: 26, color: C.accent5, align: "center", valign: "middle" });
      card(s, 3.9, y, 2.0, 0.95); T(s, e[1], { x: 3.9, y, w: 2.0, h: 0.95, fontSize: 20, color: C.text2, align: "center", valign: "middle" });
      T(s, "=", { x: 5.9, y, w: 0.6, h: 0.95, fontSize: 26, color: C.accent5, align: "center", valign: "middle" });
      card(s, 6.5, y, 3.3, 0.95, e[4] ? C.accent1 : C.text2); T(s, e[2], { x: 6.5, y, w: 3.3, h: 0.95, fontSize: 24, bold: true, color: e[4] ? C.text2 : C.accent1, align: "center", valign: "middle", fontFace: HEAD });
      T(s, e[3], { x: 10.05, y, w: 2.6, h: 0.95, fontSize: 15, color: C.accent5, valign: "middle" });
    }
    const cmp = [["LuMessageCircle", "1:1 상담 1회", "15만 원"], ["LuCoffee", "소개팅 한 번 식사 · 카페", "5~10만 원"], ["LuUserCheck", "내 연애 코치 한 달", "약 9.8만 원"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.7 + i * 4.05;
      card(s, x, 4.85, 3.75, 1.5, i === 2 ? C.text2 : C.background1);
      await iconCircle(s, x + 0.3, 5.2, 0.8, cmp[i][0], i === 2 ? HEX.gold : HEX.bg, i === 2 ? HEX.navy : HEX.navy);
      T(s, cmp[i][1], { x: x + 1.3, y: 5.1, w: 2.3, h: 0.45, fontSize: 14, color: i === 2 ? C.accent4 : C.accent5, valign: "middle" });
      T(s, cmp[i][2], { x: x + 1.3, y: 5.55, w: 2.3, h: 0.55, fontSize: 22, bold: true, color: i === 2 ? C.accent1 : C.text2, fontFace: HEAD, valign: "middle" });
    }
    T(s, "12개월 할부 기준 · VAT 별도 · 할부 이자는 카드사 기준", { x: 0.7, y: 6.55, w: 11.9, h: 0.3, fontSize: 11, color: C.accent5 });
  }

  // ===================== 20. 이런 분은 신청하지 마세요 =====================
  sec("고민 해소 · 신청");
  {
    const s = newSlide("LIGHT", "솔직하게 말씀드립니다", "이런 분은 신청하지 마세요",
      "[자격 제한 · 멘토 6:21~6:25 구조] 멘토: 한 달에 한두 개조차 팔 자신이 없다면 절대 가입하지 마세요. 이다사: 이 과정은 듣기만 하는 강의가 아니라 매주 직접 해보고 녹화하고 고치는 훈련입니다. 멘트만 원하시거나, 과제를 해볼 생각이 없거나, 결과를 보장받고 싶은 분께는 맞지 않습니다. 대신 지금의 나를 바꾸고 싶은 분이라면, 끝까지 함께하겠습니다.");
    const no = ["‘한 방 멘트’만 알고 싶은 분", "2주에 과제 하나도 해볼 생각이 없는 분", "연애 결과를 보장받고 싶은 분"];
    const yes = ["긴장하는 순간의 나를 정확히 알고 싶은 분", "녹화된 내 모습을 보는 게 불편해도 해볼 분", "12주 동안 작게라도 매주 실행할 분"];
    card(s, 0.7, 2.05, 5.75, 4.5);
    await iconCircle(s, 1.05, 2.35, 0.7, "LuBan", HEX.redLt, HEX.red);
    T(s, "맞지 않는 분", { x: 1.95, y: 2.35, w: 4, h: 0.7, fontSize: 22, bold: true, color: C.accent3, valign: "middle", fontFace: HEAD });
    card(s, 6.85, 2.05, 5.75, 4.5, C.text2);
    await iconCircle(s, 7.2, 2.35, 0.7, "LuCheck", HEX.gold, HEX.navy);
    T(s, "함께할 분", { x: 8.1, y: 2.35, w: 4, h: 0.7, fontSize: 22, bold: true, color: C.accent1, valign: "middle", fontFace: HEAD });
    for (let i = 0; i < 3; i++) {
      const y = 3.45 + i * 0.95;
      s.addImage({ data: await icon("LuX", HEX.red), x: 1.05, y: y + 0.08, w: 0.32, h: 0.32 });
      T(s, no[i], { x: 1.55, y, w: 4.7, h: 0.5, fontSize: 17, color: C.text1, valign: "middle" });
      s.addImage({ data: await icon("LuCheck", HEX.gold), x: 7.2, y: y + 0.08, w: 0.32, h: 0.32 });
      T(s, yes[i], { x: 7.7, y, w: 4.7, h: 0.5, fontSize: 17, color: C.background1, valign: "middle" });
    }
  }

  // ===================== 21. 고민 해소 =====================
  {
    const s = newSlide("LIGHT", "신청하고 싶어도, 이런 고민이 있으시죠", "걱정하지 마세요. 진단에서 함께 확인합니다",
      "[고민 해소 · 멘토 6:51~7:00 구조] 멘토: 어떤 상품을 팔지 모르겠거나, 초보라 걱정되거나, 나이가 많아 두렵거나, 해낼 수 있을지 궁금하신 분. 걱정하지 마세요, 제가 모두 해결해 드리겠습니다. 이다사: 말주변이 없어서, 나이가 많아서, 연애 경험이 거의 없어서, 시간이 부족해서 걱정되시나요? 진단에서 지금의 나를 함께 보고, 할 수 있는 순서대로 계획을 드립니다.");
    const q = [["LuMicOff", "말주변이 없어요", "말을 잘하는 게 목표가 아닙니다\n긴장한 순간의 반응을 바꿉니다"], ["LuClock", "나이가 많아요", "태도는 나이와 상관없이\n12주 단위로 바뀝니다"], ["LuUserRound", "연애 경험이 거의 없어요", "그래서 시뮬레이션으로\n실전 전에 먼저 연습합니다"], ["LuCalendarClock", "시간이 부족해요", "주당 1~2시간\n과제를 못 해도 수업은 진행"]];
    for (let i = 0; i < 4; i++) {
      const x = 0.7 + (i % 2) * 6.05, y = 2.05 + Math.floor(i / 2) * 2.25;
      card(s, x, y, 5.8, 2.0);
      await iconCircle(s, x + 0.35, y + 0.35, 0.75, q[i][0], HEX.bg, HEX.navy);
      T(s, "“" + q[i][1] + "”", { x: x + 1.35, y: y + 0.3, w: 4.2, h: 0.5, fontSize: 19, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
      T(s, q[i][2], { x: x + 1.35, y: y + 0.9, w: 4.2, h: 0.85, fontSize: 15, color: C.accent5 });
    }
  }

  // ===================== 22. CTA · 진단 신청 =====================
  {
    const s = newSlide("DARK", "지금 바로", "먼저 90분 진단에서, 지금의 나를 확인하세요",
      "[CTA · 멘토 7:01~7:12 구조] 멘토: 단돈 5만 원 1:1 상담으로 맞춤 로드맵을 드리고, 상담 후 도와드릴 수 있다고 판단되는 소수에게만 멤버십 기회를 드립니다. 부담 갖지 말고 신청하세요. 이다사: 90분 진단에서 내가 어디서 흔들리는지 확인하고 12주 개인 계획을 받습니다. 진단 결과 훈련이 필요하고 서로 맞다고 판단될 때만 12주 코칭을 안내드립니다. 진단비는 실제 금액으로 넣으세요.");
    const st = [["LuCalendarCheck", "진단 신청", "90분 · 줌 진행\n진단비 [ ]원"], ["LuClipboardList", "12주 계획 받기", "내 반응 패턴 ·\n고칠 순서 정리"], ["LuHandshake", "합류 여부 결정", "맞다고 판단될 때만\n12주 코칭 안내"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.7 + i * 4.05;
      card(s, x, 2.15, 3.75, 3.2, i === 0 ? C.accent1 : C.accent2);
      await iconCircle(s, x + 0.4, 2.5, 0.8, st[i][0], i === 0 ? HEX.navy : HEX.gold, i === 0 ? HEX.gold : HEX.navy);
      T(s, String(i + 1).padStart(2, "0"), { x: x + 2.75, y: 2.55, w: 0.7, h: 0.5, fontSize: 22, bold: true, color: i === 0 ? C.text2 : C.accent1, align: "right", fontFace: HEAD });
      T(s, st[i][1], { x: x + 0.4, y: 3.55, w: 3.0, h: 0.5, fontSize: 22, bold: true, color: i === 0 ? C.text2 : C.background1, fontFace: HEAD });
      T(s, st[i][2], { x: x + 0.4, y: 4.2, w: 3.0, h: 0.9, fontSize: 15, color: i === 0 ? C.text2 : C.accent4 });
      if (i < 2) s.addImage({ data: await icon("LuArrowRight", HEX.gold), x: x + 3.78, y: 3.65, w: 0.24, h: 0.24 });
    }
    T(s, "외운 멘트 없이, 평소의 나로 오시면 됩니다", { x: 0.7, y: 5.85, w: 11.9, h: 0.5, fontSize: 20, bold: true, color: C.accent1, fontFace: HEAD });
  }

  // ===================== 23. 클로징 =====================
  {
    const s = pres.addSlide({ masterName: "COVER", sectionTitle: section });
    s.addNotes("[클로징 · 멘토 7:14~7:26 구조] 이미 많은 분들이 이다사에서 달라졌습니다. 그리고 그 시작은 90분 진단이었습니다. 더 이상 새벽까지 소개팅 멘트를 검색하며 지치지 마세요. 이제는 내 모습 그대로 다음 만남을 잡을 때입니다. 지금 바로 진단을 신청하세요. 감사합니다.");
    s.addImage({ data: await icon("LuMoon", HEX.navy2), x: 8.6, y: 1.2, w: 5.0, h: 5.0, transparency: 30 });
    T(s, "더 이상 새벽까지\n소개팅 멘트를 검색하지 마세요", { x: 0.8, y: 1.6, w: 9.5, h: 2.2, fontSize: 42, bold: true, color: C.background1, fontFace: HEAD, lineSpacingMultiple: 1.1 });
    T(s, "이제는 내 모습 그대로, 다음 만남을 잡을 때입니다", { x: 0.8, y: 4.05, w: 9.5, h: 0.5, fontSize: 20, color: C.accent4 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 5.0, w: 4.6, h: 0.85, rectRadius: 0.42, fill: { color: HEX.gold }, line: { type: "none" } });
    T(s, "지금 90분 진단 신청하기", { x: 0.8, y: 5.0, w: 4.6, h: 0.85, fontSize: 20, bold: true, color: C.text2, align: "center", valign: "middle", fontFace: HEAD });
    T(s, "이다사 · 12주 태도 코칭", { x: 0.8, y: 6.9, w: 5, h: 0.3, fontSize: 11, color: C.accent4 });
  }

  const out = "/home/user/speed/idasa-ot/이다사_OT_고파사구조.pptx";
  require("fs").mkdirSync("/home/user/speed/idasa-ot", { recursive: true });
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
})();
