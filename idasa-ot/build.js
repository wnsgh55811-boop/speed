// 이다사 12주 부트캠프 OT — 멘토(고파사) VSL 구조 · 진단 + 6단계 커리큘럼
// 색은 4가지만: 오프화이트(배경) · 블랙(글씨) · 연한 그린(약한 강조) · 그린(강조)
// 슬라이드는 핵심만, 설명은 대본(발표자 노트). 반복 문구·페이지 번호 없음.
// run: NODE_PATH=<node_modules> PPTX_SKILL=<pptx skill dir> node build.js  → pptx + script.json
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
const HEX = { paper: "F6F4EE", black: "1A1A1A", mint: "D7E8D5", green: "1F5A43" };
const THEME = {
  name: "이다사", headFontFace: HEAD, bodyFontFace: BODY,
  colors: {
    dk1: HEX.black, lt1: HEX.paper, dk2: HEX.green, lt2: HEX.paper,
    accent1: HEX.green, accent2: HEX.mint, accent3: HEX.green, accent4: HEX.mint,
    accent5: HEX.black, accent6: HEX.mint, hlink: HEX.green, folHlink: HEX.green,
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
const BLACK = C.text1, PAPER = C.background1, GREEN = C.accent1, MINT = C.accent2;

pres.defineSlideMaster({
  title: "PAPER", background: { color: HEX.paper },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.8, y: 0.8, w: 11.7, h: 1.6, fontSize: 38, bold: true, color: BLACK, fontFace: HEAD, margin: 0, valign: "top", align: "left", lineSpacingMultiple: 1.08 }, text: "" } }],
});
pres.defineSlideMaster({ title: "GREEN", background: { color: HEX.green }, objects: [] });

