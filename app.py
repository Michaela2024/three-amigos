import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
import json
from pathlib import Path
import docx

sys.path.append(str(Path(__file__).parent))
from main import run_pm_agent, run_engineer_agent, run_qa_agent, run_synthesis_agent, parse_agent_output

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

# ── Mode selector ──
mode = st.radio(
    "What would you like to do?",
    ["Feature Brief — discuss a new feature",
     "Spec Review — review an existing spec"],
    horizontal=True
)

st.divider()

# ── Helper: read uploaded file ──
def read_uploaded_file(uploaded_file) -> str:
    if uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    else:
        return uploaded_file.read().decode("utf-8")

# ── Helper: build markdown from synthesis ──
def build_markdown(feature: str, spec: dict) -> str:
    md = f"# Feature Spec: {feature}\n\n"
    md += f"## User Story\n{spec.get('user_story', '')}\n\n"
    md += "## Acceptance Criteria\n"
    for ac in spec.get('acceptance_criteria', []):
        md += f"**{ac['id']}** Given {ac['given']}, when {ac['when']}, then {ac['then']}\n\n"
    md += "## Out of Scope\n"
    for item in spec.get('out_of_scope', []):
        md += f"- {item}\n"
    md += "\n## Open Questions\n"
    for q in spec.get('open_questions', []):
        blocking = "🔴 BLOCKING" if q.get('blocking') else "🟡"
        md += f"- {blocking} {q['question']} *(raised by: {q['raised_by']})*\n"
    md += "\n## Risks\n"
    for r in spec.get('risks', []):
        md += f"- **{r['likelihood']}** — {r['risk']}\n"
    md += "\n## Confidence Scores\n"
    conf = spec.get('confidence', {})
    md += f"- PM: {conf.get('pm')}/5\n"
    md += f"- Engineer: {conf.get('engineer')}/5\n"
    md += f"- QA: {conf.get('qa')}/5\n"
    md += f"\n_{conf.get('notes', '')}_\n"
    return md

# ══════════════════════════════════════════
# MODE 1: FEATURE BRIEF
# ══════════════════════════════════════════
if "Feature Brief" in mode:

    st.subheader("Step 1 — Describe your feature")
    st.info("💡 Type anything — a vague idea, an epic, a feature brief, or a user story. "
            "The PM agent will assess it and tell you what it is and what to think about next.")

    feature = st.text_area(
        "What do you want to build?",
        placeholder="e.g. Add email notifications for order status updates",
        height=120
    )

    assess_button = st.button("Assess", type="primary", disabled=not feature)

    # ── Step 1: PM Assessment ──
    if assess_button:
        st.session_state.pm_raw = None
        st.session_state.pm_result = None
        st.session_state.feature = feature

        with st.status("PM agent assessing...", expanded=True) as status:
            pm_raw = run_pm_agent(feature)
            pm_result = parse_agent_output(pm_raw)
            st.session_state.pm_raw = pm_raw
            st.session_state.pm_result = pm_result
            status.update(label="PM assessment complete ✓", state="complete")

    # ── Show PM output if available ──
    if st.session_state.get("pm_result"):
        pm_result = st.session_state.pm_result
        feature = st.session_state.feature

        st.divider()
        st.subheader("PM Assessment")

        input_type = pm_result.get("input_type", "feature")
        st.markdown(f"**Input type detected:** `{input_type}`")

        # Epic breakdown
        epic = pm_result.get("epic_breakdown")
        if epic and input_type == "epic":
            st.warning("This looks like an epic — too broad to spec directly. "
                      "Here's how to break it down.", icon="⚠️")
            st.markdown(f"**{epic.get('explanation', '')}**")
            st.markdown("**Candidate features:**")
            for f in epic.get("candidate_features", []):
                st.markdown(f"- {f}")
            st.markdown(f"**Recommended first:** {epic.get('recommended_first', '')}")

        else:
            # User story
            if pm_result.get("user_story"):
                st.markdown(f"**User story:** {pm_result['user_story']}")

            # Assumptions
            if pm_result.get("assumptions"):
                with st.expander("Assumptions to test", expanded=True):
                    for a in pm_result["assumptions"]:
                        st.markdown(f"- {a}")

            # Simpler version
            if pm_result.get("simpler_version"):
                st.info(f"💡 **Simpler version to test first:** {pm_result['simpler_version']}")

            # Questions
            if pm_result.get("questions"):
                with st.expander("Open questions", expanded=False):
                    for q in pm_result["questions"]:
                        st.markdown(f"- {q}")

        st.divider()

        # ── Step 2: Full pipeline ──
        if input_type != "epic":
            st.subheader("Step 2 — Run full review")
            st.markdown("The Engineer and QA agents will stress-test the PM assessment above.")

            run_button = st.button("Run full review", type="primary")

            if run_button:
                pm_raw = st.session_state.pm_raw
                eng_raw = qa_raw = None

                with st.status("Engineer agent thinking...", expanded=True) as status:
                    eng_raw = run_engineer_agent(feature, pm_raw)
                    eng_result = parse_agent_output(eng_raw)
                    status.update(label="Engineer ✓", state="complete")
                with st.expander("Engineer output", expanded=False):
                    st.json(eng_result)

                with st.status("QA agent thinking...", expanded=True) as status:
                    qa_raw = run_qa_agent(feature, pm_raw, eng_raw)
                    qa_result = parse_agent_output(qa_raw)
                    status.update(label="QA ✓", state="complete")
                with st.expander("QA output", expanded=False):
                    st.json(qa_result)

                with st.status("Synthesis agent thinking...", expanded=True) as status:
                    final_raw = run_synthesis_agent(feature, pm_raw, eng_raw, qa_raw)
                    final_spec = parse_agent_output(final_raw)
                    status.update(label="Synthesis ✓", state="complete")

                st.divider()
                st.subheader("Final Spec")
                st.json(final_spec)

                md = build_markdown(feature, final_spec)
                st.download_button(
                    label="Download spec as markdown",
                    data=md,
                    file_name="spec.md",
                    mime="text/markdown"
                )

