import json
import time
from pathlib import Path

from app.chat.service.chat_orchestrator import ChatOrchestrator
from app.evaluation.metrics.faithfulness_metrics import FaithfulnessEvaluator

def investigate_5_cases():
    orchestrator = ChatOrchestrator()
    faithfulness_eval = FaithfulnessEvaluator(gemini_service=orchestrator.gemini_service)

    target_queries = [
        "What was Lee Kuan Yew's perspective on democracy versus social stability in developing nations?",
        "Synthesize Lee Kuan Yew's stance on press freedom versus national cohesion in a multiracial society.",
        "How did greening Singapore (Garden City campaign) contribute to both tourism and investor confidence?",
        "blilingual educashun in singapor why started???",
        "meritocracy"
    ]

    for i, t_query in enumerate(target_queries, 1):
        print(f"\n==================================================")
        print(f"CASE [{i}/5]: '{t_query}'")
        print(f"==================================================")
        retrieved_chunks = orchestrator.retriever.retrieve(t_query, top_k=5)
        context_block, _ = orchestrator.context_builder.build_context(retrieved_chunks)
        time.sleep(4.2)
        answer, citations, _, is_refusal, is_post2015 = orchestrator.process_chat(t_query, session_id=f"case-debug-{i}")

        print(f"\n[RETRIEVED CONTEXT SUMMARY]:")
        for idx, chunk in enumerate(retrieved_chunks, 1):
            print(f"  Chunk {idx} [{chunk.metadata.get('document_title')} p.{chunk.metadata.get('page_number')}]: {chunk.clean_text[:120]}...")

        print(f"\n[GENERATED ANSWER]:\n{answer}")
        
        time.sleep(4.2)
        faith_res = faithfulness_eval.evaluate_faithfulness(t_query, context_block, answer)
        print(f"\n[FAITHFULNESS EVALUATION]:")
        print(f"  Score: {faith_res['score']} / 5.0")
        print(f"  Reason: {faith_res.get('reason')}")
        print(f"  Unsupported Claim: {faith_res.get('unsupported_claim')}")

if __name__ == "__main__":
    investigate_5_cases()
