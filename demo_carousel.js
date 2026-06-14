const pptxgen = require("pptxgenjs");

// ── Palette: Midnight Executive ──
const C = {
  navy:    "1E2761",
  ice:     "CADCFC",
  white:   "FFFFFF",
  dark:    "0D1B5E",
  mid:     "2A3F9F",
  light:   "EEF2FF",
  muted:   "8A94C8",
  accent:  "4ADE80",
  warn:    "F87171",
  amber:   "FBBF24",
};

const makeShadow = () => ({ type: "outer", color: "000000", blur: 8, offset: 3, angle: 45, opacity: 0.18 });

function addTag(slide, text, color, x, y) {
  slide.addShape("roundRect", {
    x, y, w: text.length * 0.095 + 0.3, h: 0.28,
    fill: { color },
    rectRadius: 0.05,
  });
  slide.addText(text, {
    x, y, w: text.length * 0.095 + 0.3, h: 0.28,
    fontSize: 9, bold: true, color: C.white,
    align: "center", valign: "middle", margin: 0,
  });
}

function sectionLabel(slide, text, x, y) {
  slide.addText(text.toUpperCase(), {
    x, y, w: 4, h: 0.22,
    fontSize: 8, bold: true, color: C.muted,
    charSpacing: 3, margin: 0,
  });
}

// ── SLIDE 1: Title ──
function slide1(pres) {
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // Large background circle motif
  s.addShape("ellipse", { x: 6.5, y: -1.5, w: 6, h: 6, fill: { color: C.mid, transparency: 70 } });
  s.addShape("ellipse", { x: 7.5, y: 0.5, w: 3.5, h: 3.5, fill: { color: C.dark, transparency: 50 } });

  // Eyebrow
  s.addText("PORTFOLIO PROJECT", {
    x: 0.6, y: 0.9, w: 4, h: 0.25,
    fontSize: 9, bold: true, color: C.ice,
    charSpacing: 4, margin: 0,
  });

  // Title
  s.addText("🤝 Three Amigos\nSpec Writer", {
    x: 0.6, y: 1.3, w: 7, h: 2.0,
    fontSize: 44, bold: true, color: C.white,
    fontFace: "Calibri",
  });

  // Subtitle
  s.addText("Stress-test your features before you build them.\nThree AI agents. One honest spec.", {
    x: 0.6, y: 3.35, w: 7, h: 0.9,
    fontSize: 15, color: C.ice,
    fontFace: "Calibri",
  });

  // Three agent pills
  const agents = [
    { label: "PM", desc: "Scope & value", color: C.mid },
    { label: "Engineer", desc: "Feasibility & risks", color: "1B5E20" },
    { label: "QA", desc: "Testability", color: "4A148C" },
  ];
  agents.forEach((a, i) => {
    const x = 0.6 + i * 3.1;
    s.addShape("roundRect", { x, y: 4.55, w: 2.8, h: 0.7, fill: { color: a.color }, rectRadius: 0.1 });
    s.addText([
      { text: a.label, options: { bold: true, breakLine: true } },
      { text: a.desc, options: { fontSize: 10 } },
    ], { x, y: 4.55, w: 2.8, h: 0.7, fontSize: 12, color: C.white, align: "center", valign: "middle" });
  });
}