// ---------- helpers ----------
const iconCache = {};
async function icon(name, hex, size = 256) {
  const k = name + hex;
  if (iconCache[k]) return iconCache[k];
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(lu[name], { color: "#" + hex, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).resize(size, size).png().toBuffer();
  return (iconCache[k] = "image/png;base64," + buf.toString("base64"));
}
const T = (s, text, o) => s.addText(text, { isTextBox: true, margin: 0, fontFace: BODY, color: BLACK, fontSize: 20, valign: "top", ...o });
// 카드: soft = 연한 그린 면, strong = 그린 면(글씨 오프화이트), line = 연한 그린 테두리만
function card(s, x, y, w, h, kind = "soft") {
  const fill = kind === "strong" ? HEX.green : kind === "soft" ? HEX.mint : HEX.paper;
  const line = kind === "line" ? { color: HEX.mint, width: 1.5 } : { type: "none" };
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, rectRadius: 0.16, line });
}
async function iconCircle(s, x, y, d, name, onGreen = false) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: onGreen ? HEX.paper : HEX.green }, line: { type: "none" } });
  const p = d * 0.27;
  s.addImage({ data: await icon(name, onGreen ? HEX.green : HEX.paper), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, altText: name });
}
async function slot(s, x, y, w, h, label) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.14, fill: { color: HEX.paper }, line: { color: HEX.green, width: 1.25, dashType: "dash" }, objectName: "교체용 슬롯" });
  T(s, label, { x, y, w, h, fontSize: 14, align: "center", valign: "middle", color: GREEN });
}
function pill(s, x, y, w, text, strong = false, h = 0.5) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: h / 2, fill: { color: strong ? HEX.green : HEX.mint }, line: { type: "none" } });
  T(s, text, { x, y, w, h, fontSize: 16, bold: true, align: "center", valign: "middle", color: strong ? PAPER : BLACK, fontFace: HEAD });
}
const SCRIPT = [];
let curSection = "";
const sec = (t) => { curSection = t; pres.addSection({ title: t }); };
function slide(title, script, master = "PAPER") {
  const s = pres.addSlide({ masterName: master, sectionTitle: curSection });
  if (title) s.addText(title, { placeholder: "title" });
  s.addNotes(script);
  SCRIPT.push({ section: curSection, script });
  return s;
}
const cols3 = (i) => 0.8 + i * 3.97; // 3열 카드 x (w 3.65)
const cols4 = (i) => 0.8 + i * 2.98; // 4열 카드 x (w 2.75)
const PHASES = [
  {
    no: "1단계", weeks: "1~2주", name: "나를 세운다", icon: "LuUser",
    lead: "사람 앞에서 내가 어떻게\n반응하는지 정확히 봅니다",
    learn: "4가지 과잉 · 내 취향 · 만남 환경", task: "GAP NOTE 5일 · 작은 부탁 3번", coach: "내 의견 하나 말하기",
    script: `1단계, 1~2주차는 나를 세우는 단계입니다.
먼저 내가 사람 앞에서 어떻게 반응하는지 정확히 봅니다. 과잉 동의, 과잉 해명, 과잉 질문, 과잉 웃음. 이 4가지 중 나는 어디에 가장 많이 해당하는지 찾습니다.
그리고 내가 무엇을 좋아하는 사람인지, 연애가 없어도 굴러가는 내 삶은 어떤지 정리합니다. 원하는 걸 말하려면, 먼저 말할 재료가 있어야 하니까요.
과제는 GAP NOTE 5일, 그리고 거절당할 수도 있는 작은 부탁 3번입니다. 거절을 당해도 내 가치는 그대로라는 걸, 머리가 아니라 경험으로 확인합니다.
2주차가 끝나면 첫 1:1 코칭에서 '내 의견 하나 말하기'를 역할극으로 연습합니다.`,
  },
  {
    no: "2단계", weeks: "3~4주", name: "흔들리지 않는다", icon: "LuAnchor",
    lead: "상대가 어떤 반응을 해도\n내 행동은 내가 고릅니다",
    learn: "분리 · 공백 · 중심 · 경계선", task: "2초 공백 5번 · 선 긋기 1번", coach: "반대 의견에 해명 없이 답하기",
    script: `2단계, 3~4주차는 흔들리지 않는 단계입니다.
사자의 태도 첫 번째 묶음, 분리·공백·중심·경계선을 배웁니다.
상대가 "그건 좀 별로인데요?" 하고 평가하는 순간, 길게 해명하지 않고 2초 멈춘 뒤 내 생각을 말하는 연습입니다.
과제는 내가 실제로 보낸 카톡에서 과잉 해명 문장을 찾아 고쳐 쓰기, 실제 대화에서 2초 공백 5번, 그리고 선 긋기 1번입니다.
4주차가 끝나면 1:1 코칭에서 반대 의견에 철회하지도, 해명하지도 않고 답하는 연습을 합니다.`,
  },
  {
    no: "3단계", weeks: "5~6주", name: "끌려다니지 않는다", icon: "LuCompass",
    lead: "맞춰주기만 하지 않고\n관계를 같이 만듭니다",
    learn: "투자 · 선택 설계 · 빈틈 · 변주", task: "먼저 제안 5번 · 내 빈틈 이야기", coach: "먼저 제안하기 + 0·6주 영상 비교",
    script: `3단계, 5~6주차는 끌려다니지 않는 단계입니다.
사자의 태도 두 번째 묶음, 투자·선택 설계·빈틈·변주를 배웁니다.
상대에게 맞춰주기만 하는 게 아니라, 관계를 같이 만드는 사람이 됩니다. 다음 만남을 제안하는 기본기가 여기서 만들어집니다.
과제는 메뉴든 장소든 시간이든 일상에서 먼저 제안 5번, 그리고 내 빈틈 이야기 하나를 실제 대화에서 꺼내보는 겁니다.
6주차 코칭에서는 0주차에 찍은 2분 자기소개와 6주차 영상을 나란히 놓고 비교합니다.`,
  },
  {
    no: "4단계", weeks: "7~8주", name: "끌어당긴다", icon: "LuMagnet",
    lead: "나를 보여주면서\n상대와 연결됩니다",
    learn: "주파수 · 서사 · 온도 · 청사진", task: "내 이야기 영상 2편 · 10분 대화", coach: "듣고, 대화 이어가기",
    script: `4단계, 7~8주차는 끌어당기는 단계입니다.
사자의 태도 세 번째 묶음, 주파수·서사·온도·청사진을 배웁니다.
면접관처럼 질문만 던지는 대화가 아니라, 질문 하나에 내 이야기 하나로 대화를 잇습니다. 상대의 속도와 온도를 읽고, 내 이야기를 매력적으로 꺼내는 법을 익힙니다.
과제는 내 이야기를 60~90초 영상으로 2편 찍어보기, 그리고 10분 이상 1:1 대화를 하고 끊긴 지점과 다시 이어진 지점을 복기하는 겁니다.
8주차 코칭에서는 상대 말을 듣고 대화를 이어가는 연습을 합니다.`,
  },
  {
    no: "5단계", weeks: "9~10주", name: "연락 · 소개팅 · 호감 표현", icon: "LuCoffee",
    lead: "배운 태도를\n실제 연락과 만남에 씁니다",
    learn: "첫 연락 · 첫 만남 · 1·2·3차 만남", task: "데이트 코스 답사 · 1·2·3차 시나리오", coach: "소개팅 전체 흐름 + 다음 만남 제안",
    script: `5단계, 9~10주차는 연락, 소개팅, 호감 표현 단계입니다.
1~4단계에서 익힌 태도를 실제 연락과 만남에 적용합니다.
첫 연락은 어떻게 하는지, 첫 만남은 어떻게 흘러가는지, 1차, 2차, 3차 만남은 각각 무엇이 달라야 하는지, 그리고 호감은 어떻게 표현하는지 배웁니다.
과제는 실제로 데려가고 싶은 동네를 직접 걸어보는 데이트 코스 답사, 그리고 1·2·3차 만남 시나리오를 한 장에 정리하는 겁니다.
10주차 코칭에서는 소개팅 전체 흐름을 처음부터 끝까지 해보고, 마지막에 다음 만남을 제안하는 연습까지 합니다.`,
  },
  {
    no: "6단계", weeks: "11~12주", name: "연애 안에서 나를 지킨다", icon: "LuShield",
    lead: "연애가 시작된 뒤에도\n나를 잃지 않습니다",
    learn: "무너지는 이유 · 갈등 · 장기 연애 · 결혼", task: "나의 관계 원칙 7문장", coach: "0·6·12주 비교 + 다음 3개월 계획",
    script: `마지막 6단계, 11~12주차는 연애 안에서 나를 지키는 단계입니다.
많은 분들이 연애를 시작하고 나서 다시 무너집니다. 왜 그런지, 사랑하면서도 나를 잃지 않으려면 어떻게 해야 하는지 배웁니다.
갈등이 생겼을 때 푸는 법, 오래가는 연애, 그리고 결혼과 좋은 파트너까지 다룹니다. 지금 연애 중이 아니어도, 과거 연애나 가까운 관계로 모든 과제를 할 수 있습니다.
마지막 과제는 나만의 관계 원칙 7문장입니다.
12주차 코칭에서는 0주, 6주, 12주 영상을 나란히 놓고 비교하고, 다음 3개월 계획까지 세웁니다.`,
  },
];
const NAV = ["진단", ...PHASES.map((p) => `${p.no} · ${p.name.replace(/ · /g, "·")}`)];
async function navSlide(active, build, script) {
  const s = slide(null, script);
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 4.3, h: 7.5, fill: { color: HEX.mint }, line: { type: "none" } });
  NAV.forEach((t, i) => {
    const y = 1.0 + i * 0.78, on = i === active;
    if (on) s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.4, y, w: 3.5, h: 0.62, rectRadius: 0.31, fill: { color: HEX.green }, line: { type: "none" } });
    T(s, t, { x: 0.68, y, w: 3.2, h: 0.62, fontSize: 15, bold: on, valign: "middle", color: on ? PAPER : BLACK, fontFace: on ? HEAD : BODY });
  });
  await build(s);
}

