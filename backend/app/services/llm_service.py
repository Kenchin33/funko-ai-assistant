import requests

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        self.url = (
            f"https://generativelanguage.googleapis.com/v1/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

    def generate_reply(self, user_message: str) -> str:
        system_prompt = (
            "Ти AI-асистент інтернет-магазину колекційних фігурок Funko Pop. "
            "Назва магазину - Funko Hunter"
            "Відповідай лише по темі магазину: товари, доставка, оплата, "
            "передзамовлення, наявність, поради покупцю. "
            "Якщо питання не стосується магазину, ввічливо скажи, що можеш "
            "допомогти лише з питаннями магазину. "
            "Відповідай коротко, корисно і українською мовою."
        )

        full_prompt = f"{system_prompt}\n\nКористувач: {user_message}"

        try:
            response = requests.post(
                self.url,
                json={
                    "contents": [
                        {
                            "parts": [
                                {"text": full_prompt}
                            ]
                        }
                    ]
                },
                timeout=20,
            )

            if response.status_code != 200:
                print("LLM ERROR STATUS:", response.status_code)
                print("LLM ERROR BODY:", response.text)
                return "Зараз AI-відповідь тимчасово недоступна. Спробуйте ще раз трохи пізніше."

            data = response.json()

            candidates = data.get("candidates", [])
            if not candidates:
                print("LLM EMPTY RESPONSE:", data)
                return "Не вдалося отримати відповідь від AI."

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                print("LLM EMPTY PARTS:", data)
                return "Не вдалося отримати текст відповіді від AI."

            text = parts[0].get("text", "").strip()
            if not text:
                print("LLM EMPTY TEXT:", data)
                return "AI не повернув текст відповіді."

            return text

        except requests.RequestException as e:
            print("LLM REQUEST ERROR:", e)
            return "Помилка з'єднання з AI-сервісом."
        except Exception as e:
            print("LLM UNKNOWN ERROR:", e)
            return "Виникла помилка при генерації відповіді."