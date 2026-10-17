# anonymizer.py
import re

def anonymize(text):
    text = re.sub(r'\+?996[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{3}', '[PHONE]', text)
    text = re.sub(r'\b0\d{3}[\s\-]?\d{3}[\s\-]?\d{3}\b', '[PHONE]', text)
    text = re.sub(r'\b\d{9,12}\b', '[PHONE]', text)
    text = re.sub(r'\bул\.?\s+\w+', '[ADDRESS]', text, flags=re.IGNORECASE)
    text = re.sub(r'\bулица\s+\w+', '[ADDRESS]', text, flags=re.IGNORECASE)
    text = re.sub(r'\bдом\s+\d+', '[ADDRESS]', text, flags=re.IGNORECASE)
    text = re.sub(r'\bкв\.?\s+\d+', '[ADDRESS]', text, flags=re.IGNORECASE)
    text = re.sub(r'@\w+', '[USER]', text)
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    return text.strip()