// ── SLIDE 2: The Problem ──
function slide2(pres) {
  const s = pres.addSlide();
  s.background = { color: C.white };

  sectionLabel(s, "The Problem", 0.5, 0.35);
  s.addText("Features get built with incomplete thinking.", {
    x: 0.5, y: 0.65, w: 9, h: 0.7,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri",
  });

  const problems = [
    { icon: "📋", title: "PM", desc: "Misses technical constraints and edge cases" },
    { icon: "⚙️", title: "Engineer", desc: "Over-engineers before scope is agreed" },
    { icon: "🧪", title: "QA", desc: "Finds untestable criteria too late in the sprint" },
  ];

  problems.forEach((p, i) => {
    const y = 1.55 + i * 1.05;
    s.addShape("roundRect", { x: 0.5, y, w: 9, h: 0.88, fill: { color: C.light }, rectRadius: 0.1,
      shadow: makeShadow() });
    s.addText(p.icon, { x: 0.7, y, w: 0.6, h: 0.88, fontSize: 22, valign: "middle", align: "center" });
    s.addText(p.title, { x: 1.4, y: y + 0.08, w: 1.5, h: 0.3, fontSize: 13, bold: true, color: C.navy });
    s.addText(p.desc, { x: 1.4, y: y + 0.42, w: 7.5, h: 0.35, fontSize: 12, color: C.navy });
  });

  s.addText("The Three Amigos practice fixes this — PM, Engineer, and QA challenge a feature together before it's built.", {
    x: 0.5, y: 4.85, w: 9, h: 0.55,
    fontSize: 12, color: C.muted, italic: true,
  });
}

// ── SLIDE 3: Step 1 — Generate Spec ──
function slide3(pres) {
  const s = pres.addSlide();
  s.background = { color: C.white };

  addTag(s, "STEP 1", C.mid, 0.5, 0.3);
  s.addText("Generate Spec", {
    x: 0.5, y: 0.65, w: 9, h: 0.6,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri",
  });

  // Feature brief box
  s.addShape("roundRect", { x: 0.5, y: 1.35, w: 9, h: 0.65, fill: { color: C.light }, rectRadius: 0.08 });
  s.addText([
    { text: "Feature brief: ", options: { bold: true, color: C.navy } },
    { text: "Add a manual time logging field to individual issues so engineers can record hours spent", options: { color: C.navy } },
  ], { x: 0.65, y: 1.35, w: 8.7, h: 0.65, fontSize: 12, valign: "middle" });

  // PM Output
  s.addText("PM Agent Output", { x: 0.5, y: 2.15, w: 9, h: 0.3, fontSize: 13, bold: true, color: C.navy });

  const pmItems = [
    { label: "User story", value: "As an engineering manager, I want engineers to log time on issues so I can track resource allocation." },
    { label: "Key assumption", value: "Engineers will remember to log time manually — unvalidated." },
    { label: "Simpler version", value: "Single optional 'hours spent' field at issue close. Test with 10 engineers for 2 weeks." },
    { label: "Contradiction caught", value: "Feature brief says 'manual' but failure condition says 'if manual, adoption = zero'." },
  ];

  pmItems.forEach((item, i) => {
    const y = 2.55 + i * 0.65;
    s.addText(item.label.toUpperCase(), { x: 0.5, y, w: 2.2, h: 0.25, fontSize: 8, bold: true, color: C.muted, charSpacing: 2 });
    s.addText(item.value, { x: 0.5, y: y + 0.25, w: 9, h: 0.32, fontSize: 11, color: C.navy });
  });
}

// ── SLIDE 4: Step 2 — Review Spec ──
function slide4(pres) {
  const s = pres.addSlide();
  s.background = { color: C.white };

  addTag(s, "STEP 2", "1B5E20", 0.5, 0.3);
  s.addText("Review Spec — Engineer & QA", {
    x: 0.5, y: 0.65, w: 9, h: 0.6,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri",
  });

  const comments = [
    { agent: "ENG", color: "1B5E20", text: "No data model spec — a naive implementation creates N+1 queries on every issue list render." },
    { agent: "ENG", color: "1B5E20", text: "No concurrency control — two engineers logging simultaneously could corrupt the total." },
    { agent: "QA", color: "4A148C", text: "'Standard time formats' is untestable. Is it 1.5h, 1:30, or 90min? Two devs, two implementations." },
    { agent: "QA", color: "4A148C", text: "What happens to time entries if the issue assignee is deleted? No defined behaviour." },
    { agent: "ENG", color: "1B5E20", text: "Permission model undefined — can all team members see each other's logged hours?" },
  ];

  comments.forEach((c, i) => {
    const y = 1.45 + i * 0.75;
    s.addShape("roundRect", { x: 0.5, y, w: 9, h: 0.62, fill: { color: C.light }, rectRadius: 0.08,
      shadow: makeShadow() });
    s.addShape("roundRect", { x: 0.5, y, w: 0.62, h: 0.62, fill: { color: c.color }, rectRadius: 0.08 });
    s.addText(c.agent, { x: 0.5, y, w: 0.62, h: 0.62, fontSize: 9, bold: true, color: C.white, align: "center", valign: "middle", margin: 0 });
    s.addText(c.text, { x: 1.25, y: y + 0.08, w: 8.1, h: 0.48, fontSize: 11, color: C.navy, valign: "middle" });
  });
}

