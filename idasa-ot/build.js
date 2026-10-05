// 이다사 12주 부트캠프 OT — 멘토(고파사) VSL 구조, 슬라이드는 핵심만 · 설명은 대본(발표자 노트)으로
// run: NODE_PATH=<node_modules> node build.js   → deck.pptx + script.json
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");
const fs = require("fs");
const path = require("path");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const OUT = path.join(__dirname, "이다사_12주부트캠프_OT.pptx");
const HEAD = "에스코어 드림 6 Bold";
const BODY = "에스코어 드림 4 Regular";
const HEX = {
  navy: "142340", navy2: "23365E", ink: "0D182E", gold: "C9A24B", goldLt: "EBDDB3",
  bg: "F4F6FA", white: "FFFFFF", mute: "586379", line: "D9DEE8", red: "D6453D", redLt: "FBE9E7", slate: "B8C2D4",
};
const THEME = {
  name: "이다사 OT", headFontFace: HEAD, bodyFontFace: BODY,
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.navy, lt2: HEX.bg,
    accent1: HEX.gold, accent2: HEX.navy2, accent3: HEX.red, accent4: HEX.slate,
    accent5: HEX.mute, accent6: HEX.goldLt, hlink: HEX.navy2, folHlink: HEX.mute,
  },
};
const PRODUCT = "이다사 12주 부트캠프";
const PLAN_A = "12주 부트캠프";
const PLAN_B = "부트캠프 + 평생 회원";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = PRODUCT + " OT";
pres.author = "이다사";
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
const C = pres.SchemeColor;

// ---------- layouts (no slide numbers) ----------
const eyebrowPh = { name: "eyebrow", type: "body", x: 0.8, y: 0.6, w: 11.7, h: 0.4, fontSize: 16, bold: true, color: C.accent1, fontFace: HEAD, margin: 0, valign: "middle", align: "left" };
const titlePh = (color) => ({ name: "title", type: "title", x: 0.8, y: 1.0, w: 11.7, h: 1.6, fontSize: 40, bold: true, color, fontFace: HEAD, margin: 0, valign: "top", align: "left", lineSpacingMultiple: 1.05 });
const brand = (dark) => ({ text: { text: PRODUCT, options: { x: 0.8, y: 6.95, w: 5, h: 0.3, fontSize: 10, color: dark ? C.accent4 : C.accent5, margin: 0 } } });
pres.defineSlideMaster({ title: "LIGHT", background: { color: HEX.bg }, objects: [brand(false), { placeholder: { options: eyebrowPh, text: "" } }, { placeholder: { options: titlePh(C.text2), text: "" } }] });
pres.defineSlideMaster({ title: "DARK", background: { color: HEX.navy }, objects: [brand(true), { placeholder: { options: eyebrowPh, text: "" } }, { placeholder: { options: titlePh(C.background1), text: "" } }] });
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
const T = (s, text, o) => s.addText(text, { isTextBox: true, margin: 0, fontFace: BODY, color: C.text1, fontSize: 18, valign: "top", ...o });
function card(s, x, y, w, h, fill = C.background1) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, rectRadius: 0.14, line: { type: "none" }, shadow: sh() });
}
async function iconCircle(s, x, y, d, name, bg, fg) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
  const p = d * 0.26;
  s.addImage({ data: await icon(name, fg), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, altText: name });
}
async function slot(s, x, y, w, h, label, dark = false) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: dark ? HEX.navy2 : "E9EDF4" }, line: { color: dark ? HEX.slate : "A9B3C6", width: 1.25, dashType: "dash" }, objectName: "교체용 슬롯" });
  const d = Math.min(0.55, h * 0.3);
  s.addImage({ data: await icon("LuImage", dark ? HEX.slate : HEX.mute), x: x + w / 2 - d / 2, y: y + h / 2 - d - 0.05, w: d, h: d });
  T(s, label, { x: x + 0.15, y: y + h / 2 + 0.08, w: w - 0.3, h: 0.4, fontSize: 12, align: "center", color: dark ? C.accent4 : C.accent5 });
}
function chip(s, x, y, w, text, fill = C.accent1, color = C.text2) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.46, rectRadius: 0.23, fill: { color: fill }, line: { type: "none" } });
  T(s, text, { x, y, w, h: 0.46, fontSize: 15, bold: true, align: "center", valign: "middle", color, fontFace: HEAD });
}
const SCRIPT = [];
function slide(master, eyebrow, title, script) {
  const s = pres.addSlide({ masterName: master, sectionTitle: curSection });
  if (eyebrow) s.addText(eyebrow, { placeholder: "eyebrow" });
  if (title) s.addText(title, { placeholder: "title" });
  s.addNotes(script);
  SCRIPT.push({ section: curSection, script });
  return s;
}
let curSection = "";
const sec = (t) => { curSection = t; pres.addSection({ title: t }); };