# ══════════════════════════════════════════
# MODE 2: SPEC REVIEW
# ══════════════════════════════════════════
else:
    st.subheader("Upload your spec")
    st.markdown("Upload an existing spec and choose which agents to review it. "
                "You'll get your spec back with inline comments.")

    uploaded_file = st.file_uploader(
        "Upload a spec file",
        type=["txt", "md", "docx"]
    )

    if uploaded_file:
        spec_text = read_uploaded_file(uploaded_file)
        st.success(f"Loaded: {uploaded_file.name}")
        with st.expander("Preview", expanded=False):
            st.text(spec_text[:2000] + ("..." if len(spec_text) > 2000 else ""))

        st.subheader("Choose your reviewers")
        col1, col2 = st.columns(2)
        with col1:
            run_eng = st.checkbox("Engineer", value=True)
            st.caption("Finds what's missing or ambiguous. Raises technical risks and decisions needed before building.")
        with col2:
            run_qa = st.checkbox("QA", value=True)
            st.caption("Makes the spec testable or declares it untestable. Finds ambiguity two developers would resolve differently.")

        review_button = st.button("Review", type="primary")

        if review_button:
            annotated = f"# Spec Review: {uploaded_file.name}\n\n"
            annotated += spec_text + "\n\n---\n\n"

            if run_eng:
                with st.status("Engineer reviewing...", expanded=True) as status:
                    eng_raw = run_engineer_agent(spec_text, spec_text)
                    eng_result = parse_agent_output(eng_raw)
                    status.update(label="Engineer ✓", state="complete")
                with st.expander("Engineer comments", expanded=True):
                    st.json(eng_result)
                annotated += "## Engineer Review\n\n"
                for c in eng_result.get("challenges", []):
                    annotated += f"**[ENGINEER]** {c['issue']} — _{c['why_it_matters']}_\n\n"

            if run_qa:
                with st.status("QA reviewing...", expanded=True) as status:
                    qa_raw = run_qa_agent(spec_text, spec_text, "")
                    qa_result = parse_agent_output(qa_raw)
                    status.update(label="QA ✓", state="complete")
                with st.expander("QA comments", expanded=True):
                    st.json(qa_result)
                annotated += "## QA Review\n\n"
                for u in qa_result.get("untestable_criteria", []):
                    annotated += f"**[QA]** {u['criterion']} — _{u['problem']}_\n\n"
                for a in qa_result.get("ambiguities", []):
                    annotated += f"**[QA - AMBIGUITY]** {a}\n\n"

            st.divider()
            st.download_button(
                label="Download annotated spec as markdown",
                data=annotated,
                file_name="annotated_spec.md",
                mime="text/markdown"
            )