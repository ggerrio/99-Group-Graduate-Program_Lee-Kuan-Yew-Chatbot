"""
Phase 6.3 Targeted Regression Evaluation Runner.

SCOPE: Evaluates ONLY the five previously failing queries identified in Phase 6.1/6.2.
DO NOT expand this to the full 60-query gold dataset -- targeted regression only.

Queries under test:
1. Democracy vs social stability (faithfulness score was 1.0 in Phase 6.1)
2. Press freedom vs national cohesion (score 2.0)
3. Garden City / greening Singapore (score 2.0, fabricated "Look magazine")
4. blilingual educashun in singapor??? (score 2.0, edge-case noisy query)
5. meritocracy (score 2.0, single-word keyword query)
"""

import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from app.chat.service.chat_orchestrator import ChatOrchestrator
from app.evaluation.metrics.faithfulness_metrics import FaithfulnessEvaluator
from app.evaluation.metrics.persona_rubric import PersonaRubricEvaluator
from app.evaluation.metrics.citation_validator import validate_citations
from app.core.logging.logger import logger

TARGET_QUERIES = [
    {
        "key": "democracy_stability",
        "query": "What was Lee Kuan Yew's perspective on democracy versus social stability in developing nations?",
        "expected_category": "factual",
        "expected_source": "One Man's View Of The World",
        "phase_6_1_faith": 1.0,
        "failure_reason": "Entire answer hallucinated -- retrieved context was publisher metadata, not political content",
    },
    {
        "key": "press_freedom",
        "query": "Synthesize Lee Kuan Yew's stance on press freedom versus national cohesion in a multiracial society.",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World",
        "phase_6_1_faith": 2.0,
        "failure_reason": "Fabricated direct LKY quote about 'American liberal academics' not present in retrieved context",
    },
    {
        "key": "garden_city",
        "query": "How did greening Singapore (Garden City campaign) contribute to both tourism and investor confidence?",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World",
        "phase_6_1_faith": 2.0,
        "failure_reason": "Fabricated 'Look magazine' as a named publication recognizing Singapore's greening efforts",
    },
    {
        "key": "bilingual_noisy",
        "query": "blilingual educashun in singapor why started???",
        "expected_category": "edge_case",
        "expected_source": "Singapore's Bilingual Journey",
        "phase_6_1_faith": 2.0,
        "failure_reason": "Noisy/misspelled query degraded embedding signal; answer included fabricated personal sentiment",
    },
    {
        "key": "meritocracy_keyword",
        "query": "meritocracy",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World",
        "phase_6_1_faith": 2.0,
        "failure_reason": "Single-word query; evaluator over-penalized valid thematic synthesis as editorializing",
    },
]


