import re

from app.integrations.shop_api_client import ShopApiClient
from app.utils.text import normalize_text


class ProductService:
    @staticmethod
    def _clean_search_query(query: str) -> str:
        normalized = normalize_text(query)

        noise_phrases = [
            "які є фігурки по",
            "які є по",
            "що є по",
            "чи є у вас фігурки",
            "чи є у вас",
            "чи є",
            "які є по",
            "що є",
            "покажи",
            "знайди",
            "funko pop",
            "фігурки",
            "фігурка",
            "є",
        ]

        cleaned = normalized

        for phrase in sorted(noise_phrases, key=len, reverse=True):
            cleaned = cleaned.replace(phrase, " ")

        cleaned = re.sub(r"[^\w\s-]", " ", cleaned)
        cleaned = " ".join(cleaned.split())
        return cleaned.strip()
    
    @staticmethod
    def clean_search_query(query: str) -> str:
        return ProductService._clean_search_query(query)

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

        number_match = re.search(r"\d+", cleaned_query)
        product_number_query = number_match.group(0) if number_match else None

        def product_search_text(product: dict) -> str:
            aliases = product.get("aliases") or []
            alias_text = " ".join(
                str(alias.get("alias") or "")
                for alias in aliases
                if isinstance(alias, dict)
            )

            return normalize_text(
                " ".join(
                    [
                        str(product.get("name") or ""),
                        str(product.get("slug") or ""),
                        str(product.get("series") or ""),
                        str(product.get("product_number") or ""),
                        alias_text,
                    ]
                )
            )

        if product_number_query:
            products_by_number = ShopApiClient.search_products(
                q=product_number_query,
                limit=10,
            )

            exact_number_product = None

            for product in products_by_number:
                product_number = str(product.get("product_number") or "").strip()

                if product_number == product_number_query:
                    exact_number_product = product
                    break

            if not exact_number_product:
                return None

            query_without_number = re.sub(
                r"\d+",
                " ",
                cleaned_query,
            )
            query_without_number = " ".join(query_without_number.split())

            if not query_without_number:
                return exact_number_product

            searchable_text = product_search_text(exact_number_product)
            query_words = query_without_number.split()

            if all(word in searchable_text for word in query_words):
                return exact_number_product

            return None

        products = ShopApiClient.search_products(q=cleaned_query, limit=10)

        if not products:
            return None

        normalized_query = cleaned_query.lower()

        for product in products:
            searchable_text = product_search_text(product)
            product_number = str(product.get("product_number") or "").lower()

            if normalized_query in searchable_text:
                return product

            if product_number and normalized_query == product_number:
                return product

        return products[0]