import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("’", "'").replace("`", "'")
    text = re.sub(r"[^\w\s']+", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_text(text: str) -> list[str]:
    normalized = normalize_text(text)
    return [token for token in normalized.split(" ") if token]