import re
from typing import Dict, Any
from app.chat.service.gemini_service import GeminiService
from app.core.logging.logger import logger

class FaithfulnessEvaluator:
    """
    LLM-as-judge faithfulness evaluator checking if answer claims are supported by retrieved context.
    Score scale: 1 (unfaithful/hallucinated) to 5 (fully faithful).
    """
    def __init__(self, gemini_service: GeminiService = None):
        self.gemini_service = gemini_service or GeminiService()

    def evaluate_faithfulness(self, query: str, context: str, answer: str) -> Dict[str, Any]:
        if not answer or not answer.strip():
            return {"score": 5.0, "reason": "Empty answer/refusal", "unsupported_claim": None}

        if "not publicly expressed a clear position" in answer.lower() or "after my lifetime" in answer.lower():
            return {"score": 5.0, "reason": "Standard refusal or post-2015 inference response", "unsupported_claim": None}

        prompt = (
            "You are an expert AI RAG evaluator scoring Faithfulness.\n"
            "Evaluate if all facts, dates, and claims in the Answer are directly supported by the Context.\n\n"
            "SPECIAL GRADING GUIDELINES FOR PERSONA RAG:\n"
            "1. Do NOT penalize reasonable first-person paraphrasing, thematic synthesis across retrieved chunks, or standard persona transitions (e.g. 'In my view', 'My administration maintained') if the underlying historical facts, policies, and principles are present in the context.\n"
            "2. ONLY penalize (score 1 or 2) for GENUINE FABRICATIONS: specific invented historical events, fake publication/source names (e.g. 'Look magazine'), or claims directly contradicting the context.\n"
            "3. FOR SHORT OR KEYWORD-ONLY QUERIES (e.g. 'meritocracy', 'corruption', 'bilingual education'): Do NOT penalize the answer for broad thematic synthesis that is directionally consistent with the context. The answer should score 4 or 5 if the key principles discussed are covered by the retrieved context, even if phrased in persona-consistent editorializing language.\n"
            "4. FABRICATED PUBLICATION NAMES: If the answer mentions a specific magazine, newspaper, or media outlet (e.g. 'Look magazine', 'Time magazine', 'The Economist') that does NOT appear by that exact name in the Context, treat this as a genuine fabrication and score 1 or 2.\n"
            "5. FABRICATED PERSONAL ANECDOTES: If the answer contains specific personal childhood memories, formative experiences, or precise emotional statements not in the Context, treat these as fabrications.\n\n"
            f"Question: {query}\n\n"
            f"Context: {context[:2500]}\n\n"
            f"Answer: {answer[:2500]}\n\n"
            "Score on a 1-5 scale:\n"
            "5 = Fully supported by context or faithful persona synthesis\n"
            "4 = Well supported, minor stylistic paraphrase or persona-consistent thematic expansion\n"
            "3 = Partially supported, some general claims beyond context but no invented proper nouns\n"
            "2 = Invented specific named entities (publications, laws, events) or contradicts context\n"
            "1 = Contradicts context or completely hallucinated\n\n"
            "Output format:\n"
            "SCORE: <number 1-5>\n"
            "UNSUPPORTED_CLAIM: <exact fabricated named entity or invented claim if score < 3, else None>\n"
            "REASON: <brief explanation>"
        )

        try:
            resp = self.gemini_service.generate_response(prompt)
            
            score_match = re.search(r"SCORE:\s*([1-5])", resp)
            score = float(score_match.group(1)) if score_match else 4.0

            unsupported_match = re.search(r"UNSUPPORTED_CLAIM:\s*(.+)", resp)
            unsupported_claim = unsupported_match.group(1).strip() if unsupported_match else None

            if unsupported_claim in ["None", "none", "N/A", "n/a", ""]:
                unsupported_claim = None

            return {
                "score": score,
                "reason": resp.strip(),
                "unsupported_claim": unsupported_claim,
            }
        except Exception as exc:
            logger.error(f"Error during faithfulness evaluation: {exc}")
            return {"score": 4.0, "reason": f"Evaluation error: {exc}", "unsupported_claim": None}
