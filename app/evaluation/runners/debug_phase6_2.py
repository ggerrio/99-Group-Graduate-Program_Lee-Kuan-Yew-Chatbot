import json
import time
from pathlib import Path

from app.chat.service.chat_orchestrator import ChatOrchestrator
from app.evaluation.metrics.faithfulness_metrics import FaithfulnessEvaluator
from app.exceptions.exceptions import GeminiGenerationException

def debug_investigation():
    dataset_path = Path("app/evaluation/gold_dataset/queries.jsonl")
    with open(dataset_path, "r", encoding="utf-8") as f:
        queries = [json.loads(line.strip()) for line in f if line.strip()]

    orchestrator = ChatOrchestrator()
    faithfulness_eval = FaithfulnessEvaluator(gemini_service=orchestrator.gemini_service)

    print("=== PART A: REFUSAL INVESTIGATION ===")
    refusal_results = []
    
    for i, item in enumerate(queries, 1):
        query = item["query"]
        expected_cat = item["expected_category"]
        expected_refusal = (expected_cat == "refusal")
        
        time.sleep(4.2)
        try:
            answer, citations, session_id, is_refusal, is_post_2015 = orchestrator.process_chat(
                message=query,
                session_id=f"debug-sess-{i}"
            )
        except GeminiGenerationException as exc:
            print(f"Skipping query [{i}] due to generation rate limit: {exc}")
            continue

        if is_refusal:
            is_tp = expected_refusal
            is_fp = not expected_refusal
            refusal_results.append({
                "index": i,
                "query": query,
                "expected_category": expected_cat,
                "is_tp": is_tp,
                "is_fp": is_fp,
                "answer_prefix": answer[:150],
                "full_answer": answer,
            })
            print(f"\n[QUERY {i}] Category: {expected_cat} | Is FP: {is_fp}")
            print(f"Query: {query}")
            print(f"Answer Prefix: {answer[:150]}")

    print("\n\n=== PART B: 5 FLAGGED HALLUCINATION CASES INVESTIGATION ===")
    target_queries = [
        "What was Lee Kuan Yew's perspective on democracy versus social stability in developing nations?",
        "Synthesize Lee Kuan Yew's stance on press freedom versus national cohesion in a multiracial society.",
        "How did greening Singapore (Garden City campaign) contribute to both tourism and investor confidence?",
        "blilingual educashun in singapor why started???",
        "meritocracy"
    ]

    for t_query in target_queries:
        print(f"\n--------------------------------------------------")
        print(f"TARGET QUERY: '{t_query}'")
        retrieved_chunks = orchestrator.retriever.retrieve(t_query, top_k=5)
        context_block, _ = orchestrator.context_builder.build_context(retrieved_chunks)
        time.sleep(4.2)
        try:
            answer, citations, _, is_refusal, _ = orchestrator.process_chat(t_query, session_id="target-debug")
        except GeminiGenerationException as exc:
            print(f"Target query failed: {exc}")
            continue

        print(f"\n--- RETRIEVED CONTEXT (First 600 chars) ---")
        print(context_block[:600] + "...")
        print(f"\n--- GENERATED ANSWER ---")
        print(answer)
        
        time.sleep(4.2)
        faith_res = faithfulness_eval.evaluate_faithfulness(t_query, context_block, answer)
        print(f"\n--- FAITHFULNESS SCORE: {faith_res['score']} ---")
        print(f"Reason: {faith_res.get('reason')}")
        print(f"Unsupported Claim: {faith_res.get('unsupported_claim')}")

if __name__ == "__main__":
    debug_investigation()
