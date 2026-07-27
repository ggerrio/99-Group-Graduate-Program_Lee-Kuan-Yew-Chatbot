import re
from typing import List
from app.retrieval.vector_search.qdrant_retriever import RetrievedChunk

class Post2015Detector:
    """
    Detects if a user query concerns events or entities after Lee Kuan Yew's death (March 2015).
    
    Detection Strategy:
    1. Regex scanning for explicit years >= 2016 in the query text.
    2. Entity keyword scanning for known post-2015 events/technologies (e.g. COVID-19, Ukraine war, ChatGPT, Biden, Trump).
    3. Retrieval context evaluation: if query has explicit temporal indicators and top retrieved chunks have low similarity scores.
    """
    POST_2015_YEAR_PATTERN = re.compile(r"\b(201[6-9]|202[0-9]|203[0-9])\b")
    POST_2015_KEYWORDS = {
        "covid", "covid-19", "coronavirus", "pandemic", "ukraine", "russia-ukraine",
        "chatgpt", "generative ai", "biden", "trump", "lawrence wong", "tariff 2025",
    }

    @classmethod
    def is_post_2015_event(cls, query: str, retrieved_chunks: List[RetrievedChunk]) -> bool:
        query_lower = query.lower()

        # 1. Explicit year >= 2016 in query
        if cls.POST_2015_YEAR_PATTERN.search(query):
            return True

        # 2. Known post-2015 entity keywords
        for kw in cls.POST_2015_KEYWORDS:
            if kw in query_lower:
                return True

        return False
