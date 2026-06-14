import json
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from main import (run_pm_agent, run_engineer_agent, run_qa_agent,
                  run_synthesis_agent, run_assumption_map,
                  run_risk_log, parse_agent_output)

# Create output folder
os.makedirs("demo_data", exist_ok=True)

feature = "Add a manual time logging field to individual issues so engineers can record hours spent"
context = """Product context:
Linear users need automatic time tracking that integrates with existing issues/cycles without manual logging. 
Any solution must maintain Linear's speed-first, minimal-UI philosophy and avoid adding complexity 
to the core issue workflow that engineers use constantly."""

feature_with_context = f"{feature}\n\n{context}"

print("Running PM agent...")
pm_raw = run_pm_agent(feature_with_context)
pm_result = parse_agent_output(pm_raw)
with open("demo_data/pm.json", "w") as f:
    json.dump(pm_result, f, indent=2)
print("PM done.")

print("Running Engineer agent...")
eng_raw = run_engineer_agent(feature_with_context, pm_raw)
eng_result = parse_agent_output(eng_raw)
with open("demo_data/eng.json", "w") as f:
    json.dump(eng_result, f, indent=2)
print("Engineer done.")

print("Running QA agent...")
qa_raw = run_qa_agent(feature_with_context, pm_raw, eng_raw)
qa_result = parse_agent_output(qa_raw)
with open("demo_data/qa.json", "w") as f:
    json.dump(qa_result, f, indent=2)
print("QA done.")

print("Running Synthesis agent...")
final_raw = run_synthesis_agent(feature_with_context, pm_raw, eng_raw, qa_raw)
final_result = parse_agent_output(final_raw)
with open("demo_data/synthesis.json", "w") as f:
    json.dump(final_result, f, indent=2)
print("Synthesis done.")

print("Running Assumption Map agent...")
assumption_raw = run_assumption_map(final_raw)
assumption_result = parse_agent_output(assumption_raw)
with open("demo_data/assumptions.json", "w") as f:
    json.dump(assumption_result, f, indent=2)
print("Assumption map done.")

print("Running Risk Log agent...")
risk_raw = run_risk_log(final_raw)
risk_result = parse_agent_output(risk_raw)
with open("demo_data/risks.json", "w") as f:
    json.dump(risk_result, f, indent=2)
print("Risk log done.")

print("\nAll demo data saved to demo_data/")
