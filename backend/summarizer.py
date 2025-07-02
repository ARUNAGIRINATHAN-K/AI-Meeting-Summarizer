from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

import nltk
import re

nltk.download("punkt")


def summarize_text(text, sentence_count=5):
    """
    Summarizes the given transcript using TextRank.
    """
    if not text.strip():
        return "No transcript available."

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, sentence_count)

    summary = " ".join(str(sentence) for sentence in summary_sentences)
    return summary if summary else "Summary not generated."


def extract_action_items(text):
    """
    Extracts simple action items from the transcript based on patterns.
    """
    action_keywords = ["will", "must", "should", "need to", "have to", "plan to", "schedule", "assign", "complete", "follow up", "remind"]
    
    # Break into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    action_items = []

    for sentence in sentences:
        lower = sentence.lower()
        if any(keyword in lower for keyword in action_keywords):
            action_items.append(sentence.strip())

    return action_items if action_items else ["No action items found."]
