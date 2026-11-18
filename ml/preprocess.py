"""
Text Preprocessing module for FormPilot AI Document Intelligence.
Handles text cleaning, tokenization, normalization, and stopword filtering for both English and Tamil text.
"""
import re
import unicodedata

# Common English and domain-specific stopwords
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", 
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "me", "more", 
    "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", 
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should", "so", 
    "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", 
    "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", 
    "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
}

def clean_text(text: str) -> str:
    """Clean and normalize extracted document text."""
    if not text:
        return ""
    
    # Normalize unicode (NFKC)
    text = unicodedata.normalize("NFKC", text)
    
    # Lowercase
    text = text.lower()
    
    # Replace newlines, tabs, and multiple spaces with a single space
    text = re.sub(r"[\r\n\t]+", " ", text)
    
    # Remove special punctuation but keep alphanumeric and basic hyphens
    text = re.sub(r"[^\w\s\u0B80-\u0BFF-]", " ", text)
    
    # Tokenize and filter stopwords and short tokens
    tokens = text.split()
    filtered = [t for t in tokens if len(t) > 1 and t not in STOPWORDS]
    
    return " ".join(filtered)

def extract_keywords(text: str, top_k: int = 10) -> list[str]:
    """Extract frequent informative words."""
    cleaned = clean_text(text)
    words = cleaned.split()
    freq = {}
    for w in words:
        if len(w) > 3:
            freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:top_k]]
