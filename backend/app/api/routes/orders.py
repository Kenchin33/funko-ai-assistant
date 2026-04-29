from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException, status

from app.integrations.shop_api_client import ShopApiClient

router = APIRouter(prefix="/orders")


class OrderCheckRequest(BaseModel):
    order_number: str
    email: EmailStr


def format_status(status_value: str) -> str:
    match status_value:
        case "new":
            return "Нове"
        case "shipped":
            return "Відправлено"
        case "resolved":
            return "Завершене"
        case "rejected":
            return "Скасоване"
        case _:
            return status_value


@router.post("/check")
def check_order(payload: OrderCheckRequest):
    order = ShopApiClient.get_order_status(
        order_number=payload.order_number,
        email=str(payload.email),
    )

    if not order:
        return {
            "found": False,
            "message": (
                "На жаль, я не знайшов замовлення з таким номером і email 😔\n"
                "Перевірте правильність введених даних і спробуйте ще раз."
            ),
        }

    status_label = format_status(order["status"])

    message = (
        f"Я знайшов ваше замовлення {order['order_number']}.\n"
        f"Поточний статус: {status_label}."
    )

    if order["status"] == "shipped" and order.get("tracking_number"):
        message += f"\nТрек-номер відправлення: {order['tracking_number']}"

    message += "\n\nЧи можу я ще чимось допомогти?"

    return {
        "found": True,
        "message": message,
        "order": {
            **order,
            "order_url": (
                f"/track-order?"
                f"order_number={order['order_number']}"
                f"&email={order['email']}"
            ),
        },
    }