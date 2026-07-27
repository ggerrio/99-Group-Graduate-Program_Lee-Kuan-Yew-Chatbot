import re

class TextCleaner:
    """
    Normalizes raw extracted PDF text while preserving historical terminology, years, quotes, and structural formatting.
    """
    PAGE_NUMBER_PATTERN = re.compile(r"^\s*(?:Page\s*\d+|\d+|\d+\s*of\s*\d+|Page\s*\d+\s*of\s*\d+)\s*$", re.IGNORECASE)
    HEADER_FOOTER_PATTERN = re.compile(r"^\s*(?:Lee\s+Kuan\s+Yew\s+Speeches|Official\s+Transcript|Confidential|Draft)\s*$", re.IGNORECASE)

    @classmethod
    def clean_text(cls, raw_text: str) -> str:
        if not raw_text:
            return ""

        # Normalize line endings
        text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

        # Strip control characters except newline and tab
        text = "".join(ch for ch in text if ch in ("\n", "\t") or ch >= " ")

        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()

            # Skip empty running headers/footers or page numbers
            if cls.PAGE_NUMBER_PATTERN.match(stripped):
                continue
            if cls.HEADER_FOOTER_PATTERN.match(stripped):
                continue

            # Remove excessive inner spaces while retaining tabs
            cleaned_line = re.sub(r"[ \t]+", " ", line)
            cleaned_lines.append(cleaned_line)

        cleaned_text = "\n".join(cleaned_lines)

        # Merge broken line wraps within paragraphs (word-\nword -> wordword)
        cleaned_text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", cleaned_text)

        # Replace 3 or more consecutive newlines with 2 newlines (preserve paragraph boundaries)
        cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

        return cleaned_text.strip()
