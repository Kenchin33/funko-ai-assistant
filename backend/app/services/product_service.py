from app.integrations.shop_api_client import ShopApiClient


class ProductService:
    @staticmethod
    def _clean_search_query(query: str) -> str:
        normalized = query.strip().lower()

        noise_phrases = [
            "які є фігурки по",
            "які є по",
            "що є по",
            "покажи",
            "знайди",
            "які є",
            "що є",
            "є",
            "чи є",
            "funko pop",
            "фігурки",
            "фігурка",
        ]

        cleaned = normalized
        for phrase in noise_phrases:
            cleaned = cleaned.replace(phrase, " ")

        cleaned = " ".join(cleaned.split())
        return cleaned

    @staticmethod
    def get_all() -> list[dict]:
        return ShopApiClient.search_products(q="", limit=50)

    @staticmethod
    def get_by_slug(slug: str) -> dict | None:
        try:
            return ShopApiClient.get_product_by_slug(slug)
        except Exception:
            return None

    @staticmethod
    def search(query: str) -> list[dict]:
        cleaned_query = ProductService._clean_search_query(query)
        return ShopApiClient.search_products(q=cleaned_query, limit=10)

    @staticmethod
    def exact_lookup(query: str) -> dict | None:
        cleaned_query = ProductService._clean_search_query(query)
        products = ShopApiClient.search_products(q=cleaned_query, limit=10)

        if not products:
            return None

        normalized_query = cleaned_query.lower()

        for product in products:
            name = (product.get("name") or "").lower()
            slug = (product.get("slug") or "").lower()
            product_number = (product.get("product_number") or "").lower()
            series = (product.get("series") or "").lower()

            if normalized_query in name or normalized_query in slug:
                return product

            if product_number and normalized_query == product_number:
                return product

            if series and normalized_query in series and len(products) == 1:
                return product

        return products[0]