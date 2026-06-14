const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const payload = JSON.parse(fs.readFileSync("demo_data/payload.json", "utf8"));
const { pm, eng, synthesis, assumptions, risks, screenshots } = payload;

const C = {
  navy:  "1E2761",
  ice:   "CADCFC",
  white: "FFFFFF",
  dark:  "0D1B5E",
  mid:   "2A3F9F",
  light: "EEF2FF",
  muted: "8A94C8",
};

const makeShadow = () => ({ type: "outer", color: "000000", blur: 8, offset: 3, angle: 45, opacity: 0.18 });

function addTag(slide, text, color, x, y) {
  slide.addShape("roundRect", { x, y, w: 1.1, h: 0.28, fill: { color }, rectRadius: 0.05 });
  slide.addText(text, { x, y, w: 1.1, h: 0.28, fontSize: 9, bold: true, color: C.white, align: "center", valign: "middle", margin: 0 });
}

function imgBase64(imgPath) {
  const ext = path.extname(imgPath).slice(1).toLowerCase();
  const mime = ext === "jpg" ? "jpeg" : ext;
  const data = fs.readFileSync(imgPath).toString("base64");
  return `image/${mime};base64,${data}`;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// ── SLIDE 1: Title ──
{
  const s = pres.addSlide();
  s.background = { color: C.navy };
  s.addShape("ellipse", { x: 6.5, y: -1.5, w: 6, h: 6, fill: { color: C.mid, transparency: 70 } });
  s.addText("PORTFOLIO PROJECT", { x: 0.6, y: 0.9, w: 4, h: 0.25, fontSize: 9, bold: true, color: C.ice, charSpacing: 4, margin: 0 });
  s.addText("Three Amigos\nSpec Writer", { x: 0.6, y: 1.3, w: 7, h: 2.0, fontSize: 44, bold: true, color: C.white, fontFace: "Calibri" });
  s.addText("Stress-test your features before you build them.\nThree AI agents. One honest spec.", { x: 0.6, y: 3.35, w: 7, h: 0.9, fontSize: 15, color: C.ice });
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
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addText("THE PROBLEM", { x: 0.5, y: 0.35, w: 4, h: 0.22, fontSize: 8, bold: true, color: C.muted, charSpacing: 3, margin: 0 });
  s.addText("Features get built with incomplete thinking.", { x: 0.5, y: 0.65, w: 9, h: 0.7, fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri" });
  const problems = [
    { icon: "📋", title: "PM", desc: "Misses technical constraints and edge cases" },
    { icon: "⚙️", title: "Engineer", desc: "Over-engineers before scope is agreed" },
    { icon: "🧪", title: "QA", desc: "Finds untestable criteria too late in the sprint" },
  ];
  problems.forEach((p, i) => {
    const y = 1.55 + i * 1.05;
    s.addShape("roundRect", { x: 0.5, y, w: 9, h: 0.88, fill: { color: C.light }, rectRadius: 0.1, shadow: makeShadow() });
    s.addText(p.icon, { x: 0.7, y, w: 0.6, h: 0.88, fontSize: 22, valign: "middle", align: "center" });
    s.addText(p.title, { x: 1.4, y: y + 0.08, w: 1.5, h: 0.3, fontSize: 13, bold: true, color: C.navy });
    s.addText(p.desc, { x: 1.4, y: y + 0.42, w: 7.5, h: 0.35, fontSize: 12, color: C.navy });
  });
  s.addText("The Three Amigos practice fixes this — PM, Engineer, and QA challenge a feature together before it's built.", {
    x: 0.5, y: 4.85, w: 9, h: 0.55, fontSize: 12, color: C.muted, italic: true,
  });
}

// ── SLIDE 3: Screenshot — UI landing ──
{
  const s = pres.addSlide();
  s.background = { color: C.navy };
  s.addText("THE TOOL", { x: 0.5, y: 0.25, w: 4, h: 0.22, fontSize: 8, bold: true, color: C.ice, charSpacing: 3, margin: 0 });
  s.addText("A three-tab workflow — Generate, Review, Artefacts", { x: 0.5, y: 0.55, w: 9, h: 0.45, fontSize: 20, bold: true, color: C.white, fontFace: "Calibri" });
  s.addImage({ data: imgBase64(screenshots.landing), x: 0.5, y: 1.1, w: 9, h: 4.3, sizing: { type: "contain", w: 9, h: 4.3 } });
}

// ── SLIDE 4: Screenshot — Feature entered ──
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTag(s, "STEP 1", C.mid, 0.5, 0.3);
  s.addText("Enter your feature brief", { x: 0.5, y: 0.65, w: 9, h: 0.5, fontSize: 24, bold: true, color: C.navy, fontFace: "Calibri" });
  s.addImage({ data: imgBase64(screenshots.feature), x: 0.5, y: 1.25, w: 9, h: 4.1, sizing: { type: "contain", w: 9, h: 4.1 } });
}

// ── SLIDE 5: Screenshot — Context filled ──
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTag(s, "STEP 1", C.mid, 0.5, 0.3);
  s.addText("Add product context — the agents work harder with it", { x: 0.5, y: 0.65, w: 9, h: 0.5, fontSize: 24, bold: true, color: C.navy, fontFace: "Calibri" });
  s.addImage({ data: imgBase64(screenshots.context), x: 0.5, y: 1.25, w: 9, h: 4.1, sizing: { type: "contain", w: 9, h: 4.1 } });
}

// ── SLIDE 6: PM Output ──
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTag(s, "PM AGENT", C.mid, 0.5, 0.3);
  s.addText("Scopes the feature and challenges its own assumptions", { x: 0.5, y: 0.65, w: 9, h: 0.5, fontSize: 24, bold: true, color: C.navy, fontFace: "Calibri" });

  const items = [
    { label: "USER STORY", value: pm.user_story || "" },
    { label: "CONTRADICTION CAUGHT", value: "Feature says 'manual' but failure condition says 'if manual, adoption = zero'" },
    { label: "SIMPLER VERSION", value: pm.simpler_version || "" },
    { label: "KEY ASSUMPTION", value: (pm.assumptions || [])[0] || "" },
  ];

  items.forEach((item, i) => {
    const y = 1.35 + i * 0.98;
    s.addShape("roundRect", { x: 0.5, y, w: 9, h: 0.82, fill: { color: C.light }, rectRadius: 0.08, shadow: makeShadow() });
    s.addText(item.label, { x: 0.7, y: y + 0.06, w: 8.5, h: 0.22, fontSize: 8, bold: true, color: C.muted, charSpacing: 2 });
    s.addText(item.value, { x: 0.7, y: y + 0.32, w: 8.5, h: 0.42, fontSize: 11, color: C.navy, valign: "middle" });
  });
}

