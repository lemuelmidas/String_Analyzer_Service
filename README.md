# A String Analyzer Service using (Django + DRF)

## Overview
This is a django-based RESTful API that analyzes strings and stores computed properties such as:
- length, is_palindrome, unique_characters, word_count, sha256_hash, character_frequency_map

## Guide

1. Clone repo
2. Create virtualenv & install:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Run migrations:
   python manage.py migrate

4. Run server:
   python manage.py runserver

## Endpoints
1. Create / Analyze
   POST /strings
   Body: { "value": "string to analyze" }
   Responses:
     201 Created - created object
     409 Conflict - already exists
     400/422 - bad input

2. Get specific string (by raw value)
   GET /strings/{urlencoded_string}
   200 / 404

3. List with filters
   GET /strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a

4. Natural language filter
   GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings

5. Delete
   DELETE /strings/{urlencoded_string}

## Tests
Run:
   python manage.py test analyzer

## Notes
- This project uses SQLite by default for local dev.
- The `sha256_hash` field is used as the primary key.
- Natural-language parsing is intentionally simple and rule-based; extend `analyzer/utils.py::parse_natural_language_query` to support more phrases.

