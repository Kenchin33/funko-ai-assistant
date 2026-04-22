from fastapi import APIRouter, Query

from app.services.product_service import ProductService

router = APIRouter(prefix="/products")


@router.get("/search")
def search_products(q: str = Query(..., min_length=1)):
    return ProductService.search(q)


@router.get("/exact")
def exact_lookup_product(q: str = Query(..., min_length=1)):
    return ProductService.exact_lookup(q)