// ── SLIDE 5: Step 3 — Assumption Map ──
function slide5(pres) {
  const s = pres.addSlide();
  s.background = { color: C.white };

  addTag(s, "STEP 3", "4A148C", 0.5, 0.3);
  s.addText("Assumption Map", {
    x: 0.5, y: 0.65, w: 9, h: 0.6,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri",
  });

  s.addText("Top priority:", { x: 0.5, y: 1.35, w: 1.4, h: 0.3, fontSize: 11, bold: true, color: C.navy });
  s.addText("Engineers will log time voluntarily — High criticality, zero evidence. Validate with a 2-week pilot before building.", {
    x: 1.9, y: 1.35, w: 7.5, h: 0.3, fontSize: 11, color: C.navy, italic: true,
  });

  const headers = ["Assumption", "Criticality", "Evidence", "Validate how"];
  const colW = [3.8, 1.3, 1.3, 2.5];
  const rows = [
    ["Engineers remember to log time without prompts", "High", "Low", "2-week pilot, 10 engineers"],
    ["Logged data will be used for decisions", "High", "Low", "Interview 3 engineering managers"],
    ["Manual logging won't feel like surveillance", "High", "Low", "Anonymous survey after pilot"],
    ["Decimal hours is the right unit", "Medium", "Low", "Watch 5 engineers log their first entry"],
  ];

  // Header row
  let x = 0.5;
  headers.forEach((h, i) => {
    s.addShape("roundRect", { x, y: 1.85, w: colW[i], h: 0.32, fill: { color: C.navy }, rectRadius: 0.04 });
    s.addText(h, { x, y: 1.85, w: colW[i], h: 0.32, fontSize: 10, bold: true, color: C.white, align: "center", valign: "middle", margin: 0 });
    x += colW[i] + 0.04;
  });

  rows.forEach((row, ri) => {
    let x = 0.5;
    const y = 2.27 + ri * 0.62;
    const bg = ri % 2 === 0 ? C.light : C.white;
    row.forEach((cell, ci) => {
      const critColor = cell === "High" ? "FEE2E2" : cell === "Medium" ? "FEF9C3" : cell === "Low" ? "DCFCE7" : bg;
      const textColor = cell === "High" ? "991B1B" : cell === "Medium" ? "92400E" : cell === "Low" ? "166534" : C.navy;
      s.addShape("roundRect", { x, y, w: colW[ci], h: 0.52, fill: { color: critColor }, rectRadius: 0.04 });
      s.addText(cell, { x, y, w: colW[ci], h: 0.52, fontSize: 10, color: textColor, align: ci === 0 ? "left" : "center", valign: "middle", margin: ci === 0 ? [0, 0, 0, 8] : 0 });
      x += colW[ci] + 0.04;
    });
  });
}

