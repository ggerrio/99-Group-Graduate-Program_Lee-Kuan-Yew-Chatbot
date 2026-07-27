import re
from typing import List
from dataclasses import dataclass

@dataclass
class RawChunk:
    text: str
    start_char: int
    end_char: int

class SemanticSplitter:
    """
    Sentence and paragraph-aware semantic text splitter maintaining target token range and overlap.
    """
    def __init__(self, target_chunk_size: int = 750, chunk_overlap: int = 150):
        self.target_chunk_size = target_chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[RawChunk]:
        """
        Splits clean document text into semantic chunks respecting paragraph and sentence boundaries.
        """
        if not text or not text.strip():
            return []

        # Split document into paragraphs first
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks: List[RawChunk] = []

        current_chunk_paragraphs: List[str] = []
        current_length = 0

        for para in paragraphs:
            para_len = len(para)

            # If adding this paragraph exceeds target chunk size and we already have content
            if current_length + para_len > self.target_chunk_size and current_chunk_paragraphs:
                chunk_text = "\n\n".join(current_chunk_paragraphs)
                chunks.append(RawChunk(text=chunk_text, start_char=0, end_char=len(chunk_text)))

                # Calculate overlap by retaining trailing paragraphs
                overlap_paragraphs: List[str] = []
                overlap_len = 0
                for prev_para in reversed(current_chunk_paragraphs):
                    if overlap_len + len(prev_para) <= self.chunk_overlap:
                        overlap_paragraphs.insert(0, prev_para)
                        overlap_len += len(prev_para)
                    else:
                        break

                current_chunk_paragraphs = overlap_paragraphs
                current_length = overlap_len

            # If single paragraph itself is larger than target_chunk_size, split by sentences
            if para_len > self.target_chunk_size:
                sentences = re.split(r"(?<=[.!?])\s+", para)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    sentence_len = len(sentence)
                    if current_length + sentence_len > self.target_chunk_size and current_chunk_paragraphs:
                        chunk_text = "\n\n".join(current_chunk_paragraphs)
                        chunks.append(RawChunk(text=chunk_text, start_char=0, end_char=len(chunk_text)))
                        current_chunk_paragraphs = []
                        current_length = 0

                    current_chunk_paragraphs.append(sentence)
                    current_length += sentence_len
            else:
                current_chunk_paragraphs.append(para)
                current_length += para_len

        # Append trailing remaining content
        if current_chunk_paragraphs:
            chunk_text = "\n\n".join(current_chunk_paragraphs)
            chunks.append(RawChunk(text=chunk_text, start_char=0, end_char=len(chunk_text)))

        return chunks