(async () => {
  // ================= 훅 · 신뢰 =================
  sec("훅 · 신뢰");
  {
    const s = slide(null, `소개팅도 해보고, 썸도 타봤는데, 왜 매번 흐지부지 끝날까요?
좋아하는 여자 앞에서만 이상하게 말이 많아지시나요? 대화는 끊기지 않고 잘 이어간 것 같은데, 이상하게 두 번째 만남은 잡히지 않습니다.
집에 와서 다시 '소개팅 멘트', '애프터 신청 방법'을 검색하고 계시죠.
이 영상을 끝까지 보시면, 더 이상 멘트를 검색하지 않으셔도 됩니다.
왜 매번 흐지부지 끝나는지, 그리고 12주 동안 무엇을 바꾸면 되는지 지금부터 말씀드리겠습니다.`, "GREEN");
    T(s, "왜 매번\n흐지부지 끝나는 걸까요?", { x: 0.8, y: 2.0, w: 11.7, h: 3.5, fontSize: 60, bold: true, color: PAPER, fontFace: HEAD, align: "center", valign: "middle", lineSpacingMultiple: 1.1 });
  }
  {
    const s = slide("연애가 어려운 남성분들만\n코칭해 온 사람입니다",
      `이런 말을 하는 제가 과연 믿을 만한 사람인지 궁금하시죠.
저는 [기간] 동안 6,500건이 넘는 소개팅·연애 고민을 1:1로 상담해 왔습니다.
말로 듣는 상담만 한 게 아닙니다. 실제로 대화를 해보게 하고, 녹화하고, 말투와 표정과 시선을 장면 단위로 다시 봤습니다.
[플랫폼·수상·출간 기록을 한 문장으로.]
그래서 저는 남자들이 어느 순간에 무너지는지, 정확히 알고 있습니다.`);
    T(s, "6,500건", { x: 0.8, y: 4.0, w: 6, h: 1.1, fontSize: 72, bold: true, color: GREEN, fontFace: HEAD, valign: "middle" });
    T(s, "1:1 상담", { x: 0.8, y: 5.2, w: 6, h: 0.5, fontSize: 24 });
    await slot(s, 7.5, 0.8, 5.0, 5.9, "프로필 · 상담 현장 사진");
  }
  {
    const s = slide(null, `그리고 지금도 이런 메시지가 계속 옵니다.
"토요일에 같이 가자고 제가 먼저 말했어요. 예전 같으면 상상도 못 했을 거예요."
"처음으로 소개팅 끝나고 상대가 먼저 연락 왔습니다."
[실제 후기 2~3개를 그대로 읽으세요.]
저에게 오신 분들이 정말 변하지 않았다면, 이런 연락은 오지 않았겠죠.`);
    for (let i = 0; i < 4; i++) await slot(s, cols4(i), 0.8, 2.75, 5.9, "후기 캡처");
  }

  // ================= 문제 · 해법 =================
  sec("문제 · 해법");
  {
    const s = slide(PRODUCT, `${PRODUCT}는 제가 6,500건의 상담과 녹화 복기를 하며 쌓은 방법을 그대로 담은 1:1 훈련 과정입니다.
진단에서 내가 어디서 무너지는지 찾고,
12주 동안 강의 28편과 과제, 그리고 1:1 코칭 6회로 그 태도를 바꾸고,
졸업한 뒤에도 실제 연애에서 평생 점검받습니다.
PDF 받고 영상만 보는 강의가 아닙니다. 직접 해보고, 고치는 부트캠프입니다.`);
    const it = [["LuStethoscope", "진단"], ["LuUserCheck", "1:1 훈련"], ["LuInfinity", "평생 점검"]];
    for (let i = 0; i < 3; i++) {
      const x = cols3(i);
      card(s, x, 2.8, 3.65, 3.4);
      await iconCircle(s, x + 1.2, 3.3, 1.25, it[i][0]);
      T(s, it[i][1], { x, y: 4.85, w: 3.65, h: 0.8, fontSize: 30, bold: true, fontFace: HEAD, align: "center", valign: "middle" });
    }
  }
  {
    const s = slide("멘트가 아니라\n태도를 바꿔야 합니다",
      `제가 수많은 분들을 상담하면서 깨달은 진실이 하나 있습니다.
연애가 서툰 사람일수록, 멘트를 더 외울 게 아니라 '태도'를 바꿔야 한다는 겁니다.
멘트 100개를 외워도, 마음에 드는 여자 앞에서 긴장하는 순간 전부 사라집니다.
하지만 평가받는 순간 2초 멈추고 내 기준을 말하는 태도 하나는, 한 번 몸에 익으면 어떤 상대 앞에서도 남습니다.
멘트 100개보다 태도 하나가 훨씬 쉽고, 훨씬 현실적입니다.`);
    card(s, 0.8, 3.4, 5.6, 2.6, "line");
    T(s, "멘트 100개", { x: 0.8, y: 3.4, w: 5.6, h: 2.6, fontSize: 38, bold: true, fontFace: HEAD, align: "center", valign: "middle" });
    T(s, "<", { x: 6.4, y: 3.4, w: 0.5, h: 2.6, fontSize: 44, bold: true, color: GREEN, align: "center", valign: "middle" });
    card(s, 6.9, 3.4, 5.6, 2.6, "strong");
    T(s, "태도 1가지", { x: 6.9, y: 3.4, w: 5.6, h: 2.6, fontSize: 38, bold: true, color: PAPER, fontFace: HEAD, align: "center", valign: "middle" });
  }
  {
    const s = slide("외운 멘트는\n긴장하면 사라집니다",
      `요즘 '이 멘트만 쓰면 된다', '카톡은 이렇게 보내라'는 강의와 영상이 정말 많습니다.
그런데 상대 반응이 대본과 조금만 달라져도, 다음 말이 막힙니다.
픽업이나 밀당 기술은 연기라서 오래 못 갑니다. 관계가 시작돼도 계속 불안합니다.
유튜브 꿀팁은 보는 순간엔 알 것 같지만, 막상 긴장하면 몸이 안 따라옵니다.
상대가 바뀌어도, 상황이 바뀌어도 남는 건 단 하나, 긴장한 순간에도 무너지지 않는 '내 태도'입니다.`);
    const b = ["멘트 모음", "픽업 기술", "유튜브 꿀팁"];
    for (let i = 0; i < 3; i++) {
      const x = cols3(i);
      card(s, x, 3.3, 3.65, 2.7, "line");
      s.addImage({ data: await icon("LuX", HEX.green), x: x + 0.45, y: 3.7, w: 0.7, h: 0.7 });
      T(s, b[i], { x: x + 0.45, y: 4.8, w: 3.0, h: 0.8, fontSize: 28, bold: true, fontFace: HEAD, valign: "middle" });
    }
  }
  {
    const s = slide("하이에나가 아니라\n사자처럼",
      `이 부트캠프 전체를 한 문장으로 말하면, 하이에나의 반응을 사자의 반응으로 바꾸는 과정입니다.
하이에나는 상대 반응을 먹고 삽니다. 상대가 웃으면 안심하고, 표정이 굳으면 불안해서 점수를 따려고 합니다.
사자는 자기 기준으로 움직입니다. 상대 반응에 흔들리지 않고, 원하는 걸 말하고, 먼저 제안합니다.
사람 앞에서 작아지는 이유는 자신감이 없어서가 아닙니다. 만남을 '심사받는 자리'로 해석하기 때문입니다. 그리고 점수를 따려는 사람에게는 끌리지 않습니다.`);
    card(s, 0.8, 3.1, 5.6, 3.1, "line");
    T(s, "하이에나", { x: 1.3, y: 3.5, w: 4.6, h: 0.7, fontSize: 34, bold: true, fontFace: HEAD, valign: "middle" });
    T(s, "상대 반응을 먹고 산다", { x: 1.3, y: 4.5, w: 4.6, h: 0.5, fontSize: 22 });
    card(s, 6.9, 3.1, 5.6, 3.1, "strong");
    T(s, "사자", { x: 7.4, y: 3.5, w: 4.6, h: 0.7, fontSize: 34, bold: true, color: PAPER, fontFace: HEAD, valign: "middle" });
    T(s, "자기 기준으로 움직인다", { x: 7.4, y: 4.5, w: 4.6, h: 0.5, fontSize: 22, color: PAPER });
  }
  {
    const s = slide("긴장하면 나오는\n4가지 과잉",
      `혹시 이 중에 해당하는 게 있으신가요?
과잉 동의. 상대가 뭘 말해도 "저도요, 저도요" 합니다.
과잉 해명. "아, 그런 뜻이 아니라…" 하면서 길게 설명합니다.
과잉 질문. 대화가 끊길까 봐 면접관처럼 질문만 던집니다.
과잉 웃음. 긴장해서 계속 웃습니다.
이 4가지는 모두 상대에게 점수를 따려는 하이에나의 반응입니다. 그리고 부트캠프에서는 각각을 사자의 태도로 하나씩 고칩니다.`);
    const q = [["과잉 동의", "“저도요, 저도요”"], ["과잉 해명", "“그런 뜻이 아니라”"], ["과잉 질문", "“취미가 뭐예요?”"], ["과잉 웃음", "“하하… 하하”"]];
    q.forEach(([name, quote], i) => {
      const x = cols4(i);
      card(s, x, 3.1, 2.75, 3.1);
      T(s, name, { x: x + 0.3, y: 3.45, w: 2.2, h: 0.6, fontSize: 26, bold: true, color: GREEN, fontFace: HEAD, valign: "middle" });
      T(s, quote, { x: x + 0.25, y: 4.35, w: 2.35, h: 1.4, fontSize: 17 });
    });
  }
  {
    const s = slide("사자의 태도 12가지",
      `12주 동안 익히는 건 바로 이 사자의 태도 12가지입니다.
첫 번째 묶음은 흔들리지 않는 태도. 분리, 공백, 중심, 경계선입니다.
두 번째 묶음은 끌려다니지 않는 태도. 투자, 선택 설계, 빈틈, 변주입니다.
세 번째 묶음은 끌어당기는 태도. 주파수, 서사, 온도, 청사진입니다.
지금은 단어가 낯설어도 괜찮습니다. 강의 하나에 과제 하나씩, 하나하나 몸으로 익히게 됩니다.`);
    const g = [["흔들리지 않는다", ["분리", "공백", "중심", "경계선"]], ["끌려다니지 않는다", ["투자", "선택 설계", "빈틈", "변주"]], ["끌어당긴다", ["주파수", "서사", "온도", "청사진"]]];
    g.forEach(([name, items], i) => {
      const x = cols3(i);
      card(s, x, 2.7, 3.65, 3.6, "line");
      T(s, name, { x: x + 0.4, y: 3.05, w: 3.0, h: 0.6, fontSize: 24, bold: true, color: GREEN, fontFace: HEAD, valign: "middle" });
      items.forEach((t, j) => pill(s, x + 0.4 + (j % 2) * 1.47, 4.05 + Math.floor(j / 2) * 0.9, 1.35, t, false, 0.64));
    });
  }

  // ================= 커리큘럼 =================
  sec("커리큘럼");
  {
    const s = slide("진단 + 6단계",
      `${PRODUCT}는 진단으로 시작해서, 2주씩 6단계로 진행됩니다.
1단계 나를 세운다, 2단계 흔들리지 않는다, 3단계 끌려다니지 않는다,
4단계 끌어당긴다, 5단계 연락·소개팅·호감 표현, 그리고 6단계 연애 안에서 나를 지킨다.
앞의 네 단계에서 태도를 만들고, 뒤의 두 단계에서 실제 만남과 연애에 씁니다.
하나씩 보여드리겠습니다.`);
    PHASES.forEach((p, i) => {
      const x = cols3(i % 3), y = 2.6 + Math.floor(i / 3) * 2.05;
      const strong = i >= 4;
      card(s, x, y, 3.65, 1.85, strong ? "strong" : "soft");
      T(s, `${p.no} · ${p.weeks}`, { x: x + 0.35, y: y + 0.3, w: 3.0, h: 0.4, fontSize: 16, bold: true, color: strong ? PAPER : GREEN, fontFace: HEAD, valign: "middle" });
      T(s, p.name.replace(/ · /g, "·"), { x: x + 0.35, y: y + 0.8, w: 3.1, h: 0.75, fontSize: p.name.length > 9 ? 21 : 24, bold: true, color: strong ? PAPER : BLACK, fontFace: HEAD, valign: "middle" });
    });
  }
  await navSlide(0, async (s) => {
    T(s, "진단 90분", { x: 4.9, y: 1.0, w: 7.6, h: 0.9, fontSize: 44, bold: true, fontFace: HEAD, valign: "middle" });
    T(s, "내가 어디서 무너지는지 찾고,\n나만의 12주 계획을 받습니다", { x: 4.9, y: 2.1, w: 7.6, h: 1.1, fontSize: 22, lineSpacingMultiple: 1.15 });
    const st = [["LuVideo", "실제 상황\n시뮬레이션"], ["LuEye", "녹화 장면\n복기"], ["LuClipboardList", "12주\n개인 계획"]];
    for (let i = 0; i < 3; i++) {
      const x = 4.9 + i * 2.6;
      card(s, x, 3.9, 2.4, 2.5);
      await iconCircle(s, x + 0.35, 4.2, 0.8, st[i][0]);
      T(s, st[i][1], { x: x + 0.35, y: 5.2, w: 1.9, h: 0.9, fontSize: 17, bold: true, fontFace: HEAD });
    }
  }, `먼저 시작 전에, 90분 진단을 받습니다.
AI 여성 영상과 실제 상황처럼 대화를 해봅니다. 첫 만남 장면, 두 번째 만남 장면을 직접 해보고 녹화합니다.
그리고 녹화된 장면을 같이 보면서 확인합니다. 4가지 과잉 중 어디에 해당하는지, 말을 서두르는지, 시선이 빠지는지.
진단이 끝나면 바꿀 것, 새로 만들 것, 지킬 것이 정리된 나만의 12주 계획을 받습니다.`);
  for (let i = 0; i < PHASES.length; i++) {
    const p = PHASES[i];
    await navSlide(i + 1, async (s) => {
      pill(s, 4.9, 1.0, 2.6, `${p.no} · ${p.weeks}`);
      T(s, p.name, { x: 4.9, y: 1.7, w: 7.6, h: 0.9, fontSize: p.name.length > 9 ? 36 : 42, bold: true, fontFace: HEAD, valign: "middle" });
      T(s, p.lead, { x: 4.9, y: 2.75, w: 7.6, h: 1.0, fontSize: 21, lineSpacingMultiple: 1.15 });
      const rows = [["배우는 것", p.learn], ["대표 과제", p.task], ["1:1 코칭", p.coach]];
      rows.forEach(([k, v], r) => {
        const y = 4.1 + r * 0.92;
        card(s, 4.9, y, 7.65, 0.78);
        T(s, k, { x: 5.2, y, w: 1.7, h: 0.78, fontSize: 16, bold: true, color: GREEN, fontFace: HEAD, valign: "middle" });
        T(s, v, { x: 6.9, y, w: 5.5, h: 0.78, fontSize: 17, valign: "middle" });
      });
    }, p.script);
  }
  {
    const s = slide("한 단계 = 2주,\n이렇게 돌아갑니다",
      `한 단계는 2주입니다. 2주 동안 이렇게 돌아갑니다.
강의를 봅니다. 강의는 총 28편이고, 강의 하나에 과제가 하나씩 있습니다.
매일 1분, 자세와 시선, 말속도를 연습합니다. 단계마다 집중 포인트가 바뀝니다.
실전 과제를 일상에서 직접 해봅니다.
주말마다 GAP NOTE를 한 장 씁니다. 원래 하고 싶었던 것과 실제로 한 것의 차이를 적는 겁니다.
그리고 단계가 끝나면 셀프 점검을 하고, 바로 1:1 코칭 90분을 받습니다. 90분 중 대부분이 실제 연습입니다.
주당 1~2시간이면 충분합니다.`);
    const fl = [["LuMonitorPlay", "강의"], ["LuTimer", "매일 1분"], ["LuFootprints", "실전 과제"], ["LuNotebookPen", "GAP NOTE"], ["LuUsers", "1:1 코칭"]];
    for (let i = 0; i < fl.length; i++) {
      const x = 0.8 + i * 2.4, last = i === fl.length - 1;
      card(s, x, 3.3, 2.1, 2.7, last ? "strong" : "soft");
      await iconCircle(s, x + 0.6, 3.7, 0.9, fl[i][0], last);
      T(s, fl[i][1], { x, y: 4.9, w: 2.1, h: 0.6, fontSize: 20, bold: true, color: last ? PAPER : BLACK, fontFace: HEAD, align: "center", valign: "middle" });
    }
  }
  {
    const s = slide("1:1 코칭 6회,\n2주마다 직접 해보고 고칩니다",
      `1:1 코칭은 12주 동안 6회, 단계가 끝날 때마다 90분씩 진행합니다.
2주차에는 내 의견 하나 말하기, 4주차에는 반대 의견에 해명 없이 답하기,
6주차에는 먼저 제안하기와 중간 영상 비교, 8주차에는 듣고 대화 이어가기,
10주차에는 소개팅 전체 흐름과 다음 만남 제안, 12주차에는 최종 영상 비교와 다음 3개월 계획입니다.
듣기만 하는 시간이 아닙니다. 역할극을 하고, 가장 중요한 한두 가지만 피드백 받고, 같은 장면을 다시 해봅니다. 녹화본도 드립니다.`);
    s.addShape(pres.shapes.LINE, { x: 1.4, y: 4.0, w: 10.5, h: 0, line: { color: HEX.mint, width: 3 } });
    const tl = [["2주", "의견 말하기"], ["4주", "해명 없이 답하기"], ["6주", "먼저 제안하기"], ["8주", "대화 이어가기"], ["10주", "소개팅 전체 흐름"], ["12주", "최종 비교"]];
    tl.forEach(([w, t], i) => {
      const cx = 1.4 + i * 2.1;
      s.addShape(pres.shapes.OVAL, { x: cx - 0.2, y: 3.8, w: 0.4, h: 0.4, fill: { color: i === 5 ? HEX.green : HEX.mint }, line: { type: "none" } });
      T(s, w, { x: cx - 0.9, y: 4.45, w: 1.8, h: 0.55, fontSize: 24, bold: true, color: GREEN, fontFace: HEAD, align: "center", valign: "middle" });
      T(s, t, { x: cx - 1.0, y: 5.1, w: 2.0, h: 0.8, fontSize: 16, align: "center" });
    });
  }
  {
    const s = slide("0 · 6 · 12주,\n같은 조건으로 비교합니다",
      `좋아진 것 같다는 느낌만으로 판단하지 않습니다.
시작하는 날, 2분 자기소개 영상을 찍습니다. 그리고 6주차와 12주차에 똑같은 질문, 똑같은 조건으로 다시 찍습니다.
세 영상을 나란히 놓고 보면, 말속도, 시선, 해명하는 습관이 어떻게 달라졌는지 내 눈으로 확인할 수 있습니다.
(결과는 실행에 따라 다르며, 연애 결과를 보장하지는 않습니다.)`);
    const v = ["0주", "6주", "12주"];
    for (let i = 0; i < 3; i++) {
      const x = cols3(i), last = i === 2;
      card(s, x, 3.1, 3.65, 2.4, last ? "strong" : "soft");
      s.addImage({ data: await icon("LuCirclePlay", last ? HEX.paper : HEX.green), x: x + 1.37, y: 3.85, w: 0.9, h: 0.9 });
      T(s, v[i], { x, y: 5.75, w: 3.65, h: 0.6, fontSize: 28, bold: true, color: GREEN, fontFace: HEAD, align: "center", valign: "middle" });
    }
  }
  {
    const s = slide("12주 뒤,\n이 세 가지를 합니다",
      `정리하면, ${PRODUCT}는 진단부터 실제 연애가 시작될 때까지 A부터 Z까지 함께하는 과정입니다.
28편의 강의와 28개의 과제는 모두 이 세 가지 중 하나로 이어집니다.
원하는 걸 말합니다. 내 이야기로 대화를 잇습니다. 그리고 다음 만남을 먼저 제안합니다.
단언컨대, 내 녹화 영상을 장면 단위로 보면서 태도 자체를 고쳐주는 1:1 연애 훈련은 흔하지 않습니다.`);
    const g = ["원하는 걸\n말한다", "내 이야기로\n대화를 잇는다", "다음 만남을\n제안한다"];
    for (let i = 0; i < 3; i++) {
      const x = cols3(i);
      card(s, x, 3.1, 3.65, 3.0, "strong");
      T(s, String(i + 1).padStart(2, "0"), { x: x + 0.45, y: 3.45, w: 2, h: 0.6, fontSize: 26, bold: true, color: MINT, fontFace: HEAD, valign: "middle" });
      T(s, g[i], { x: x + 0.45, y: 4.3, w: 3.0, h: 1.3, fontSize: 26, bold: true, color: PAPER, fontFace: HEAD, valign: "middle" });
    }
  }

  // ================= 구조 · 가격 =================
  sec("구조 · 가격");
  {
    const s = slide("무조건 1:1로만",
      `여러분, 연애 강의를 듣기만 해서 바뀐다면, 강의를 가장 많이 들은 사람이 연애를 제일 잘했어야 합니다. 그렇죠?
대부분의 연애 강의는 영상을 보거나 단체로 수업을 듣고 끝납니다. 내 말투, 내 표정, 내 시선을 봐주는 사람은 없습니다.
그리고 4주, 8주 지나면 끝납니다.
그래서 ${PRODUCT}는 무조건 1:1로만 진행합니다. 내 영상을 장면 단위로 보면서 고치고, 졸업한 뒤에도 평생 점검합니다.`);
    card(s, 0.8, 2.8, 5.6, 3.4, "line");
    T(s, "듣는 강의", { x: 1.3, y: 3.4, w: 4.8, h: 0.8, fontSize: 34, bold: true, fontFace: HEAD, valign: "middle" });
    T(s, "VOD · 단체 · 4~8주", { x: 1.3, y: 4.5, w: 4.8, h: 0.5, fontSize: 22 });
    card(s, 6.9, 2.8, 5.6, 3.4, "strong");
    T(s, "1:1 교정", { x: 7.4, y: 3.4, w: 4.8, h: 0.8, fontSize: 34, bold: true, color: PAPER, fontFace: HEAD, valign: "middle" });
    T(s, "녹화 복기 · 12주 + 평생", { x: 7.4, y: 4.5, w: 4.8, h: 0.5, fontSize: 22, color: PAPER });
  }
  {
    const s = slide("진짜 연애는\n12주 뒤에 시작됩니다",
      `부트캠프는 크게 두 구간으로 나뉩니다.
첫 번째 구간은 12주 집중 구간입니다. 강의 28편, 매일 루틴, 실전 과제, 그리고 1:1 코칭 6회로 태도를 바꿉니다.
이 집중 구간이 없으면, 대부분 아무것도 안 하고 흐지부지됩니다. 그래서 12주 안에 반드시 바꾸는 걸 목표로 달립니다.
두 번째 구간은 졸업 후 평생 회원 구간입니다.
진짜 연애는 12주 뒤에 시작됩니다. 썸이 생겼을 때, 연애가 시작됐을 때, 같은 문제로 다툴 때, 결혼을 고민할 때, 그때마다 돌아와서 점검받으시면 됩니다.
매달 사례 라이브, 게시판 주 1회 답변, 6개월 영상 점검, 1년 안 1:1 점검 1회가 포함됩니다.
[실제 사례 하나를 짧게: 연애 시작 후 고민이 생긴 수강생을 어떻게 도왔는지.]`);
    [[0.8, "1구간 · 12주", "집중 부트캠프", true], [6.9, "2구간 · 졸업 후", "평생 회원", false]].forEach(([x, tag, name, strong]) => {
      card(s, x, 3.1, 5.6, 3.0, strong ? "strong" : "soft");
      T(s, tag, { x: x + 0.5, y: 3.5, w: 4.8, h: 0.5, fontSize: 20, bold: true, color: strong ? MINT : GREEN, fontFace: HEAD, valign: "middle" });
      T(s, name, { x: x + 0.5, y: 4.3, w: 4.8, h: 1.0, fontSize: 38, bold: true, color: strong ? PAPER : BLACK, fontFace: HEAD, valign: "middle" });
    });
  }
  {
    const s = slide("두 가지 중 하나",
      `가격은 화면에 보이는 그대로입니다.
${PLAN_A}는 117만 원, 12개월 할부로 한 달 약 9만 8천 원입니다.
${PLAN_B}은 149만 원, 한 달 약 12만 4천 원입니다.
32만 원 차이로 졸업 뒤에도 라이브, 게시판 답변, 반년 점검, 1:1 점검이 평생 이어집니다.
모두 VAT 별도이고, 환불 규정은 결제 단계에서 안내드립니다.
혹시 가격을 보고 비싸다는 생각이 드셨나요?`);
    [[0.8, PLAN_A, "117만 원", false], [6.9, PLAN_B, "149만 원", true]].forEach(([x, n, p, strong]) => {
      card(s, x, 2.6, 5.6, 3.6, strong ? "strong" : "line");
      if (strong) pill(s, x + 4.05, 2.95, 1.25, "추천", false, 0.46);
      T(s, n, { x: x + 0.5, y: 2.95, w: 3.5, h: 0.5, fontSize: 22, bold: true, color: strong ? PAPER : BLACK, fontFace: HEAD, valign: "middle" });
      T(s, p, { x: x + 0.5, y: 3.8, w: 4.8, h: 1.3, fontSize: 64, bold: true, color: strong ? PAPER : GREEN, fontFace: HEAD, valign: "middle" });
      T(s, "VAT 별도", { x: x + 0.5, y: 5.4, w: 4.8, h: 0.4, fontSize: 16, color: strong ? PAPER : BLACK });
    });
  }
  {
    const s = slide("1년 상담의 5분의 1",
      `아니요, 오히려 저렴합니다.
1:1로 꾸준히 도움을 받으려면 원래 비용이 듭니다. 예를 들어 회당 15만 원짜리 1:1 상담을 한 달에 4번, 1년 동안 받으면 48회, 720만 원입니다.
${PLAN_B}은 149만 원, 그 5분의 1입니다.
(※ 회당 15만 원은 가정 예시이며 시장 평균이 아닙니다. 상담과 코칭은 목적이 다르고, 코칭은 정신건강 치료를 대체하지 않습니다.)`);
    [["1년 1:1 상담 (가정)", 720, HEX.mint, BLACK], [PLAN_B, 149, HEX.green, GREEN]].forEach(([label, v, fill, vc], i) => {
      const y = 3.0 + i * 1.6, w = (v / 720) * 5.8;
      T(s, label, { x: 0.8, y, w: 3.4, h: 1.05, fontSize: 21, valign: "middle" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.3, y, w, h: 1.05, rectRadius: 0.1, fill: { color: fill }, line: { type: "none" } });
      T(s, v + "만 원", { x: 4.5 + w, y, w: 2.2, h: 1.05, fontSize: 32, bold: true, color: vc, fontFace: HEAD, valign: "middle" });
    });
  }
  {
    const s = slide("내 연애 코치를\n고용하는 겁니다",
      `쉽게 말하면, 한 달 10만 원 정도로 1년 동안 내 연애 코치를 고용하는 겁니다.
117만 원을 12개월로 나누면 한 달 약 9만 8천 원. 1:1 상담 한 번 비용보다 적습니다.
소개팅 한 번 나가는 식사비, 카페값만 생각해도 비슷합니다.
그 돈으로 한 달 동안 내 태도를 보고 고쳐주는 사람이 생기는 겁니다.
혼자서 같은 실수를 반복하는 시간과 비용을 생각하면, 투자하지 않을 이유가 없습니다.
(12개월 할부 기준, VAT 별도, 할부 이자는 카드사 기준입니다.)`);
    T(s, "월 9.8만 원", { x: 0.8, y: 3.2, w: 11.7, h: 1.8, fontSize: 100, bold: true, color: GREEN, fontFace: HEAD, valign: "middle" });
    T(s, `${PLAN_A} · 12개월 할부 기준 · VAT 별도`, { x: 0.8, y: 5.2, w: 11.7, h: 0.5, fontSize: 18 });
  }

  // ================= 고민 해소 · 신청 =================
  sec("고민 해소 · 신청");
  {
    const s = slide("이런 분은\n신청하지 마세요",
      `솔직하게 말씀드리겠습니다. 이런 분은 신청하지 마세요.
'한 방 멘트'만 알고 싶은 분. 저는 멘트를 팔지 않습니다.
2주에 과제 하나도 해볼 생각이 없는 분. 부트캠프는 듣기만 하는 강의가 아니라 직접 해보는 훈련입니다. 강의 하나에 과제 하나, 전부 필수입니다.
연애 결과를 보장받고 싶은 분. 저는 지킬 수 있는 것만 약속합니다.
대신, 녹화된 내 모습을 보는 게 불편해도 한번 바꿔보고 싶은 분이라면, 끝까지 함께하겠습니다.`);
    const no = ["멘트만\n원하는 분", "실행하지\n않을 분", "결과 보장을\n원하는 분"];
    for (let i = 0; i < 3; i++) {
      const x = cols3(i);
      card(s, x, 3.1, 3.65, 3.0, "line");
      s.addImage({ data: await icon("LuBan", HEX.green), x: x + 0.45, y: 3.5, w: 0.7, h: 0.7 });
      T(s, no[i], { x: x + 0.45, y: 4.5, w: 3.0, h: 1.2, fontSize: 26, bold: true, fontFace: HEAD, valign: "middle" });
    }
  }
  {
    const s = slide("걱정하지 마세요",
      `지금쯤 신청하고는 싶은데, 이런 고민이 드실 거예요.
"저는 원래 말주변이 없는데요." 말을 잘하는 게 목표가 아닙니다. 긴장한 순간의 태도를 바꾸는 겁니다.
"나이가 많은데 될까요?" 태도는 나이와 상관없이, 12주 단위로 바뀝니다.
"연애 경험이 거의 없어요." 그래서 실전 전에 시뮬레이션으로 먼저 연습하고, 지금 연애 중이 아니어도 모든 과제를 할 수 있게 만들었습니다.
"시간이 없어요." 주당 1~2시간이면 됩니다. 과제를 못 한 주에도 코칭은 진행합니다.
걱정하지 마세요. 진단에서 지금의 나를 함께 보고, 할 수 있는 순서대로 계획을 드립니다.`);
    const q = ["말주변이 없어요", "나이가 많아요", "경험이 없어요", "시간이 없어요"];
    q.forEach((t, i) => {
      const x = 0.8 + (i % 2) * 5.95, y = 2.6 + Math.floor(i / 2) * 1.9;
      card(s, x, y, 5.75, 1.6);
      T(s, "“" + t + "”", { x: x + 0.5, y, w: 5.0, h: 1.6, fontSize: 28, bold: true, fontFace: HEAD, valign: "middle" });
    });
  }
  {
    const s = slide("90분 진단부터",
      `지금 바로 90분 진단을 신청하세요.
진단비는 5만 원입니다. 5만 원으로, 내가 어디서 흔들리는지 확인하고 나에게 딱 맞는 12주 계획을 받으실 수 있습니다.
그리고 진단 후, 제가 도와드릴 수 있다고 판단되고 서로 맞는 분께만 부트캠프 합류를 안내드립니다.
그러니 부담 갖지 마시고, 외운 멘트 없이 평소의 나로 편하게 오세요.`);
    const st = [["01", "진단", "5만 원"], ["02", "12주 계획", null], ["03", "합류 결정", null]];
    st.forEach(([n, t, sub], i) => {
      const x = cols3(i), strong = i === 0;
      card(s, x, 2.8, 3.65, 3.3, strong ? "strong" : "soft");
      T(s, n, { x: x + 0.45, y: 3.2, w: 2, h: 0.6, fontSize: 28, bold: true, color: strong ? MINT : GREEN, fontFace: HEAD, valign: "middle" });
      T(s, t, { x: x + 0.45, y: 4.3, w: 3.0, h: 0.8, fontSize: 32, bold: true, color: strong ? PAPER : BLACK, fontFace: HEAD, valign: "middle" });
      if (sub) T(s, sub, { x: x + 0.45, y: 5.1, w: 3.0, h: 0.6, fontSize: 22, color: PAPER, valign: "middle" });
    });
  }
  {
    const s = slide(null, `이미 많은 분들이 이다사에서 달라졌습니다. 그리고 그 시작은 모두 90분 진단이었습니다.
더 이상 새벽까지 소개팅 멘트를 검색하며 지치지 마세요.
이제는 내 모습 그대로, 다음 만남을 잡을 때입니다.
지금 바로 진단을 신청하세요. 감사합니다.`, "GREEN");
    T(s, "멘트 검색은\n이제 그만하셔도 됩니다", { x: 0.8, y: 1.8, w: 11.7, h: 2.8, fontSize: 56, bold: true, color: PAPER, fontFace: HEAD, align: "center", valign: "middle", lineSpacingMultiple: 1.1 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.37, y: 5.0, w: 4.6, h: 0.9, rectRadius: 0.45, fill: { color: HEX.mint }, line: { type: "none" } });
    T(s, "90분 진단 신청하기", { x: 4.37, y: 5.0, w: 4.6, h: 0.9, fontSize: 22, bold: true, align: "center", valign: "middle", fontFace: HEAD });
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  fs.writeFileSync(path.join(__dirname, "script.json"), JSON.stringify(SCRIPT, null, 1));
  console.log("wrote", OUT, SCRIPT.length, "slides");
})();