// ── SLIDE 6: Risk Log ──
function slide6(pres) {
  const s = pres.addSlide();
  s.background = { color: C.white };

  addTag(s, "STEP 3", "B45309", 0.5, 0.3);
  s.addText("Risk Log", {
    x: 0.5, y: 0.65, w: 9, h: 0.6,
    fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri",
  });

  s.addText("🔴 Top priority:", { x: 0.5, y: 1.35, w: 1.6, h: 0.3, fontSize: 11, bold: true, color: C.navy });
  s.addText("Manual logging on a speed-first tool violates Linear's core philosophy. Decide architecture before sprint starts.", {
    x: 2.1, y: 1.35, w: 7.3, h: 0.3, fontSize: 11, color: C.navy, italic: true,
  });

  const risks = [
    { risk: "Engineers don't log time → zero data → feature abandoned", l: "High", i: "High", fix: "Pilot first, measure adoption in week 1" },
    { risk: "Clutter added to issue view slows core workflow", l: "High", i: "High", fix: "Collapsible section, off by default" },
    { risk: "Data used for performance review → engineer resentment", l: "Medium", i: "High", fix: "Explicit data use policy before launch" },
    { risk: "No permission model → all hours visible cross-team", l: "Medium", i: "Medium", fix: "Define visibility rules in acceptance criteria" },
  ];

  risks.forEach((r, i) => {
    const y = 1.82 + i * 0.84;
    s.addShape("roundRect", { x: 0.5, y, w: 9, h: 0.72, fill: { color: C.light }, rectRadius: 0.08, shadow: makeShadow() });

    const lColor = r.l === "High" ? "DC2626" : r.l === "Medium" ? "D97706" : "16A34A";
    s.addText(r.l, { x: 0.6, y: y + 0.08, w: 0.9, h: 0.25, fontSize: 9, bold: true, color: lColor, align: "center" });
    s.addText("likelihood", { x: 0.6, y: y + 0.35, w: 0.9, h: 0.22, fontSize: 8, color: C.muted, align: "center" });

    s.addText(r.risk, { x: 1.65, y: y + 0.06, w: 5.2, h: 0.28, fontSize: 11, bold: true, color: C.navy });
    s.addText("Mitigation: " + r.fix, { x: 1.65, y: y + 0.38, w: 7.2, h: 0.25, fontSize: 10, color: C.muted, italic: true });
  });
}

// ── SLIDE 7: Call to Action ──
function slide7(pres) {
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape("ellipse", { x: -1, y: 3, w: 5, h: 5, fill: { color: C.mid, transparency: 75 } });
  s.addShape("ellipse", { x: 7, y: -1, w: 4, h: 4, fill: { color: C.dark, transparency: 60 } });

  s.addText("Try it yourself.", {
    x: 0.6, y: 1.0, w: 9, h: 0.9,
    fontSize: 40, bold: true, color: C.white, fontFace: "Calibri",
  });

  s.addText("Three Amigos Spec Writer is open source.\nEnter a feature, get a stress-tested spec in seconds.", {
    x: 0.6, y: 2.05, w: 8, h: 0.85,
    fontSize: 15, color: C.ice,
  });

  const links = [
    { icon: "🐙", label: "GitHub", value: "github.com/Michaela2024/three-amigos" },
    { icon: "⚙️", label: "Built with", value: "Python · Streamlit · Claude Sonnet · Anthropic API" },
    { icon: "💡", label: "Try the example", value: "Linear + time tracking feature — see the contradiction the agents catch" },
  ];

  links.forEach((l, i) => {
    const y = 3.1 + i * 0.72;
    s.addText(l.icon + "  " + l.label, { x: 0.6, y, w: 1.8, h: 0.3, fontSize: 11, bold: true, color: C.ice });
    s.addText(l.value, { x: 2.5, y, w: 7, h: 0.3, fontSize: 11, color: C.white });
  });

  s.addText("Built by [Michaela Heigl] · Product leader & builder", {
    x: 0.6, y: 5.1, w: 9, h: 0.3,
    fontSize: 10, color: C.muted, italic: true,
  });
}

// ── Build deck ──
async function buildDeck() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "Three Amigos Spec Writer";
  pres.title = "Three Amigos Spec Writer — LinkedIn Carousel";

  slide1(pres);
  slide2(pres);
  slide3(pres);
  slide4(pres);
  slide5(pres);
  slide6(pres);
  slide7(pres);

  await pres.writeFile({ fileName: "three_amigos_carousel.pptx" });
  console.log("Done — three_amigos_carousel.pptx");
}

buildDeck().catch(console.error);
