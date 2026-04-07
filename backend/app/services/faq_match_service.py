from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.faq import FAQEntry
from app.services.faq_service import FAQService
from app.utils.text import normalize_text, tokenize_text


@dataclass
class FAQMatchResult:
    matched: bool
    faq: FAQEntry | None = None
    score: int = 0


class FAQMatchService:
    @staticmethod
    def _build_search_text(faq: FAQEntry) -> str:
        parts = [
            faq.question or "",
            faq.keywords or "",
            faq.category or "",
        ]
        return normalize_text(" ".join(parts))

    @staticmethod
    def _score_message_against_faq(user_text: str, faq: FAQEntry) -> int:
        normalized_user_text = normalize_text(user_text)
        user_tokens = set(tokenize_text(user_text))
        faq_search_text = FAQMatchService._build_search_text(faq)
        faq_tokens = set(tokenize_text(faq_search_text))

        score = 0

        if normalized_user_text == normalize_text(faq.question):
            score += 100

        if normalize_text(faq.question) in normalized_user_text:
            score += 30

        for token in user_tokens:
            if token in faq_tokens:
                score += 10

        if faq.keywords:
            keyword_parts = [kw.strip().lower() for kw in faq.keywords.split(",") if kw.strip()]
            for keyword in keyword_parts:
                if keyword and keyword in normalized_user_text:
                    score += 20

        return score

    @staticmethod
    def find_best_match(db: Session, user_text: str) -> FAQMatchResult:
        faqs = FAQService.get_all(db)

        best_faq = None
        best_score = 0

        for faq in faqs:
            score = FAQMatchService._score_message_against_faq(user_text, faq)
            if score > best_score:
                best_score = score
                best_faq = faq

        if best_faq and best_score >= 30:
            return FAQMatchResult(
                matched=True,
                faq=best_faq,
                score=best_score,
            )

        return FAQMatchResult(
            matched=False,
            faq=None,
            score=best_score,
        )