const STEPS = ["준비 · 진단", "1단계 · 나를 세운다", "2단계 · 끌어당긴다", "3단계 · 실전에서 쓴다"];
async function stepSlide(active, title, lead, iconName, script) {
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: curSection });
  s.addNotes(script);
  SCRIPT.push({ section: curSection, script });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 4.2, h: 7.5, fill: { color: C.text2 }, line: { type: "none" } });
  T(s, "12주 프로세스", { x: 0.6, y: 0.7, w: 3.2, h: 0.4, fontSize: 16, bold: true, color: C.accent1, fontFace: HEAD });
  STEPS.forEach((t, i) => {
    const y = 1.6 + i * 0.85, on = i === active;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.45, y, w: 3.3, h: 0.64, rectRadius: 0.1, fill: { color: on ? HEX.gold : HEX.navy2 }, line: { type: "none" } });
    T(s, t, { x: 0.7, y, w: 3.0, h: 0.64, fontSize: 16, bold: on, valign: "middle", color: on ? C.text2 : C.accent4, fontFace: on ? HEAD : BODY });
  });
  await iconCircle(s, 5.0, 1.3, 1.3, iconName, HEX.navy, HEX.gold);
  T(s, title, { x: 5.0, y: 3.0, w: 7.6, h: 1.0, fontSize: 44, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
  T(s, lead, { x: 5.0, y: 4.2, w: 7.6, h: 1.4, fontSize: 24, color: C.accent5, lineSpacingMultiple: 1.15 });
  T(s, PRODUCT, { x: 4.75, y: 6.95, w: 5, h: 0.3, fontSize: 10, color: C.accent5 });
}

(async () => {
  // ============ 훅 · 신뢰 ============
  sec("훅 · 신뢰");
  {
    const script = `좋아하는 여자 앞에서만 이상하게 말이 많아지시나요?
소개팅에서 대화는 끊기지 않고 잘 이어간 것 같은데, 이상하게 두 번째 만남은 잡히지 않습니다.
집에 와서 다시 '소개팅 멘트', '애프터 신청 방법'을 검색하고 계시죠.
이 영상을 끝까지 보시면, 더 이상 멘트를 검색하지 않으셔도 됩니다.
왜 두 번째 만남이 안 잡히는지, 그리고 12주 동안 무엇을 바꾸면 되는지 지금부터 말씀드리겠습니다.`;
    const s = pres.addSlide({ masterName: "COVER", sectionTitle: curSection });
    s.addNotes(script); SCRIPT.push({ section: curSection, script });
    s.addImage({ data: await icon("LuCompass", HEX.navy2), x: 8.3, y: 1.0, w: 5.6, h: 5.6, transparency: 30 });
    T(s, "두 번째 만남,\n왜 안 잡힐까요?", { x: 0.8, y: 2.0, w: 9, h: 2.4, fontSize: 60, bold: true, color: C.background1, fontFace: HEAD, lineSpacingMultiple: 1.05 });
    chip(s, 0.8, 4.9, 3.3, PRODUCT);
  }
  {
    const s = slide("LIGHT", "먼저 결과부터", "멘트 없이 바꾼 결과",
      `먼저 결과부터 보여드리겠습니다.
[실제 수치] 12주 안에 두 번째 만남을 직접 제안한 수강생이 00%입니다.
평가받는 순간 길게 해명하던 시간은 평균 00초에서 0초로 줄었습니다.
그리고 부트캠프 기간 중에 연애를 시작한 분이 00명입니다.
이분들, 멘트를 외운 게 아닙니다. 긴장하는 순간의 반응을 바꿨을 뿐입니다.
(※ 실제 확인된 숫자로 바꿔 읽으세요.)`);
    const st = [["00%", "먼저 제안"], ["−00초", "해명 시간"], ["00명", "연애 시작"]];
    st.forEach(([n, l], i) => {
      const x = 0.8 + i * 3.97;
      card(s, x, 2.9, 3.65, 3.3);
      T(s, n, { x: x + 0.4, y: 3.3, w: 3.1, h: 1.3, fontSize: 54, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
      T(s, l, { x: x + 0.4, y: 4.8, w: 3.0, h: 0.5, fontSize: 22, color: C.accent5 });
      T(s, "실제 수치로 교체", { x: x + 0.4, y: 5.55, w: 3.0, h: 0.3, fontSize: 11, bold: true, color: C.accent3 });
    });
  }
  {
    const s = slide("LIGHT", "저는", "긴장한 순간만\n봐 온 사람입니다",
      `이런 말을 하는 제가 과연 믿을 만한 사람인지 궁금하시죠.
저는 [기간] 동안 [0,000]건이 넘는 소개팅·연애 고민을 1:1로 상담해 왔습니다.
말로 듣는 상담만 한 게 아닙니다. 실제로 대화를 해보게 하고, 녹화하고, 말투와 표정과 시선을 장면 단위로 다시 봤습니다. 그렇게 쌓인 녹화 복기만 [000]시간이 넘습니다.
[플랫폼·수상·출간 기록을 한 문장으로.]
그래서 저는 남자들이 어느 순간에 무너지는지, 정확히 알고 있습니다.`);
    [["0,000건", "1:1 상담"], ["000시간", "녹화 복기"]].forEach(([n, l], i) => {
      T(s, n, { x: 0.8, y: 3.3 + i * 1.5, w: 6, h: 0.9, fontSize: 48, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
      T(s, l, { x: 0.8, y: 4.15 + i * 1.5, w: 6, h: 0.4, fontSize: 20, color: C.accent5 });
    });
    await slot(s, 7.5, 1.3, 5.0, 5.2, "프로필 · 상담 현장 사진");
  }
  {
    const s = slide("LIGHT", "수강생들의 변화", "영상이 증명합니다",
      `수강생들의 변화는 말이 아니라 영상으로 확인합니다.
부트캠프를 시작하는 날, 같은 질문으로 영상을 찍습니다. 그리고 6주차, 12주차에 똑같은 질문, 똑같은 조건으로 다시 찍습니다.
0주차에는 상대가 "그건 좀 별로인데요?" 한마디만 해도 40초 넘게 해명하던 분이,
6주차에는 2초 멈추고 자기 생각을 말하고,
12주차에는 웃으면서 "그럼 토요일에 같이 가요"라고 먼저 제안합니다.
(※ 동의받은 수강생 전후 캡처를 넣으세요. 결과는 실행에 따라 다릅니다.)`);
    const weeks = ["0주", "6주", "12주"];
    for (let i = 0; i < 3; i++) {
      const x = 0.8 + i * 3.97;
      await slot(s, x, 2.75, 3.65, 2.9, "수강생 영상 캡처");
      T(s, weeks[i], { x, y: 5.85, w: 3.65, h: 0.6, fontSize: 30, bold: true, color: i === 2 ? C.accent1 : C.text2, fontFace: HEAD, align: "center" });
    }
  }
  {
    const s = slide("LIGHT", "지금도 오는 메시지", "결과가 없었다면\n오지 않았을 연락",
      `그리고 지금도 이런 메시지가 계속 옵니다.
"토요일에 같이 가자고 제가 먼저 말했어요. 예전 같으면 상상도 못 했을 거예요."
"처음으로 소개팅 끝나고 상대가 먼저 연락 왔습니다."
[실제 후기 2~3개를 그대로 읽으세요.]
저에게 오신 분들이 정말 변하지 않았다면, 이런 연락은 오지 않았겠죠.`);
    for (let i = 0; i < 4; i++) await slot(s, 0.8 + i * 2.98, 2.85, 2.75, 3.6, "후기 캡처");
  }

  // ============ 문제 · 해법 ============
  sec("문제 · 해법");
  {
    const s = slide("DARK", "소개합니다", PRODUCT,
      `${PRODUCT}는 제가 수많은 상담과 녹화 복기를 하며 쌓은 방법을 그대로 담은 1:1 훈련 과정입니다.
진단에서 내가 어디서 무너지는지 찾고,
12주 동안 1:1로 역할극하고 녹화하고 고치면서 그 반응을 바꾸고,
졸업한 뒤에도 실제 연애에서 평생 점검받습니다.
PDF 받고 영상만 보는 강의가 아닙니다. 직접 해보고, 고치는 부트캠프입니다.`);
    const it = [["LuStethoscope", "진단"], ["LuUserCheck", "1:1 훈련"], ["LuInfinity", "평생 점검"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.8 + i * 3.97;
      card(s, x, 3.0, 3.65, 3.2, C.accent2);
      await iconCircle(s, x + 1.2, 3.45, 1.25, it[i][0], HEX.gold, HEX.navy);
      T(s, it[i][1], { x, y: 5.0, w: 3.65, h: 0.7, fontSize: 28, bold: true, color: C.background1, fontFace: HEAD, align: "center", valign: "middle" });
    }
  }
  {
    const s = slide("LIGHT", "수많은 상담 끝에 깨달은 진실", "멘트가 아니라\n반응을 바꿔야 합니다",
      `제가 수많은 분들을 상담하면서 깨달은 진실이 하나 있습니다.
연애가 서툰 사람일수록, 멘트를 더 외울 게 아니라 '반응'을 바꿔야 한다는 겁니다.
멘트 100개를 외워도, 마음에 드는 여자 앞에서 긴장하는 순간 전부 사라집니다.
하지만 평가받는 순간 2초 멈추고 내 기준을 말하는 반응 하나는, 한 번 몸에 익으면 어떤 상대 앞에서도 남습니다.
멘트 100개보다 반응 하나가 훨씬 쉽고, 훨씬 현실적입니다.`);
    card(s, 0.8, 3.6, 5.6, 2.4);
    T(s, "멘트 100개", { x: 0.8, y: 3.6, w: 5.6, h: 2.4, fontSize: 36, bold: true, color: C.accent5, fontFace: HEAD, align: "center", valign: "middle" });
    T(s, "<", { x: 6.4, y: 3.6, w: 0.5, h: 2.4, fontSize: 44, bold: true, color: C.accent1, align: "center", valign: "middle" });
    card(s, 6.9, 3.6, 5.6, 2.4, C.text2);
    T(s, "반응 1개", { x: 6.9, y: 3.6, w: 5.6, h: 2.4, fontSize: 36, bold: true, color: C.accent1, fontFace: HEAD, align: "center", valign: "middle" });
  }
  {
    const s = slide("LIGHT", "요즘 넘쳐나는 연애 강의들", "외운 멘트는\n긴장하면 사라집니다",
      `요즘 '이 멘트만 쓰면 된다', '카톡은 이렇게 보내라'는 강의와 영상이 정말 많습니다.
그런데 상대 반응이 대본과 조금만 달라져도, 다음 말이 막힙니다.
픽업이나 밀당 기술은 연기라서 오래 못 갑니다. 관계가 시작돼도 계속 불안합니다.
유튜브 꿀팁은 보는 순간엔 알 것 같지만, 막상 긴장하면 몸이 안 따라옵니다.
상대가 바뀌어도, 상황이 바뀌어도 남는 건 단 하나, 긴장한 순간에도 무너지지 않는 '내 태도'입니다.`);
    const b = [["LuMessageSquareText", "멘트 모음"], ["LuFlame", "픽업 기술"], ["LuYoutube", "유튜브 꿀팁"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.8 + i * 3.97;
      card(s, x, 3.2, 3.65, 2.9);
      await iconCircle(s, x + 0.4, 3.6, 1.0, b[i][0], HEX.redLt, HEX.red);
      s.addImage({ data: await icon("LuX", HEX.red), x: x + 2.65, y: 3.7, w: 0.6, h: 0.6 });
      T(s, b[i][1], { x: x + 0.4, y: 4.9, w: 3.0, h: 0.7, fontSize: 26, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
    }
  }

  // ============ 커리큘럼 ============
  sec("커리큘럼");
  {
    const s = slide("LIGHT", "12주 프로세스", "준비 + 3단계",
      `${PRODUCT}는 준비 단계와 3단계로 진행됩니다.
준비 단계에서 진단을 받고 나만의 12주 계획을 세웁니다.
1단계 1~4주차는 나를 세우는 구간,
2단계 5~8주차는 끌어당기는 구간,
3단계 9~12주차는 실제 만남에서 쓰는 구간입니다.
하나씩 보여드리겠습니다.`);
    const bl = [["LuStethoscope", "준비", "진단"], ["LuAnchor", "1단계", "나를 세운다"], ["LuMagnet", "2단계", "끌어당긴다"], ["LuCoffee", "3단계", "실전에서 쓴다"]];
    for (let i = 0; i < 4; i++) {
      const x = 0.8 + i * 2.98, on = i === 0;
      card(s, x, 2.9, 2.75, 3.4, on ? C.text2 : C.background1);
      await iconCircle(s, x + 0.35, 3.3, 0.95, bl[i][0], on ? HEX.gold : HEX.navy, on ? HEX.navy : HEX.gold);
      T(s, bl[i][1], { x: x + 0.35, y: 4.5, w: 2.2, h: 0.4, fontSize: 16, bold: true, color: C.accent1, fontFace: HEAD });
      T(s, bl[i][2], { x: x + 0.35, y: 4.95, w: 2.3, h: 0.9, fontSize: 24, bold: true, color: on ? C.background1 : C.text2, fontFace: HEAD });
    }
  }
  await stepSlide(0, "진단", "90분 동안,\n내가 어디서 무너지는지 찾습니다", "LuStethoscope",
    `먼저 준비 단계, 진단입니다.
90분 동안 AI 여성 영상과 실제 상황처럼 대화를 해봅니다. 첫 만남 장면, 두 번째 만남 장면을 직접 해보고 녹화합니다.
그리고 녹화된 장면을 같이 보면서 확인합니다. 말을 서두르는지, 시선이 빠지는지, 해명이 길어지는지.
진단이 끝나면 바꿀 것, 새로 만들 것, 지킬 것이 정리된 나만의 12주 계획을 받습니다.`);
  await stepSlide(1, "나를 세운다", "평가받아도\n해명하지 않습니다", "LuAnchor",
    `1단계, 1~4주차는 나를 세우는 구간입니다.
진단에서 가장 많이 보이는 문제가 바로 이겁니다. 상대가 조금만 평가하는 말을 해도 길게 해명하는 습관.
1~2주차에는 일상에서 작은 부탁을 세 번 해보고, 3~4주차에는 선을 한 번 그어봅니다.
그리고 매일 1분, 자세와 시선, 2초 공백을 연습합니다.
[증거: 수강생 평균 해명 시간이 0주 00초에서 4주 00초로 줄었습니다.]`);
  await stepSlide(2, "끌어당긴다", "끌려다니지 않고\n먼저 제안합니다", "LuMagnet",
    `2단계, 5~8주차는 끌어당기는 구간입니다.
상대 반응에 끌려다니지 않고, 내 이야기로 대화를 잇습니다. 질문 하나, 내 이야기 하나.
호감을 숨기지 않고, 다음 만남을 먼저 제안합니다. "말한 그 집, 토요일에 같이 가요."
6주차에는 처음 찍은 영상과 같은 질문으로 다시 찍어서, 지금까지 무엇이 달라졌는지 직접 확인합니다.`);
  await stepSlide(3, "실전에서 쓴다", "실제 만남에서 쓰고,\n연애 안에서도 나를 지킵니다", "LuCoffee",
    `마지막 3단계, 9~12주차는 실전 구간입니다.
연애는 강의를 듣는 것만으로 바뀌지 않습니다. 그래서 실제 만남에서 써봐야 합니다.
데이트 코스를 직접 답사하고, 실제 만남을 하고, 그 장면을 1:1로 같이 복기합니다.
그리고 연애가 시작된 뒤에도 흔들리지 않도록, 나만의 관계 원칙 7문장을 만듭니다.
12주차에 0주, 6주, 12주 영상을 나란히 놓고 최종 비교합니다.`);
  {
    const s = slide("DARK", "정리하면", "12주 뒤,\n이 세 가지를 합니다",
      `정리하면, ${PRODUCT}는 진단부터 실제 연애가 시작될 때까지 A부터 Z까지 함께하는 과정입니다.
12주 뒤 여러분은 이 세 가지를 하게 됩니다.
원하는 걸 말합니다. 내 이야기로 대화를 잇습니다. 그리고 다음 만남을 먼저 제안합니다.
단언컨대, 내 녹화 영상을 장면 단위로 보면서 반응 자체를 고쳐주는 1:1 연애 훈련은 흔하지 않습니다.`);
    const g = ["원하는 걸 말한다", "대화를 잇는다", "먼저 제안한다"];
    for (let i = 0; i < 3; i++) {
      const x = 0.8 + i * 3.97;
      card(s, x, 3.3, 3.65, 2.6, C.accent2);
      await iconCircle(s, x + 0.4, 3.7, 0.9, "LuCheck", HEX.gold, HEX.navy);
      T(s, g[i], { x: x + 0.4, y: 4.85, w: 3.0, h: 0.7, fontSize: 24, bold: true, color: C.background1, fontFace: HEAD, valign: "middle" });
    }
  }

  // ============ 구조 · 가격 ============
  sec("구조 · 가격");
  {
    const s = slide("LIGHT", "다른 연애 강의와 다른 점", "무조건 1:1로만",
      `여러분, 연애 강의를 듣기만 해서 바뀐다면, 강의를 가장 많이 들은 사람이 연애를 제일 잘했어야 합니다. 그렇죠?
대부분의 연애 강의는 영상을 보거나 단체로 수업을 듣고 끝납니다. 내 말투, 내 표정, 내 시선을 봐주는 사람은 없습니다.
그리고 4주, 8주 지나면 끝납니다.
그래서 ${PRODUCT}는 무조건 1:1로만 진행합니다. 내 영상을 장면 단위로 보면서 고치고, 졸업한 뒤에도 평생 점검합니다.`);
    card(s, 0.8, 3.0, 5.6, 3.3);
    await iconCircle(s, 1.2, 3.4, 0.95, "LuUsers", HEX.bg, HEX.mute);
    T(s, "듣는 강의", { x: 1.2, y: 4.6, w: 4.8, h: 0.7, fontSize: 30, bold: true, color: C.accent5, fontFace: HEAD });
    T(s, "VOD · 단체 · 4~8주", { x: 1.2, y: 5.35, w: 4.8, h: 0.5, fontSize: 20, color: C.accent5 });
    card(s, 6.9, 3.0, 5.6, 3.3, C.text2);
    await iconCircle(s, 7.3, 3.4, 0.95, "LuUserCheck", HEX.gold, HEX.navy);
    T(s, "1:1 교정", { x: 7.3, y: 4.6, w: 4.8, h: 0.7, fontSize: 30, bold: true, color: C.accent1, fontFace: HEAD });
    T(s, "녹화 복기 · 12주 + 평생", { x: 7.3, y: 5.35, w: 4.8, h: 0.5, fontSize: 20, color: C.background1 });
  }
  {
    const s = slide("LIGHT", "두 구간으로 나뉩니다", "연애는 12주 뒤에\n진짜 시작됩니다",
      `부트캠프는 크게 두 구간으로 나뉩니다.
첫 번째 구간은 12주 집중 구간입니다. 1:1 90분 코칭 6회, 강의, 매일 루틴, 실전 과제로 반응을 바꿉니다.
이 집중 구간이 없으면, 대부분 아무것도 안 하고 흐지부지됩니다. 그래서 12주 안에 반드시 바꾸는 걸 목표로 달립니다.
두 번째 구간은 졸업 후 평생 회원 구간입니다.
진짜 연애는 12주 뒤에 시작됩니다. 썸이 생겼을 때, 연애가 시작됐을 때, 같은 문제로 다툴 때, 결혼을 고민할 때, 그때마다 돌아와서 점검받으시면 됩니다.
매달 사례 라이브, 게시판 주 1회 답변, 6개월 영상 점검, 1년 안 1:1 점검 1회가 포함됩니다.
[실제 사례 하나를 짧게: 연애 시작 후 고민이 생긴 수강생을 어떻게 도왔는지.]`);
    s.addShape(pres.shapes.LINE, { x: 1.2, y: 3.35, w: 10.9, h: 0, line: { color: HEX.slate, width: 2 } });
    [[0.8, "1구간 · 12주", "집중 부트캠프", true], [6.9, "2구간 · 졸업 후", "평생 회원", false]].forEach(([x, tag, name, dark]) => {
      s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 3.18, w: 0.34, h: 0.34, fill: { color: dark ? HEX.navy : HEX.gold }, line: { type: "none" } });
      card(s, x, 3.85, 5.6, 2.5, dark ? C.text2 : C.background1);
      T(s, tag, { x: x + 0.45, y: 4.2, w: 4.8, h: 0.4, fontSize: 18, bold: true, color: C.accent1, fontFace: HEAD });
      T(s, name, { x: x + 0.45, y: 4.75, w: 4.8, h: 0.9, fontSize: 36, bold: true, color: dark ? C.background1 : C.text2, fontFace: HEAD, valign: "middle" });
    });
  }
  {
    const s = slide("LIGHT", "가격", "두 가지 중 하나",
      `가격은 화면에 보이는 그대로입니다.
${PLAN_A}는 117만 원, 12개월 할부로 한 달 약 9만 8천 원입니다.
${PLAN_B}은 149만 원, 한 달 약 12만 4천 원입니다.
32만 원 차이로 졸업 뒤에도 라이브, 게시판 답변, 반년 점검, 1:1 점검이 평생 이어집니다.
모두 VAT 별도이고, 환불 규정은 결제 단계에서 안내드립니다.
혹시 가격을 보고 비싸다는 생각이 드셨나요?`);
    [[0.8, PLAN_A, "117만 원", false], [6.9, PLAN_B, "149만 원", true]].forEach(([x, n, p, dark]) => {
      card(s, x, 2.9, 5.6, 3.4, dark ? C.text2 : C.background1);
      if (dark) chip(s, x + 4.05, 3.2, 1.25, "추천");
      T(s, n, { x: x + 0.5, y: 3.25, w: 3.6, h: 0.5, fontSize: 22, bold: true, color: dark ? C.background1 : C.text2, fontFace: HEAD, valign: "middle" });
      T(s, p, { x: x + 0.5, y: 4.0, w: 4.8, h: 1.3, fontSize: 64, bold: true, color: dark ? C.accent1 : C.text2, fontFace: HEAD, valign: "middle" });
      T(s, "VAT 별도", { x: x + 0.5, y: 5.5, w: 4.8, h: 0.4, fontSize: 14, color: dark ? C.accent4 : C.accent5 });
    });
  }
  {
    const s = slide("DARK", "비싼가요?", "1년 상담의\n5분의 1",
      `아니요, 오히려 저렴합니다.
1:1로 꾸준히 도움을 받으려면 원래 비용이 듭니다. 예를 들어 회당 15만 원짜리 1:1 상담을 한 달에 4번, 1년 동안 받으면 48회, 720만 원입니다.
${PLAN_B}은 149만 원, 그 5분의 1입니다.
(※ 회당 15만 원은 가정 예시이며 시장 평균이 아닙니다. 상담과 코칭은 목적이 다르고, 코칭은 정신건강 치료를 대체하지 않습니다.)`);
    const bars = [["1년 1:1 상담 (가정)", 720, HEX.slate, C.background1], [PLAN_B, 149, HEX.gold, C.accent1]];
    bars.forEach(([label, v, fill, vc], i) => {
      const y = 3.3 + i * 1.5, w = (v / 720) * 6.6;
      T(s, label, { x: 0.8, y, w: 3.3, h: 1.0, fontSize: 20, color: C.accent4, valign: "middle" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.2, y, w, h: 1.0, rectRadius: 0.08, fill: { color: fill }, line: { type: "none" } });
      T(s, v + "만 원", { x: 4.4 + w, y, w: 2.2, h: 1.0, fontSize: 30, bold: true, color: vc, fontFace: HEAD, valign: "middle" });
    });
  }
  {
    const s = slide("LIGHT", "쉽게 말하면", "내 연애 코치를\n고용하는 겁니다",
      `쉽게 말하면, 한 달 10만 원 정도로 1년 동안 내 연애 코치를 고용하는 겁니다.
117만 원을 12개월로 나누면 한 달 약 9만 8천 원. 1:1 상담 한 번 비용보다 적습니다.
소개팅 한 번 나가는 식사비, 카페값만 생각해도 비슷합니다.
그 돈으로 한 달 동안 내 반응을 보고 고쳐주는 사람이 생기는 겁니다.
혼자서 같은 실수를 반복하는 시간과 비용을 생각하면, 투자하지 않을 이유가 없습니다.
(12개월 할부 기준, VAT 별도, 할부 이자는 카드사 기준입니다.)`);
    T(s, "월 9.8만 원", { x: 0.8, y: 3.2, w: 11.7, h: 1.8, fontSize: 96, bold: true, color: C.accent1, fontFace: HEAD, valign: "middle" });
    T(s, "12개월 할부 기준 · VAT 별도", { x: 0.8, y: 5.2, w: 11.7, h: 0.5, fontSize: 18, color: C.accent5 });
  }

  // ============ 신청 ============
  sec("고민 해소 · 신청");
  {
    const s = slide("LIGHT", "솔직하게 말씀드립니다", "이런 분은\n신청하지 마세요",
      `솔직하게 말씀드리겠습니다. 이런 분은 신청하지 마세요.
'한 방 멘트'만 알고 싶은 분. 저는 멘트를 팔지 않습니다.
2주에 과제 하나도 해볼 생각이 없는 분. 부트캠프는 듣기만 하는 강의가 아니라 직접 해보는 훈련입니다.
연애 결과를 보장받고 싶은 분. 저는 지킬 수 있는 것만 약속합니다.
대신, 녹화된 내 모습을 보는 게 불편해도 한번 바꿔보고 싶은 분이라면, 끝까지 함께하겠습니다.`);
    const no = ["멘트만 원하는 분", "실행하지 않을 분", "결과 보장을 원하는 분"];
    for (let i = 0; i < 3; i++) {
      const x = 0.8 + i * 3.97;
      card(s, x, 3.3, 3.65, 2.7);
      await iconCircle(s, x + 0.4, 3.7, 0.9, "LuBan", HEX.redLt, HEX.red);
      T(s, no[i], { x: x + 0.4, y: 4.85, w: 3.0, h: 0.8, fontSize: 22, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
    }
  }
  {
    const s = slide("LIGHT", "이런 고민 있으시죠", "걱정하지 마세요",
      `지금쯤 신청하고는 싶은데, 이런 고민이 드실 거예요.
"저는 원래 말주변이 없는데요." 말을 잘하는 게 목표가 아닙니다. 긴장한 순간의 반응을 바꾸는 겁니다.
"나이가 많은데 될까요?" 태도는 나이와 상관없이, 12주 단위로 바뀝니다.
"연애 경험이 거의 없어요." 그래서 실전 전에 시뮬레이션으로 먼저 연습합니다.
"시간이 없어요." 주당 1~2시간이면 됩니다. 과제를 못 한 주에도 수업은 진행합니다.
걱정하지 마세요. 진단에서 지금의 나를 함께 보고, 할 수 있는 순서대로 계획을 드립니다.`);
    const q = ["말주변이 없어요", "나이가 많아요", "경험이 없어요", "시간이 없어요"];
    for (let i = 0; i < 4; i++) {
      const x = 0.8 + (i % 2) * 5.95, y = 2.9 + Math.floor(i / 2) * 1.75;
      card(s, x, y, 5.75, 1.5);
      await iconCircle(s, x + 0.35, y + 0.3, 0.9, "LuMessageCircle", HEX.bg, HEX.navy);
      T(s, "“" + q[i] + "”", { x: x + 1.55, y, w: 4.0, h: 1.5, fontSize: 26, bold: true, color: C.text2, fontFace: HEAD, valign: "middle" });
    }
  }
  {
    const s = slide("DARK", "지금 바로", "90분 진단부터",
      `지금 바로 90분 진단을 신청하세요.
진단비 [ ]원으로, 내가 어디서 흔들리는지 확인하고 나에게 딱 맞는 12주 계획을 받으실 수 있습니다.
그리고 진단 후, 제가 도와드릴 수 있다고 판단되고 서로 맞는 분께만 부트캠프 합류를 안내드립니다.
그러니 부담 갖지 마시고, 외운 멘트 없이 평소의 나로 편하게 오세요.`);
    const st = [["LuCalendarCheck", "진단"], ["LuClipboardList", "12주 계획"], ["LuHandshake", "합류 결정"]];
    for (let i = 0; i < 3; i++) {
      const x = 0.8 + i * 3.97, on = i === 0;
      card(s, x, 3.0, 3.65, 3.1, on ? C.accent1 : C.accent2);
      await iconCircle(s, x + 0.4, 3.4, 1.0, st[i][0], on ? HEX.navy : HEX.gold, on ? HEX.gold : HEX.navy);
      T(s, String(i + 1).padStart(2, "0"), { x: x + 2.4, y: 3.45, w: 0.9, h: 0.6, fontSize: 28, bold: true, color: on ? C.text2 : C.accent1, align: "right", fontFace: HEAD });
      T(s, st[i][1], { x: x + 0.4, y: 4.75, w: 3.0, h: 0.8, fontSize: 30, bold: true, color: on ? C.text2 : C.background1, fontFace: HEAD, valign: "middle" });
      if (i < 2) s.addImage({ data: await icon("LuArrowRight", HEX.gold), x: x + 3.72, y: 4.4, w: 0.2, h: 0.2 });
    }
  }
  {
    const script = `이미 많은 분들이 이다사에서 달라졌습니다. 그리고 그 시작은 모두 90분 진단이었습니다.
더 이상 새벽까지 소개팅 멘트를 검색하며 지치지 마세요.
이제는 내 모습 그대로, 다음 만남을 잡을 때입니다.
지금 바로 진단을 신청하세요. 감사합니다.`;
    const s = pres.addSlide({ masterName: "COVER", sectionTitle: curSection });
    s.addNotes(script); SCRIPT.push({ section: curSection, script });
    s.addImage({ data: await icon("LuMoon", HEX.navy2), x: 8.6, y: 1.2, w: 5.0, h: 5.0, transparency: 30 });
    T(s, "멘트 검색은\n이제 그만", { x: 0.8, y: 2.0, w: 9, h: 2.4, fontSize: 60, bold: true, color: C.background1, fontFace: HEAD, lineSpacingMultiple: 1.05 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 4.9, w: 4.6, h: 0.9, rectRadius: 0.45, fill: { color: HEX.gold }, line: { type: "none" } });
    T(s, "90분 진단 신청하기", { x: 0.8, y: 4.9, w: 4.6, h: 0.9, fontSize: 22, bold: true, color: C.text2, align: "center", valign: "middle", fontFace: HEAD });
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  fs.writeFileSync(path.join(__dirname, "script.json"), JSON.stringify(SCRIPT, null, 1));
  console.log("wrote", OUT, SCRIPT.length, "slides");
})();
