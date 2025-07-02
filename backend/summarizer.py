from transformers import pipeline
import re

def summarize_text(text):
    # Initialize BART summarizer
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # Split text into chunks if too long (BART has a max token limit)
    max_chunk_len = 1024
    chunks = [text[i:i+max_chunk_len] for i in range(0, len(text), max_chunk_len)]
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)

def extract_action_items(text):
    # Initialize BART for text generation (to refine action items)
    generator = pipeline("text2text-generation", model="facebook/bart-large")
    
    # Rule-based action item detection (e.g., look for verbs like "assigned", "do", "complete")
    action_keywords = r'\b(assigned|to do|complete|action|responsible|task)\b.*?(?=\n|\.)'
    action_items = re.findall(action_keywords, text, re.IGNORECASE)
    
    # Refine action items using BART
    refined_items = []
    for item in action_items:
        prompt = f"Convert this to a concise action item: {item}"
        refined = generator(prompt, max_length=50, do_sample=False)[0]['generated_text']
        refined_items.append(f"- {refined}")
    
    return "\n".join(refined_items) if refined_items else "No action items detected."