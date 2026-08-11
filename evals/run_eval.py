import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm.schemas import LLMRequest
from src.llm.client import generate_llm_response

def run_evaluations():
    eval_file = os.path.join(os.path.dirname(__file__), "cases.json")
    with open(eval_file, "r") as f:
        cases = json.load(f)

    total = len(cases)
    passed = 0

    print("\n--- Running LLM Evaluation Suite ---")
    for case in cases:
        req = LLMRequest(prompt=case["input"])
        try:
            res = generate_llm_response(req)
            cat_ok = res.content.category.value == case["expected_category"]
            prio_ok = res.content.priority.value == case["expected_priority"]
            
            if cat_ok and prio_ok:
                passed += 1
                status = "PASSED"
            else:
                status = f"FAILED (Got: {res.content.category.value}/{res.content.priority.value})"
        except Exception as e:
            status = f"ERROR ({str(e)})"

        print(f"Case {case['id']} [{case['label']}]: {status}")

    score = (passed / total) * 100
    print(f"\nFinal Score: {passed}/{total} ({score:.1f}%)\n")

if __name__ == "__main__":
    run_evaluations()