// ── SLIDE 7: Engineer + QA ──
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTag(s, "STEP 2", "1B5E20", 0.5, 0.3);
  s.addText("Engineer & QA stress-test the spec", { x: 0.5, y: 0.65, w: 9, h: 0.5, fontSize: 24, bold: true, color: C.navy, fontFace: "Calibri" });

  const comments = [
    { agent: "ENG", color: "1B5E20", text: (eng.challenges || [])[0]?.issue || "" },
    { agent: "ENG", color: "1B5E20", text: (eng.challenges || [])[1]?.issue || "" },
    { agent: "QA",  color: "4A148C", text: (eng.challenges || [])[2]?.issue || "" },
    { agent: "QA",  color: "4A148C", text: "What happens to time entries if the issue assignee is deleted? No defined behaviour." },
    { agent: "ENG", color: "1B5E20", text: (eng.challenges || [])[3]?.issue || "" },
  ];

  comments.forEach((c, i) => {
    const y = 1.35 + i * 0.78;
    s.addShape("roundRect", { x: 0.5, y, w: 9, h: 0.65, fill: { color: C.light }, rectRadius: 0.08, shadow: makeShadow() });
    s.addShape("roundRect", { x: 0.5, y, w: 0.62, h: 0.65, fill: { color: c.color }, rectRadius: 0.08 });
    s.addText(c.agent, { x: 0.5, y, w: 0.62, h: 0.65, fontSize: 9, bold: true, color: C.white, align: "center", valign: "middle", margin: 0 });
    s.addText(c.text, { x: 1.25, y: y + 0.1, w: 8.1, h: 0.48, fontSize: 11, color: C.navy, valign: "middle" });
  });
}

