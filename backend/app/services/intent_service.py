from app.utils.text import normalize_text


class IntentType:
    PRODUCT_SEARCH = "product_search"
    PRODUCT_EXACT = "product_exact"
    FAQ = "faq"
    LLM = "llm"
    UNKNOWN = "unknown"


class IntentService:
    PRODUCT_SEARCH_KEYWORDS = [
        "які є",
        "покажи",
        "знайди",
        "що є",
        "які фігурки",
        "мені потрібні фігурки",
        "фігурки",
        "які є в наявності",
        "чи є",
        "чи є у вас"
        "чи є у вас фігурки"
    ]

    PRODUCT_EXACT_HINTS = [
        "є",
        "чи є",
        "потрібні",
        "в наявності",
        "чи є у вас",
        "чи є у вас фігурки"
    ]

    LLM_HINTS = [
        "яка різниця",
        "чим відрізняється",
        "поясни",
        "поясни будь ласка",
        "що порадиш",
        "що краще",
        "порівняй",
        "розкажи",
    ]

    @staticmethod
    def detect_intent(message_text: str) -> str:
        text = normalize_text(message_text)

        if any(phrase in text for phrase in IntentService.LLM_HINTS):
            return IntentType.LLM

        if any(word in text for word in IntentService.PRODUCT_EXACT_HINTS):
            if any(char.isdigit() for char in text):
                return IntentType.PRODUCT_EXACT

        if any(keyword in text for keyword in IntentService.PRODUCT_SEARCH_KEYWORDS):
            return IntentType.PRODUCT_SEARCH

        return IntentType.FAQ