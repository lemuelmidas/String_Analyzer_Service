import hashlib
from collections import Counter

def analyze_string(text):
    text_clean = text.strip()
    return {
        "length": len(text_clean),
        "is_palindrome": text_clean.lower() == text_clean[::-1].lower(),
        "unique_characters": len(set(text_clean)),
        "word_count": len(text_clean.split()),
        "sha256_hash": hashlib.sha256(text_clean.encode()).hexdigest(),
        "character_frequency_map": dict(Counter(text_clean))
    }