// ── SLIDE 8: Assumption Map ──
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTag(s, "STEP 3", "4A148C", 0.5, 0.3);
  s.addText("Assumption Map", { x: 0.5, y: 0.65, w: 9, h: 0.5, fontSize: 24, bold: true, color: C.navy, fontFace: "Calibri" });
  s.addText(`Top priority: ${assumptions.top_priority || ""}`, { x: 0.5, y: 1.25, w: 9, h: 0.4, fontSize: 11, color: C.navy, italic: true });

  const headers = ["Assumption", "Criticality", "Evidence", "Validate how"];
  const colW = [3.8, 1.3, 1.3, 2.5];
  let x = 0.5;
  headers.forEach((h, i) => {
    s.addShape("roundRect", { x, y: 1.75, w: colW[i], h: 0.32, fill: { color: C.navy }, rectRadius: 0.04 });
    s.addText(h, { x, y: 1.75, w: colW[i], h: 0.32, fontSize: 10, bold: true, color: C.white, align: "center", valign: "middle", margin: 0 });
    x += colW[i] + 0.04;
  });

  const rows = (assumptions.assumptions || []).slice(0, 4).map(a => [
    a.assumption, a.criticality, a.evidence, a.validation_method
  ]);

  rows.forEach((row, ri) => {
    let x = 0.5;
    const y = 2.17 + ri * 0.77;
    row.forEach((cell, ci) => {
      const critColor = cell === "High" ? "FEE2E2" : cell === "Medium" ? "FEF9C3" : cell === "Low" ? "DCFCE7" : C.light;
      const textColor = cell === "High" ? "991B1B" : cell === "Medium" ? "92400E" : cell === "Low" ? "166534" : C.navy;
      s.addShape("roundRect", { x, y, w: colW[ci], h: 0.65, fill: { color: critColor }, rectRadius: 0.04 });
      s.addText(cell, { x, y, w: colW[ci], h: 0.65, fontSize: 10, color: textColor, align: ci === 0 ? "left" : "center", valign: "middle", margin: ci === 0 ? [0, 0, 0, 8] : 0 });
      x += colW[ci] + 0.04;
    });
  });
}

// ── SLIDE 9: Risk Log ──
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTag(s, "STEP 3", "B45309", 0.5, 0.3);
  s.addText("Risk Log", { x: 0.5, y: 0.65, w: 9, h: 0.5, fontSize: 24, bold: true, color: C.navy, fontFace: "Calibri" });
  s.addText(`Top priority: ${risks.top_priority || ""}`, { x: 0.5, y: 1.25, w: 9, h: 0.4, fontSize: 11, color: C.navy, italic: true });

  const topRisks = (risks.risks || []).slice(0, 4);
  topRisks.forEach((r, i) => {
    const y = 1.75 + i * 0.9;
    s.addShape("roundRect", { x: 0.5, y, w: 9, h: 0.75, fill: { color: C.light }, rectRadius: 0.08, shadow: makeShadow() });
    const lColor = r.likelihood === "High" ? "DC2626" : r.likelihood === "Medium" ? "D97706" : "16A34A";
    s.addText(r.likelihood, { x: 0.6, y: y + 0.08, w: 1.0, h: 0.25, fontSize: 10, bold: true, color: lColor, align: "center" });
    s.addText("likelihood", { x: 0.6, y: y + 0.38, w: 1.0, h: 0.2, fontSize: 8, color: C.muted, align: "center" });
    s.addText(r.risk, { x: 1.75, y: y + 0.06, w: 7.6, h: 0.28, fontSize: 11, bold: true, color: C.navy });
    s.addText(`Mitigation: ${r.mitigation}`, { x: 1.75, y: y + 0.4, w: 7.6, h: 0.25, fontSize: 10, color: C.muted, italic: true });
  });
}

// ── SLIDE 10: CTA ──
{
  const s = pres.addSlide();
  s.background = { color: C.navy };
  s.addShape("ellipse", { x: -1, y: 3, w: 5, h: 5, fill: { color: C.mid, transparency: 75 } });
  s.addShape("ellipse", { x: 7, y: -1, w: 4, h: 4, fill: { color: C.dark, transparency: 60 } });
  s.addText("Try it yourself.", { x: 0.6, y: 1.0, w: 9, h: 0.9, fontSize: 40, bold: true, color: C.white, fontFace: "Calibri" });
  s.addText("Three Amigos Spec Writer is open source.\nEnter a feature, get a stress-tested spec in seconds.", { x: 0.6, y: 2.05, w: 8, h: 0.85, fontSize: 15, color: C.ice });
  const links = [
    { label: "GitHub", value: "github.com/Michaela2024/three-amigos" },
    { label: "Built with", value: "Python · Streamlit · Claude Sonnet · Anthropic API" },
    { label: "Try the example", value: "Linear + time tracking — see the contradiction the agents catch" },
  ];
  links.forEach((l, i) => {
    const y = 3.1 + i * 0.72;
    s.addText(l.label, { x: 0.6, y, w: 1.8, h: 0.3, fontSize: 11, bold: true, color: C.ice });
    s.addText(l.value, { x: 2.5, y, w: 7, h: 0.3, fontSize: 11, color: C.white });
  });
  s.addText("Built by [Your name] · Product leader & builder", { x: 0.6, y: 5.1, w: 9, h: 0.3, fontSize: 10, color: C.muted, italic: true });
}

pres.writeFile({ fileName: "three_amigos_demo.pptx" }).then(() => {
  console.log("Done — three_amigos_demo.pptx");
});
