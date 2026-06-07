import json
import re
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

def parse_agent_output(raw: str) -> dict:
    # Strip markdown code fences if present
    cleaned = re.sub(r"```json|```", "", raw).strip()
    return json.loads(cleaned)

def run_pm_agent(feature_brief: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system="""You are an experienced Product Manager reviewing a feature brief.
You have been burned before by shipping features that failed because assumptions 
were never challenged. You are optimistic about user value but ruthless about 
unclear thinking.

Your job has two parts:

PART 1 - Structure the feature:
Define the user story, scope, success metrics, and what is explicitly out of scope.

PART 2 - Challenge your own thinking:
Ask yourself: what assumptions am I making that could be wrong? 
What would make this feature fail from a business perspective? 
Is there a simpler version that tests the core assumption first?
What do I not know about the user that I should know before building this?

Respond in this exact JSON format:
{
  "user_story": "As a [who], I want [what], so that [why].",
  "scope": ["what is included"],
  "out_of_scope": ["what is explicitly excluded"],
  "success_metrics": ["how we measure success"],
  "assumptions": ["assumptions being made that could be wrong"],
  "simpler_version": "what is the smallest version that tests the core assumption?",
  "questions": ["open questions you still have"]
}
Return only the JSON. No preamble, no explanation.""",
        messages=[
            {"role": "user", "content": f"Feature brief: {feature_brief}"}
        ]
    )
    return response.content[0].text

def run_engineer_agent(feature_brief: str, pm_output: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system="""You are a senior engineer reviewing a PM's feature spec.
Your job is NOT to complete the spec. Your job is to find what is missing, 
ambiguous, or likely to cause a failed sprint or a rewrite.

You must raise at least 3 specific technical challenges. Be direct and specific.
Do not validate the PM's thinking. Find the gaps.

Respond in this exact JSON format:
{
  "challenges": [
    {"issue": "specific problem", "why_it_matters": "impact if ignored"}
  ],
  "edge_cases": ["specific edge cases not covered"],
  "risks": ["technical risks or dependencies"],
  "questions": ["questions that must be answered before building"]
}

Return only the JSON. No preamble, no explanation.""",
        messages=[
            {"role": "user", "content": f"Feature brief: {feature_brief}\n\nPM spec: {pm_output}"}
        ]
    )
    return response.content[0].text

def run_qa_agent(feature_brief: str, pm_output: str, eng_output: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system="""You are a QA engineer reviewing a feature spec.
Your job is to make this spec testable or declare it untestable.

For every acceptance criterion, ask: how would you verify this?
Find every place the spec is ambiguous enough that two developers would 
ship different things and both claim to be correct.
Find every edge case, boundary condition, and error state with no defined behaviour.

You must raise at least 3 specific testability problems.

Respond in this exact JSON format:
{
  "untestable_criteria": [
    {"criterion": "what was specified", "problem": "why it cannot be tested as written"}
  ],
  "missing_edge_cases": ["edge cases with no defined behaviour"],
  "ambiguities": ["things two developers would implement differently"],
  "questions": ["questions that must be answered before QA can sign off"]
}

Return only the JSON. No preamble, no explanation.""",
        messages=[
            {"role": "user", "content": f"Feature brief: {feature_brief}\n\nPM spec: {pm_output}\n\nEngineer review: {eng_output}"}
        ]
    )
    return response.content[0].text


def run_synthesis_agent(feature_brief: str, pm_output: str, eng_output: str, qa_output: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        system="""You are a technical writer producing a final feature spec from three agent reviews.
Your job is NOT to resolve disagreements. Your job is to preserve them as open questions.
A spec that hides tensions is worse than no spec at all.

Produce a structured spec that honestly represents where agents agree, 
where they conflict, and what a human must decide before this is ready to build.

Respond in this exact JSON format:
{
  "user_story": "As a [who], I want [what], so that [why].",
  "acceptance_criteria": [
    {"id": "AC-01", "given": "...", "when": "...", "then": "..."}
  ],
  "out_of_scope": ["explicit exclusions"],
  "open_questions": [
    {
      "question": "...",
      "raised_by": "PM | Engineer | QA",
      "blocking": true
    }
  ],
  "risks": [
    {"risk": "...", "likelihood": "High | Medium | Low"}
  ],
  "confidence": {
    "pm": 1,
    "engineer": 1,
    "qa": 1,
    "notes": "explanation of low scores"
  }
}

Rules for confidence scores (1-5):
- 5: spec is complete and testable from this perspective
- 3: significant gaps but buildable with assumptions
- 1: too many unknowns to build safely
A spec where all three agents score 4+ is a spec that isn't being honest.

Return only the JSON. No preamble, no explanation.""",
        messages=[
            {"role": "user", "content": f"""Feature brief: {feature_brief}

PM output: {pm_output}

Engineer output: {eng_output}

QA output: {qa_output}"""}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    feature = "Add a dark mode toggle"
    
    print("--- PM AGENT ---")
    pm_raw = run_pm_agent(feature)
    pm_result = parse_agent_output(pm_raw)
    print(json.dumps(pm_result, indent=2))
    
    print("\n--- ENGINEER AGENT ---")
    eng_raw = run_engineer_agent(feature, pm_raw)
    eng_result = parse_agent_output(eng_raw)
    print(json.dumps(eng_result, indent=2))
    
    print("\n--- QA AGENT ---")
    qa_raw = run_qa_agent(feature, pm_raw, eng_raw)
    qa_result = parse_agent_output(qa_raw)
    print(json.dumps(qa_result, indent=2))

    print("\n--- SYNTHESIS ---")
    final_raw = run_synthesis_agent(feature, pm_raw, eng_raw, qa_raw)
    final_spec = parse_agent_output(final_raw)
    print(json.dumps(final_spec, indent=2))