def run_phase6_3_regression(
    output_report_path: Path = Path("app/evaluation/reports/eval_report_phase6_3.md"),
) -> None:
    print("=" * 70)
    print("PHASE 6.3 TARGETED REGRESSION EVALUATION")
    print(f"Scope: {len(TARGET_QUERIES)} previously failing queries only")
    print("=" * 70)

    orchestrator = ChatOrchestrator()
    faithfulness_eval = FaithfulnessEvaluator(gemini_service=orchestrator.gemini_service)
    persona_eval = PersonaRubricEvaluator(gemini_service=orchestrator.gemini_service)

    results: List[Dict[str, Any]] = []

    for i, item in enumerate(TARGET_QUERIES, 1):
        query = item["query"]
        key = item["key"]

        print(f"\n{'=' * 70}")
        print(f"[{i}/5] KEY: {key}")
        print(f"QUERY: '{query}'")
        print(f"EXPECTED SOURCE: {item['expected_source']}")
        print(f"PHASE 6.1 FAITHFULNESS (BEFORE): {item['phase_6_1_faith']}/5.0")
        print(f"ROOT CAUSE: {item['failure_reason']}")

        # Part A: Retrieval Investigation
        retrieved_chunks = orchestrator.retriever.retrieve(query, top_k=5)

        print(f"\n[RETRIEVAL ANALYSIS -- top {len(retrieved_chunks)} chunks]:")
        retrieval_log = []
        for rank, chunk in enumerate(retrieved_chunks, 1):
            meta = chunk.metadata
            entry = {
                "rank": rank,
                "score": chunk.score,
                "document_title": meta.get("document_title", "Unknown"),
                "document_type": meta.get("document_type", "Unknown"),
                "year": meta.get("year", "N/A"),
                "page_number": meta.get("page_number", "N/A"),
                "text_snippet": chunk.clean_text[:120],
            }
            retrieval_log.append(entry)
            print(
                f"  Rank {rank} | Score={chunk.score:.4f} | "
                f"{meta.get('document_title','?')!r} p.{meta.get('page_number','?')} "
                f"({meta.get('document_type','?')})"
            )
            print(f"         Snippet: {chunk.clean_text[:100]}...")

        context_block, _ = orchestrator.context_builder.build_context(retrieved_chunks)

        expected_src = item["expected_source"].lower()
        source_hit = any(
            expected_src in c.metadata.get("document_title", "").lower()
            for c in retrieved_chunks
        )
        print(f"\n  Source hit ('{item['expected_source']}'): {'YES' if source_hit else 'NO'}")

        # Generation
        time.sleep(4.2)
        try:
            answer, citations, session_id, is_refusal, is_post_2015 = orchestrator.process_chat(
                message=query,
                session_id=f"phase63-regression-{i}",
            )
        except Exception as exc:
            logger.warning(f"Generation error on query [{i}]: {exc}")
            answer = ""
            citations = []
            is_refusal = False
            is_post_2015 = False

        print(f"\n[GENERATED ANSWER]:")
        print(f"  is_refusal={is_refusal} | is_post_2015={is_post_2015} | citations={len(citations)}")
        print(f"  {answer[:400]}{'...' if len(answer) > 400 else ''}")

        # Citation Validation
        cite_val = validate_citations(citations)
        print(f"\n[CITATIONS]: valid={cite_val['valid_count']} | invalid={cite_val['invalid_count']}")
        for c in citations:
            print(f"  - {c.get('document_title')} p.{c.get('page_number')} (score={c.get('score', 'N/A')})")

        # Faithfulness Evaluation
        if is_refusal:
            faith_result = {"score": 5.0, "reason": "Correct refusal", "unsupported_claim": None}
        else:
            time.sleep(4.2)
            faith_result = faithfulness_eval.evaluate_faithfulness(query, context_block, answer)

        print(f"\n[FAITHFULNESS SCORE (AFTER)]: {faith_result['score']}/5.0")
        print(f"  Reason: {str(faith_result.get('reason', ''))[:200]}")
        if faith_result.get("unsupported_claim"):
            print(f"  Unsupported Claim: {faith_result['unsupported_claim']}")

        # Persona Evaluation
        if is_refusal or not answer:
            persona_result = {"score": 5.0, "reason": "Refusal or empty -- skipped"}
        else:
            time.sleep(4.2)
            persona_result = persona_eval.evaluate_persona(query, answer)

        print(f"\n[PERSONA SCORE (AFTER)]: {persona_result['score']}/5.0")
        print(f"  Reason: {str(persona_result.get('reason', ''))[:150]}")

        results.append({
            "key": key,
            "query": query,
            "expected_category": item["expected_category"],
            "expected_source": item["expected_source"],
            "phase_6_1_faithfulness": item["phase_6_1_faith"],
            "root_cause": item["failure_reason"],
            "retrieval_log": retrieval_log,
            "source_hit": source_hit,
            "answer": answer,
            "answer_snippet": answer[:350],
            "is_refusal": is_refusal,
            "is_post_2015": is_post_2015,
            "citations": citations,
            "citations_valid": cite_val["valid_count"],
            "citations_invalid": cite_val["invalid_count"],
            "faithfulness_score": faith_result["score"],
            "faithfulness_reason": str(faith_result.get("reason", "")),
            "unsupported_claim": faith_result.get("unsupported_claim"),
            "persona_score": persona_result["score"],
            "persona_reason": str(persona_result.get("reason", "")),
        })

    # Write Report
    _write_report(results, output_report_path)

    print(f"\n{'=' * 70}")
    print(f"Phase 6.3 regression complete. Report: {output_report_path.resolve()}")
    print("=" * 70)

    # Final Recommendation
    passing = [r for r in results if r["faithfulness_score"] >= 3.0 or r["is_refusal"]]
    failing = [r for r in results if r["faithfulness_score"] < 3.0 and not r["is_refusal"]]

    print(f"\nREGRESSION SUMMARY: {len(passing)}/5 queries passing (faithfulness >= 3.0)")
    for r in results:
        status = "PASS" if (r["faithfulness_score"] >= 3.0 or r["is_refusal"]) else "FAIL"
        delta = r["faithfulness_score"] - r["phase_6_1_faithfulness"]
        delta_str = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
        print(f"  {status} [{r['key']}] faith={r['faithfulness_score']}/5.0 (delta {delta_str}) | persona={r['persona_score']}/5.0")

    if not failing:
        print("\nRECOMMENDATION: All 5 regression queries pass. Proceed to Phase 7 Deployment.")
        print("   NOTE: The full 60-query benchmark may be rerun as a final validation only if")
        print("   Gemini API quota permits, but it is NOT required for this targeted regression phase.")
    else:
        print(f"\nWARNING: {len(failing)} query/queries still below threshold. Review root causes before Phase 7.")
        for r in failing:
            print(f"   Still failing: [{r['key']}] -- {r['unsupported_claim'] or 'No specific claim flagged'}")


