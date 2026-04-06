from app.core.database import Base, engine
from app.models import FAQEntry, ChatMessage, ChatSession


def init_db() -> None:
    Base.metadata.create_all(bind=engine)