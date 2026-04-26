from sqlalchemy.orm import Session
from urllib.parse import quote

from app.schemas.chat import ChatMessageCreate
from app.services.chat_service import ChatService
from app.services.faq_match_service import FAQMatchService
from app.services.intent_service import IntentService, IntentType
from app.services.product_service import ProductService
from app.services.llm_service import LLMService



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

        intent = IntentService.detect_intent(message_text)

        # ---------------- PRODUCT EXACT ----------------
        if intent == IntentType.PRODUCT_EXACT:
            product = ProductService.exact_lookup(message_text)

            if product:
                actions = [
                    {
                        "type": "link",
                        "label": "Відкрити товар",
                        "url": f"/product/{product['slug']}",
                    }
                ]

                assistant_message = ChatService.create_message(
                    db=db,
                    session_id=session_id,
                    payload=ChatMessageCreate(
                        role="assistant",
                        message_text=f"Так, знайшов фігурку:\n{product['name']}",
                        detected_intent="product_exact",
                        metadata_json={
                            "product_slug": product["slug"],
                            "actions": actions,
                        },
                    ),
                )

                return {
                    "session_id": session_id,
                    "user_message": user_message,
                    "assistant_message": assistant_message,
                    "matched_faq_id": None,
                    "matched_intent": "product_exact",
                    "actions": actions,
                }

            # не знайдено
            assistant_message = ChatService.create_message(
                db=db,
                session_id=session_id,
                payload=ChatMessageCreate(
                    role="assistant",
                    message_text="На жаль, я не знайшов таку фігурку в наявності 😔",
                    detected_intent="product_exact_not_found",
                    metadata_json={},
                ),
            )

            return {
                "session_id": session_id,
                "user_message": user_message,
                "assistant_message": assistant_message,
                "matched_faq_id": None,
                "matched_intent": "product_exact_not_found",
                "actions": [],
            }

        # ---------------- PRODUCT SEARCH ----------------
        if intent == IntentType.PRODUCT_SEARCH:
            cleaned_query = ProductService.clean_search_query(message_text)
            products = ProductService.search(message_text)

            if products:
                actions = [
                    {
                        "type": "link",
                        "label": "Переглянути результати",
                        "url": f"/search?q={quote(cleaned_query)}",
                    }
                ]

                assistant_message = ChatService.create_message(
                    db=db,
                    session_id=session_id,
                    payload=ChatMessageCreate(
                        role="assistant",
                        message_text=f"Я знайшов кілька варіантів за вашим запитом \"{message_text}\" 👇",
                        detected_intent="product_search",
                        metadata_json={
                            "products_found": len(products),
                            "product_slugs": [product["slug"] for product in products[:5]],
                            "actions": actions,
                        },
                    ),
                )

                return {
                    "session_id": session_id,
                    "user_message": user_message,
                    "assistant_message": assistant_message,
                    "matched_faq_id": None,
                    "matched_intent": "product_search",
                    "actions": actions,
                }

            assistant_message = ChatService.create_message(
                db=db,
                session_id=session_id,
                payload=ChatMessageCreate(
                    role="assistant",
                    message_text="На жаль, я нічого не знайшов за вашим запитом 😔",
                    detected_intent="product_search_not_found",
                    metadata_json={},
                ),
            )

            return {
                "session_id": session_id,
                "user_message": user_message,
                "assistant_message": assistant_message,
                "matched_faq_id": None,
                "matched_intent": "product_search_not_found",
                "actions": [],
            }
        
        # ---------------- LLM DIRECT ----------------
        if intent == IntentType.LLM:
            llm = LLMService()
            ai_text, provider = llm.generate_reply(message_text)

            assistant_message = ChatService.create_message(
                db=db,
                session_id=session_id,
                payload=ChatMessageCreate(
                    role="assistant",
                    message_text=ai_text,
                    detected_intent="llm_fallback",
                    metadata_json={
                        "model": provider,
                    },
                ),
            )

            return {
                "session_id": session_id,
                "user_message": user_message,
                "assistant_message": assistant_message,
                "matched_faq_id": None,
                "matched_intent": "llm_fallback",
                "actions": [],
            }


        # ---------------- FAQ ----------------
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

        # ---------------- LLM FALLBACK ----------------
        llm = LLMService()

        ai_text, provider = llm.generate_reply(message_text)

        assistant_message = ChatService.create_message(
            db=db,
            session_id=session_id,
            payload=ChatMessageCreate(
                role="assistant",
                message_text=ai_text,
                detected_intent="llm_fallback",
                metadata_json={
                    "model": provider,
                },
            ),
        )

        return {
            "session_id": session_id,
            "user_message": user_message,
            "assistant_message": assistant_message,
            "matched_faq_id": None,
            "matched_intent": "llm_fallback",
            "actions": [],
        }