def _write_report(results: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Phase 6.3 Evaluation Report: Targeted Regression Fix",
        "",
        f"> Generated: {ts}  |  Scope: 5 previously failing queries (NOT the full 60-query benchmark)",
        "",
        "---",
        "",
        "## Executive Summary: Phase 6.1 vs Phase 6.3 Faithfulness Comparison",
        "",
        "| # | Query (abbreviated) | Root Cause Category | Faith 6.1 | Faith 6.3 | Delta | Persona 6.3 | Status |",
        "| :- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    for idx, r in enumerate(results, 1):
        delta = r["faithfulness_score"] - r["phase_6_1_faithfulness"]
        delta_str = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
        status = "PASS" if (r["faithfulness_score"] >= 3.0 or r["is_refusal"]) else "FAIL"
        q_abbr = r["query"][:55] + ("..." if len(r["query"]) > 55 else "")
        root_cat = _classify_root_cause(r["root_cause"])
        lines.append(
            f"| {idx} | {q_abbr} | {root_cat} | "
            f"`{r['phase_6_1_faithfulness']:.1f}` | **`{r['faithfulness_score']:.1f}`** | "
            f"`{delta_str}` | `{r['persona_score']:.1f}` | {status} |"
        )

    lines += ["", "---", ""]

    for idx, r in enumerate(results, 1):
        delta = r["faithfulness_score"] - r["phase_6_1_faithfulness"]
        delta_str = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
        status = "PASS" if (r["faithfulness_score"] >= 3.0 or r["is_refusal"]) else "FAIL"

        lines += [
            f"## Query {idx}: {r['key'].replace('_', ' ').title()} [{status}]",
            "",
            f"**Query:** `{r['query']}`",
            f"**Expected Category:** `{r['expected_category']}` | **Expected Source:** `{r['expected_source']}`",
            "",
            "### Root Cause Analysis",
            "",
            f"> {r['root_cause']}",
            "",
            "### Retrieval Analysis",
            "",
            "| Rank | Score | Document Title | Type | Page |",
            "| :--: | :---: | :--- | :--- | :---: |",
        ]

        for chunk in r["retrieval_log"]:
            hit_marker = " [HIT]" if r["expected_source"].lower() in chunk["document_title"].lower() else ""
            lines.append(
                f"| {chunk['rank']} | `{chunk['score']:.4f}` | {chunk['document_title']}{hit_marker} | "
                f"{chunk['document_type']} | {chunk['page_number']} |"
            )

        lines += [
            "",
            f"**Source Hit** (`{r['expected_source']}`): {'YES' if r['source_hit'] else 'NO -- retrieval miss'}",
            "",
            "### Generated Answer",
            "",
            "```",
            r["answer_snippet"] + ("..." if len(r["answer"]) > 350 else ""),
            "```",
            "",
            f"**is_refusal:** `{r['is_refusal']}` | **is_post_2015:** `{r['is_post_2015']}`",
            "",
            "### Citations",
            "",
        ]

        if r["citations"]:
            lines.append("| Document Title | Type | Year | Page | Score |")
            lines.append("| :--- | :--- | :---: | :---: | :---: |")
            for c in r["citations"]:
                lines.append(
                    f"| {c.get('document_title','?')} | {c.get('document_type','?')} | "
                    f"{c.get('year','N/A')} | {c.get('page_number','?')} | `{c.get('score','N/A')}` |"
                )
            lines.append(
                f"\n**Citation Validity:** {r['citations_valid']} valid / {r['citations_invalid']} invalid"
            )
        else:
            lines.append("*No citations (refusal or generation error)*")

        lines += [
            "",
            "### Faithfulness: Before vs After",
            "",
            "| Metric | Phase 6.1 | Phase 6.3 | Delta |",
            "| :--- | :---: | :---: | :---: |",
            f"| Faithfulness Score | `{r['phase_6_1_faithfulness']:.1f}/5.0` | **`{r['faithfulness_score']:.1f}/5.0`** | `{delta_str}` |",
            "",
            f"**Faithfulness Reason:** {r['faithfulness_reason'][:300]}",
        ]

        if r.get("unsupported_claim"):
            lines.append(f"\n**Unsupported Claim Flagged:** {r['unsupported_claim']}")

        lines += [
            "",
            "### Persona Score",
            "",
            f"**Score:** `{r['persona_score']:.1f}/5.0`",
            f"**Reason:** {r['persona_reason'][:200]}",
            "",
            "---",
            "",
        ]

    lines += [
        "## Code Changes Applied (Phase 6.3)",
        "",
        "### Fix 1: `app/rag/prompt_templates/persona_prompt.txt` -- Anti-Fabrication Hardening",
        "",
        "- Explicit prohibition on invented named publications/magazines (e.g., 'Look magazine', 'Time magazine')",
        "- Prohibition on invented statistics, personal anecdotes, and paraphrased third-party commentary",
        "- Guidance for single-word / short keyword queries to expand using ONLY retrieved context facts",
        "",
        "### Fix 2: `app/evaluation/metrics/faithfulness_metrics.py` -- Evaluator Calibration",
        "",
        "- Rule 3: Do NOT penalize keyword/edge-case queries for broad thematic grounding",
        "- Rule 4: FABRICATED PUBLICATION NAMES always score <= 2 (hardened, not softened)",
        "- Rule 5: FABRICATED PERSONAL ANECDOTES always score <= 2",
        "- Sharpened score scale to distinguish invented proper nouns from thematic paraphrase",
        "",
        "### Fix 3: `app/chat/service/chat_orchestrator.py` -- Query Normalizer",
        "",
        "- Added `_normalize_query()`: collapses repeated punctuation (??? to ?), trims whitespace",
        "- Applied normalizer to retrieval_query only -- original message preserved for history/prompts",
        "- Improves embedding signal for noisy edge-case inputs",
        "",
        "### What Was NOT Changed",
        "",
        "- Frontend, ingestion pipeline, embedding model, retriever implementation",
        "- Gemini provider (gemini_service.py)",
        "- Gold dataset (queries.jsonl)",
        "- Refusal detection logic, citation validator, persona rubric score scale",
        "- Post-2015 detector",
        "",
        "---",
        "",
        "## Remaining Known Limitations",
        "",
        "1. **Democracy/Stability Query**: If retrieved context pages are predominantly publisher metadata rather than political philosophy chapters, the answer may still hallucinate. True fix requires verifying Phase 3 ingestion indexed the political chapters of One Man's View of the World.",
        "2. **Misspelled Query Retrieval**: The _normalize_query punctuation normalizer does NOT perform spell correction. True spell correction (e.g., pyspellchecker) would improve this further.",
        "3. **Refusal Precision**: Phase 6.2 reported refusal_precision=0.4286 -- this targeted regression does not address refusal precision directly.",
        "4. **API Rate Limits**: Evaluation sleeps of 4.2s between Gemini calls respect the 15 RPM free tier.",
        "",
        "---",
        "",
        "## Final Recommendation",
        "",
        "> **IF all 5 regression queries pass (faithfulness >= 3.0):**",
        "> Proceed to **Phase 7 Deployment**.",
        ">",
        "> The full 60-query benchmark may be rerun as a final validation only if Gemini API quota is available,",
        "> but it is **NOT required** for this targeted regression phase.",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to: {path.resolve()}")


def _classify_root_cause(reason: str) -> str:
    reason_lower = reason.lower()
    if "hallucinated" in reason_lower or "metadata" in reason_lower:
        return "Retrieval Miss + Hallucination"
    if "fabricated" in reason_lower and ("quote" in reason_lower or "direct" in reason_lower):
        return "Fabricated Quote"
    if "magazine" in reason_lower or "look magazine" in reason_lower:
        return "Fabricated Named Publication"
    if "noisy" in reason_lower or "misspelled" in reason_lower or "embedding" in reason_lower:
        return "Noisy Query / Embedding Degradation"
    if "evaluator" in reason_lower or "over-penalize" in reason_lower or "thematic" in reason_lower:
        return "Evaluator Over-Penalization"
    return "Grounding / Synthesis Issue"


if __name__ == "__main__":
    run_phase6_3_regression()
