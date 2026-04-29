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
            "чи є у вас фігурки по",
            "чи є у вас",
            "чи є",
            "які є по",
            "що є з",
            "покажи",
            "знайди",
            "funko pop",
            "фігурки",
            "фігурка",
            "фігурки по",
            "фігурка по",
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

        if product_number_query:
            query_without_number = re.sub(r"\d+", " ", cleaned_query)
            query_without_number = " ".join(query_without_number.split())

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

            if not query_without_number:
                return exact_number_product

            products_by_text = ShopApiClient.search_products(
                q=query_without_number,
                limit=10,
            )

            for product in products_by_text:
                product_number = str(product.get("product_number") or "").strip()

                if product_number == product_number_query:
                    return product

            return None

        products = ShopApiClient.search_products(q=cleaned_query, limit=10)

        if not products:
            return None

        normalized_query = cleaned_query.lower()

        for product in products:
            name = (product.get("name") or "").lower()
            slug = (product.get("slug") or "").lower()
            product_number = str(product.get("product_number") or "").lower()
            series = (product.get("series") or "").lower()

            if normalized_query in name or normalized_query in slug:
                return product

            if product_number and normalized_query == product_number:
                return product

            if series and normalized_query in series and len(products) == 1:
                return product

        return products[0]
    
    @staticmethod
    def exact_lookup_many(query: str) -> list[dict]:
        cleaned_query = ProductService._clean_search_query(query)

        number_match = re.search(r"\d+", cleaned_query)
        product_number_query = number_match.group(0) if number_match else None

        if not product_number_query:
            product = ProductService.exact_lookup(query)
            return [product] if product else []

        products = ShopApiClient.search_products(
            q=product_number_query,
            limit=20,
        )

        matched_products = []

        for product in products:
            product_number = str(product.get("product_number") or "").strip()

            if product_number == product_number_query:
                matched_products.append(product)

        return matched_products