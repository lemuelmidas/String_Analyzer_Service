import hashlib, re, collections

def compute_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def compute_properties(value: str) -> dict:
    length = len(value)
    normalized = re.sub(r'\s+', '', value).lower()
    is_palindrome = normalized == normalized[::-1] and len(normalized) > 0
    unique_characters = len(set(value))
    word_count = len(value.split())
    freq = dict(collections.Counter(value))

    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": compute_sha256(value),
        "character_frequency_map": freq,
    }

def parse_natural_language_query(query: str):
    q = query.lower().strip()
    filters = {}

    if "palindrom" in q:
        filters["is_palindrome"] = True
    if "single word" in q or "one word" in q:
        filters["word_count"] = 1
    if "longer than" in q:
        import re
        m = re.search(r"longer than (\d+)", q)
        if m:
            filters["min_length"] = int(m.group(1)) + 1
    if "containing the letter" in q:
        m = re.search(r"containing the letter (\w)", q)
        if m:
            filters["contains_character"] = m.group(1)
    if "first vowel" in q:
        filters["contains_character"] = "a"

    if not filters:
        raise ValueError("Unable to parse query")

    return filters
