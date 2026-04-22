import requests

from app.core.config import settings


class ShopApiClient:
    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "X-Assistant-Api-Key": settings.SHOP_ASSISTANT_API_KEY,
        }

    @staticmethod
    def search_products(
        q: str,
        category: str | None = None,
        subcategory: str | None = None,
        rarity: str | None = None,
        availability_status: str | None = None,
        is_box_damaged: bool | None = None,
        limit: int = 10,
    ) -> list[dict]:
        response = requests.get(
            f"{settings.SHOP_API_BASE_URL}/assistant/products/search",
            headers=ShopApiClient._headers(),
            params={
                "q": q,
                "category": category,
                "subcategory": subcategory,
                "rarity": rarity,
                "availability_status": availability_status,
                "is_box_damaged": is_box_damaged,
                "limit": limit,
            },
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_product_by_slug(slug: str) -> dict:
        response = requests.get(
            f"{settings.SHOP_API_BASE_URL}/assistant/products/by-slug/{slug}",
            headers=ShopApiClient._headers(),
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_complaint(payload: dict) -> dict:
        response = requests.post(
            f"{settings.SHOP_API_BASE_URL}/assistant/complaints",
            headers=ShopApiClient._headers(),
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()