import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
import json
import docx
import importlib.util
import os

spec_loader = importlib.util.spec_from_file_location(
    "main",
    os.path.join(os.path.dirname(__file__), "main.py")
)
main_module = importlib.util.module_from_spec(spec_loader)
spec_loader.loader.exec_module(main_module)

run_pm_agent = main_module.run_pm_agent
run_engineer_agent = main_module.run_engineer_agent
run_qa_agent = main_module.run_qa_agent
run_synthesis_agent = main_module.run_synthesis_agent
run_assumption_map = main_module.run_assumption_map
run_risk_log = main_module.run_risk_log
parse_agent_output = main_module.parse_agent_output

# ── Cached agent calls ──
@st.cache_data(show_spinner=False)
def cached_pm_agent(feature: str) -> str:
    return run_pm_agent(feature)

@st.cache_data(show_spinner=False)
def cached_engineer_agent(feature: str, pm_raw: str) -> str:
    return run_engineer_agent(feature, pm_raw)

@st.cache_data(show_spinner=False)
def cached_qa_agent(feature: str, pm_raw: str, eng_raw: str) -> str:
    return run_qa_agent(feature, pm_raw, eng_raw)

@st.cache_data(show_spinner=False)
def cached_synthesis_agent(feature: str, pm_raw: str, eng_raw: str, qa_raw: str) -> str:
    return run_synthesis_agent(feature, pm_raw, eng_raw, qa_raw)

@st.cache_data(show_spinner=False)
def cached_assumption_map(spec: str) -> str:
    return run_assumption_map(spec)

@st.cache_data(show_spinner=False)
def cached_risk_log(spec: str) -> str:
    return run_risk_log(spec)

st.set_page_config(
    page_title="Three Amigos Spec Writer",
    page_icon="🤝",
    layout="wide"
)

# ── Header ──
st.title("🤝 Three Amigos Spec Writer")
st.caption("Stress-test your features before you build them.")
st.markdown("""
**Three Amigos** is a practice from agile development where a PM, Engineer, and QA 
stress-test a feature together before it's built. This tool runs that conversation 
for you in seconds — surfacing conflicts, edge cases, and open questions before 
a line of code is written.
""")

st.divider()

# ── Tabs ──
tab1, tab2, tab3 = st.tabs(["Generate Spec", "Review Spec", "PM Artefacts"])

# ── Helper: read uploaded file ──
def read_uploaded_file(uploaded_file) -> str:
    if uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    else:
        return uploaded_file.read().decode("utf-8")

# ── Helper: build assumption map markdown ──
def build_assumption_markdown(result: dict) -> str:
    md = "# Assumption Map\n\n"
    md += f"**Top priority:** {result.get('top_priority', '')}\n\n"
    md += "| Assumption | Why it matters | Criticality | Evidence | Validation method |\n"
    md += "|------------|---------------|-------------|----------|------------------|\n"
    for a in result.get('assumptions', []):
        md += f"| {a['assumption']} | {a['why_it_matters']} | {a['criticality']} | {a['evidence']} | {a['validation_method']} |\n"
    return md

# ── Helper: build risk log markdown ──
def build_risk_markdown(result: dict) -> str:
    md = "# Risk Log\n\n"
    md += f"**Top priority:** {result.get('top_priority', '')}\n\n"
    md += "| Risk | Likelihood | Impact | Mitigation | Owner |\n"
    md += "|------|-----------|--------|------------|-------|\n"
    for r in result.get('risks', []):
        md += f"| {r['risk']} | {r['likelihood']} | {r['impact']} | {r['mitigation']} | {r.get('owner', '')} |\n"
    return md

