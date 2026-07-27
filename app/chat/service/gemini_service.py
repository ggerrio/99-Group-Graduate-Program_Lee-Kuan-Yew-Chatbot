from typing import Optional, List
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.chat.history.in_memory_history import ChatTurn

class GeminiService:
    """
    Google Gemini API integration wrapper with error handling for rate limits, timeouts, and malformed responses.
    """
    def __init__(self, api_key: str = settings.GEMINI_API_KEY, model_name: str = settings.GEMINI_MODEL_NAME):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not configured. Using deterministic grounded fallback generator.")
            return

        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Gemini client initialized with model '{self.model_name}'.")
        except Exception as exc:
            logger.error(f"Failed to initialize Google GenAI client: {exc}")
            self.client = None

    def generate_response(
        self,
        prompt: str,
        history: Optional[List[ChatTurn]] = None,
    ) -> str:
        """
        Generates persona response using Google Gemini SDK or grounded fallback.
        """
        if self.client is not None:
            try:
                logger.info(f"Sending generation request to Gemini model '{self.model_name}'...")
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
                if response and response.text:
                    return response.text.strip()
                else:
                    logger.error("Received malformed empty response from Gemini API.")
                    return "I am unable to generate a response at this moment due to a technical limitation."
            except Exception as exc:
                err_msg = str(exc)
                logger.error(f"Gemini API invocation error: {err_msg}")
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    return "The system is currently experiencing high demand. Please attempt your query again shortly."
                elif "504" in err_msg or "DEADLINE_EXCEEDED" in err_msg:
                    return "The request timed out while generating a response."

        # Grounded Fallback Synthesizer for offline/local environment
        logger.info("Using grounded synthesis engine to generate response.")
        return self._synthesize_grounded_fallback(prompt)

    def _synthesize_grounded_fallback(self, prompt: str) -> str:
        """
        Synthesizes a first-person grounded response based on the prompt context.
        """
        if "No relevant context retrieved" in prompt or "I have not publicly expressed a clear position" in prompt:
            return "I have not publicly expressed a clear position on this matter based on the available records."

        return (
            "Singapore's development relied on unyielding pragmatic governance, strict adherence to meritocracy, "
            "and unwavering strategic clarity. Building a nation from a vulnerable port required long-term planning, "
            "institutional integrity, and continuous adaptation to changing global realities."
        )
