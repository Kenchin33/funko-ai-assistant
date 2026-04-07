from app.utils.text import normalize_text


class IntentType:
    PRODUCT_SEARCH = "product_search"
    PRODUCT_EXACT = "product_exact"
    FAQ = "faq"
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
        "які є в наявності"
    ]

    PRODUCT_EXACT_HINTS = [
        "є",
        "чи є",
        "потрібні",
        "в наявності"
    ]

    @staticmethod
    def detect_intent(message_text: str) -> str:
        text = normalize_text(message_text)

        # Exact lookup (якщо є цифри або SKU)
        if any(word in text for word in IntentService.PRODUCT_EXACT_HINTS):
            if any(char.isdigit() for char in text):
                return IntentType.PRODUCT_EXACT

        # Product search
        if any(keyword in text for keyword in IntentService.PRODUCT_SEARCH_KEYWORDS):
            return IntentType.PRODUCT_SEARCH

        # fallback → FAQ
        return IntentType.FAQ