# ══════════════════════════════════════════
# TAB 1: GENERATE SPEC
# ══════════════════════════════════════════
with tab1:
    st.subheader("Generate a feature spec")
    st.markdown("Enter a feature idea, epic, or user story. The PM agent will assess it "
                "and generate a spec you can download and refine.")

    feature = st.text_area(
        "What do you want to build?",
        placeholder="e.g. Add email notifications for order status updates",
        height=120,
        key="feature_input"
    )

    context = st.text_area(
        "Product context (optional)",
        placeholder="e.g. B2B SaaS project management tool, React frontend, Python backend, "
                    "primary users are project managers and developers.",
        height=80,
        key="context_input"
    )

    assess_button = st.button("Generate Spec", type="primary",
                              disabled=not feature, key="assess_btn")

    if assess_button:
        st.session_state.pm_raw = None
        st.session_state.pm_result = None
        feature_with_context = f"{feature}\n\nProduct context:\n{context}" if context else feature
        st.session_state.feature = feature_with_context

        with st.status("PM agent thinking...", expanded=True) as status:
            pm_raw = cached_pm_agent(feature_with_context)
            pm_result = parse_agent_output(pm_raw)
            st.session_state.pm_raw = pm_raw
            st.session_state.pm_result = pm_result
            status.update(label="PM ✓", state="complete")

    if st.session_state.get("pm_result"):
        pm_result = st.session_state.pm_result
        feature = st.session_state.feature

        st.divider()

        input_type = pm_result.get("input_type", "feature")
        st.markdown(f"**Input type detected:** `{input_type}`")

        epic = pm_result.get("epic_breakdown")
        if epic and input_type == "epic":
            st.warning("This looks like an epic — too broad to spec directly.", icon="⚠️")
            st.markdown(f"**{epic.get('explanation', '')}**")
            st.markdown("**Candidate features:**")
            for f in epic.get("candidate_features", []):
                st.markdown(f"- {f}")
            st.markdown(f"**Recommended first:** {epic.get('recommended_first', '')}")
            st.info("👆 Pick one of the candidate features above and enter it as a new brief.")

        else:
            if pm_result.get("user_story"):
                st.markdown(f"**User story:** {pm_result['user_story']}")

            if pm_result.get("assumptions"):
                with st.expander("Assumptions to test", expanded=True):
                    for a in pm_result["assumptions"]:
                        st.markdown(f"- {a}")

            if pm_result.get("simpler_version"):
                st.info(f"💡 **Simpler version:** {pm_result['simpler_version']}")

            if pm_result.get("questions"):
                with st.expander("Open questions", expanded=False):
                    for q in pm_result["questions"]:
                        st.markdown(f"- {q}")

            st.divider()

            md = f"# Feature Spec: {feature}\n\n"
            md += f"## User Story\n{pm_result.get('user_story', '')}\n\n"
            md += "## Scope\n"
            for item in pm_result.get('scope', []):
                md += f"- {item}\n"
            md += "\n## Out of Scope\n"
            for item in pm_result.get('out_of_scope', []):
                md += f"- {item}\n"
            md += "\n## Success Metrics\n"
            for item in pm_result.get('success_metrics', []):
                md += f"- {item}\n"
            md += "\n## Assumptions to Test\n"
            for item in pm_result.get('assumptions', []):
                md += f"- {item}\n"
            md += f"\n## Simpler Version\n{pm_result.get('simpler_version', '')}\n\n"
            md += "## Open Questions\n"
            for item in pm_result.get('questions', []):
                md += f"- {item}\n"

            st.download_button(
                label="⬇️ Download spec as markdown",
                data=md,
                file_name="spec.md",
                mime="text/markdown",
                key="download_spec"
            )

