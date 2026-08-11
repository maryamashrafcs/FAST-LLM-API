import json
import os
import sys

# Force live LLM mode for evaluation
os.environ["LLM_STUB"] = "0"
os.environ["LLM_ENABLED"] = "true"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm.schemas import LLMRequest
from src.llm.client import generate_llm_response

def run_evaluations():
    eval_file = os.path.join(os.path.dirname(__file__), "cases.json")
    with open(eval_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    total = len(cases)
    passed = 0

    print("\n--- Running LLM Evaluation Suite ---")
    for case in cases:
        req = LLMRequest(prompt=case["input"])
        try:
            res = generate_llm_response(req)
            
            got_cat = str(res.content.category.value).strip().lower()
            exp_cat = str(case["expected_category"]).strip().lower()
            
            got_prio = str(res.content.priority.value).strip().lower()
            exp_prio = str(case["expected_priority"]).strip().lower()

            cat_ok = got_cat == exp_cat
            prio_ok = got_prio == exp_prio
            
            if cat_ok and prio_ok:
                passed += 1
                status = "PASSED"
            else:
                status = f"FAILED (Got: {res.content.category.value}/{res.content.priority.value} | Expected: {case['expected_category']}/{case['expected_priority']})"
        except Exception as e:
            status = f"ERROR ({str(e)})"

        print(f"Case {case['id']} [{case['label']}]: {status}")

    score = (passed / total) * 100
    print(f"\nFinal Score: {passed}/{total} ({score:.1f}%)\n")

if __name__ == "__main__":
    run_evaluations()