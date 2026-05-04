from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.integrations.shop_api_client import ShopApiClient
from app.schemas.chat import ChatMessageCreate
from app.services.chat_service import ChatService

router = APIRouter(prefix="/orders")


class OrderCheckRequest(BaseModel):
    session_id: int
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
def check_order(
    payload: OrderCheckRequest,
    db: Session = Depends(get_db),
):
    session = ChatService.get_session_by_id(db, payload.session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    user_message = ChatService.create_message(
        db=db,
        session_id=payload.session_id,
        payload=ChatMessageCreate(
            role="user",
            message_text=f"Перевірити замовлення {payload.order_number}",
            detected_intent="order_check_request",
            metadata_json=None,
        ),
    )

    order = ShopApiClient.get_order_status(
        order_number=payload.order_number,
        email=str(payload.email),
    )

    if not order:
        assistant_message = ChatService.create_message(
            db=db,
            session_id=payload.session_id,
            payload=ChatMessageCreate(
                role="assistant",
                message_text=(
                    "На жаль, я не знайшов замовлення з таким номером і email 😔\n"
                    "Перевірте правильність введених даних і спробуйте ще раз."
                ),
                detected_intent="order_check_result",
                metadata_json={
                    "found": False,
                    "actions": [],
                },
            ),
        )

        return {
            "found": False,
            "message": assistant_message.message_text,
            "user_message": user_message,
            "assistant_message": assistant_message,
        }

    order_url = (
        f"/track-order?"
        f"order_number={order['order_number']}"
        f"&email={order['email']}"
    )

    status_label = format_status(order["status"])

    message = (
        f"Я знайшов ваше замовлення {order['order_number']}.\n"
        f"Поточний статус: {status_label}."
    )

    if order["status"] == "shipped" and order.get("tracking_number"):
        message += f"\nТрек-номер відправлення: {order['tracking_number']}"

    message += "\n\nЧи можу я ще чимось допомогти?"

    actions = [
        {
            "type": "link",
            "label": "Відкрити замовлення",
            "url": order_url,
        }
    ]

    assistant_message = ChatService.create_message(
        db=db,
        session_id=payload.session_id,
        payload=ChatMessageCreate(
            role="assistant",
            message_text=message,
            detected_intent="order_check_result",
            metadata_json={
                "found": True,
                "order_number": order["order_number"],
                "actions": actions,
            },
        ),
    )

    return {
        "found": True,
        "message": message,
        "order": {
            **order,
            "order_url": order_url,
        },
        "user_message": user_message,
        "assistant_message": assistant_message,
    }