# ══════════════════════════════════════════
# TAB 2: REVIEW SPEC
# ══════════════════════════════════════════
with tab2:
    st.subheader("Review an existing spec")
    st.markdown("Upload a spec — including one generated in Tab 1 — and get it back "
                "with inline comments from Engineer, QA, or both.")

    uploaded_file = st.file_uploader(
        "Upload a spec file (.txt, .md, .docx)",
        type=["txt", "md", "docx"],
        key="spec_upload"
    )

    if uploaded_file:
        spec_text = read_uploaded_file(uploaded_file)
        st.success(f"Loaded: {uploaded_file.name}")
        with st.expander("Preview", expanded=False):
            st.text(spec_text[:2000] + ("..." if len(spec_text) > 2000 else ""))

        st.subheader("Choose your reviewers")
        col1, col2 = st.columns(2)
        with col1:
            run_eng = st.checkbox("Engineer", value=True, key="eng_check")
            st.caption("Finds what's missing or ambiguous. Raises technical risks "
                      "and decisions needed before building.")
        with col2:
            run_qa = st.checkbox("QA", value=True, key="qa_check")
            st.caption("Makes the spec testable or declares it untestable. "
                      "Finds ambiguity two developers would resolve differently.")

        review_button = st.button("Review Spec", type="primary", key="review_btn")

        if review_button:
            annotated = f"# Spec Review: {uploaded_file.name}\n\n"
            annotated += spec_text + "\n\n---\n\n"

            if run_eng:
                with st.status("Engineer reviewing...", expanded=True) as status:
                    eng_raw = cached_engineer_agent(spec_text, spec_text)
                    eng_result = parse_agent_output(eng_raw)
                    status.update(label="Engineer ✓", state="complete")
                with st.expander("Engineer comments", expanded=True):
                    st.json(eng_result)
                annotated += "## Engineer Review\n\n"
                for c in eng_result.get("challenges", []):
                    annotated += f"**[ENGINEER]** {c['issue']}\n\n"
                    annotated += f"_{c['why_it_matters']}_\n\n"

            if run_qa:
                with st.status("QA reviewing...", expanded=True) as status:
                    qa_raw = cached_qa_agent(spec_text, spec_text, "")
                    qa_result = parse_agent_output(qa_raw)
                    status.update(label="QA ✓", state="complete")
                with st.expander("QA comments", expanded=True):
                    st.json(qa_result)
                annotated += "## QA Review\n\n"
                for u in qa_result.get("untestable_criteria", []):
                    annotated += f"**[QA - UNTESTABLE]** {u['criterion']}\n\n"
                    annotated += f"_{u['problem']}_\n\n"
                for a in qa_result.get("ambiguities", []):
                    annotated += f"**[QA - AMBIGUITY]** {a}\n\n"

            st.divider()
            st.download_button(
                label="⬇️ Download annotated spec as markdown",
                data=annotated,
                file_name="annotated_spec.md",
                mime="text/markdown",
                key="download_annotated"
            )

# ══════════════════════════════════════════
# TAB 3: PM ARTEFACTS
# ══════════════════════════════════════════
with tab3:
    st.subheader("Generate PM artefacts")
    st.markdown("Upload a reviewed spec and generate an assumption map, risk log, or both.")

    artefact_file = st.file_uploader(
        "Upload a spec file (.txt, .md, .docx)",
        type=["txt", "md", "docx"],
        key="artefact_upload"
    )

    if artefact_file:
        artefact_text = read_uploaded_file(artefact_file)
        st.success(f"Loaded: {artefact_file.name}")
        with st.expander("Preview", expanded=False):
            st.text(artefact_text[:2000] + ("..." if len(artefact_text) > 2000 else ""))

        st.subheader("Choose your artefacts")
        col1, col2 = st.columns(2)
        with col1:
            gen_assumptions = st.checkbox("Assumption Map", value=True,
                                          key="assumption_check")
            st.caption("What has to be true for this feature to succeed, "
                      "ranked by criticality and evidence.")
        with col2:
            gen_risks = st.checkbox("Risk Log", value=True, key="risk_check")
            st.caption("What could go wrong, likelihood, impact, "
                      "mitigation, and owner.")

        artefact_button = st.button("Generate Artefacts", type="primary",
                                    key="artefact_btn")

        if artefact_button:
            if gen_assumptions:
                with st.status("Generating assumption map...", expanded=True) as status:
                    assumption_raw = cached_assumption_map(artefact_text)
                    assumption_result = parse_agent_output(assumption_raw)
                    status.update(label="Assumption map ✓", state="complete")

                st.subheader("Assumption Map")
                st.markdown(f"**Top priority:** {assumption_result.get('top_priority', '')}")
                st.dataframe(assumption_result.get('assumptions', []))

                assumption_md = build_assumption_markdown(assumption_result)
                st.download_button(
                    label="⬇️ Download assumption map",
                    data=assumption_md,
                    file_name="assumption_map.md",
                    mime="text/markdown",
                    key="download_assumptions"
                )

            if gen_risks:
                with st.status("Generating risk log...", expanded=True) as status:
                    risk_raw = cached_risk_log(artefact_text)
                    risk_result = parse_agent_output(risk_raw)
                    status.update(label="Risk log ✓", state="complete")

                st.subheader("Risk Log")
                st.markdown(f"**Top priority:** {risk_result.get('top_priority', '')}")
                st.dataframe(risk_result.get('risks', []))

                risk_md = build_risk_markdown(risk_result)
                st.download_button(
                    label="⬇️ Download risk log",
                    data=risk_md,
                    file_name="risk_log.md",
                    mime="text/markdown",
                    key="download_risks"
                )