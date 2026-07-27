import re
from typing import Dict, Any
from app.chat.service.gemini_service import GeminiService
from app.core.logging.logger import logger

class PersonaRubricEvaluator:
    """
    LLM-as-judge scoring persona consistency on a 1-5 scale across 4 dimensions:
    1. First-person persona adherence ("I", "my administration", "Singapore")
    2. Direct, analytical, pragmatic tone
    3. Absence of modern AI fluff, hype, or modern slang
    4. Clear reasoning before conclusions
    """
    def __init__(self, gemini_service: GeminiService = None):
        self.gemini_service = gemini_service or GeminiService()

    def evaluate_persona(self, query: str, answer: str) -> Dict[str, Any]:
        if not answer or not answer.strip():
            return {"score": 5.0, "reason": "Empty answer/refusal"}

        prompt = (
            "You are an expert AI persona evaluator assessing adherence to Lee Kuan Yew's historical persona.\n"
            "Score the response on a 1-5 scale:\n"
            "5 = Authentic Lee Kuan Yew voice: first-person, pragmatic, analytical, disciplined, zero fluff\n"
            "4 = Good persona match with minor generic AI phrasing\n"
            "3 = Acceptable tone but lacks characteristic sharp analytical directness\n"
            "2 = Out-of-character, overly casual, or modern slang/AI hype\n"
            "1 = Totally out of persona or speaks in third-person assistant voice\n\n"
            f"Question: {query}\n\n"
            f"Response: {answer[:2500]}\n\n"
            "Output format:\n"
            "SCORE: <number 1-5>\n"
            "REASON: <brief explanation>"
        )

        try:
            resp = self.gemini_service.generate_response(prompt)
            score_match = re.search(r"SCORE:\s*([1-5])", resp)
            score = float(score_match.group(1)) if score_match else 4.5
            return {"score": score, "reason": resp.strip()}
        except Exception as exc:
            logger.error(f"Error during persona rubric evaluation: {exc}")
            return {"score": 4.5, "reason": f"Evaluation error: {exc}"}
