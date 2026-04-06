from sqlalchemy.orm import Session

from app.schemas.chat import ChatMessageCreate
from app.services.chat_service import ChatService
from app.services.faq_match_service import FAQMatchService


class ChatReplyService:
    @staticmethod
    def process_user_message(db: Session, session_id: int, message_text: str):
        user_message = ChatService.create_message(
            db=db,
            session_id=session_id,
            payload=ChatMessageCreate(
                role="user",
                message_text=message_text,
                detected_intent=None,
                metadata_json=None,
            ),
        )

        faq_match = FAQMatchService.find_best_match(db, message_text)

        if faq_match.matched and faq_match.faq:
            actions = []
            if faq_match.faq.button_label and faq_match.faq.button_url:
                actions.append(
                    {
                        "type": "link",
                        "label": faq_match.faq.button_label,
                        "url": faq_match.faq.button_url,
                    }
                )

            assistant_message = ChatService.create_message(
                db=db,
                session_id=session_id,
                payload=ChatMessageCreate(
                    role="assistant",
                    message_text=faq_match.faq.answer,
                    detected_intent="faq_match",
                    metadata_json={
                        "faq_id": faq_match.faq.id,
                        "faq_category": faq_match.faq.category,
                        "match_score": faq_match.score,
                        "actions": actions,
                    },
                ),
            )

            return {
                "session_id": session_id,
                "user_message": user_message,
                "assistant_message": assistant_message,
                "matched_faq_id": faq_match.faq.id,
                "matched_intent": "faq_match",
                "actions": actions,
            }

        fallback_text = (
            "Поки що я не знайшов точної відповіді на ваше запитання в базі магазину. "
            "Спробуйте уточнити запит або поставити питання про доставку, оплату, "
            "повернення, передзамовлення, наявність чи контакти."
        )

        assistant_message = ChatService.create_message(
            db=db,
            session_id=session_id,
            payload=ChatMessageCreate(
                role="assistant",
                message_text=fallback_text,
                detected_intent="fallback",
                metadata_json={
                    "reason": "no_faq_match",
                },
            ),
        )

        return {
            "session_id": session_id,
            "user_message": user_message,
            "assistant_message": assistant_message,
            "matched_faq_id": None,
            "matched_intent": "fallback",
            "actions": [],
        }