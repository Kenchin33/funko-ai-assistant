import requests

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.gemini_api_key = settings.GEMINI_API_KEY
        self.gemini_model = settings.GEMINI_MODEL
        self.gemini_url = (
            f"https://generativelanguage.googleapis.com/v1/models/"
            f"{self.gemini_model}:generateContent?key={self.gemini_api_key}"
        )

        self.openrouter_api_key = settings.OPENROUTER_API_KEY
        self.openrouter_model = settings.OPENROUTER_MODEL
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

    def _build_system_prompt(self) -> str:
        return (
            "Ти AI-асистент інтернет-магазину колекційних фігурок Funko Pop. "
            "Відповідай лише по темі магазину: товари, доставка, оплата, "
            "передзамовлення, наявність, поради покупцю. "
            "Якщо питання не стосується магазину, ввічливо скажи, що можеш "
            "допомогти лише з питаннями магазину. "
            "Не вигадуй наявність товарів, якщо не маєш точних даних. "
            "Відповідай коротко, корисно і українською мовою."
        )

    def _smart_text_fallback(self) -> str:
        return (
            "Зараз AI-асистент тимчасово недоступний 😔\n\n"
            "Але я все ще можу допомогти з:\n"
            "• доставкою\n"
            "• оплатою\n"
            "• наявністю товарів\n"
            "• передзамовленням\n\n"
            "Оберіть категорію в меню вище або спробуйте ще раз трохи пізніше."
        )

    def _try_gemini(self, user_message: str) -> str | None:
        system_prompt = self._build_system_prompt()
        full_prompt = f"{system_prompt}\n\nКористувач: {user_message}"

        try:
            response = requests.post(
                self.gemini_url,
                json={
                    "contents": [
                        {
                            "parts": [{"text": full_prompt}]
                        }
                    ]
                },
                timeout=20,
            )

            print("GEMINI STATUS:", response.status_code)
            print("GEMINI BODY:", response.text)

            if response.status_code != 200:
                return None

            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return None

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                return None

            text = parts[0].get("text", "").strip()
            return text or None

        except requests.RequestException as e:
            print("GEMINI REQUEST ERROR:", e)
            return None
        except Exception as e:
            print("GEMINI UNKNOWN ERROR:", e)
            return None

    def _try_openrouter(self, user_message: str) -> str | None:
        if not self.openrouter_api_key:
            return None

        try:
            response = requests.post(
                self.openrouter_url,
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.openrouter_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": self._build_system_prompt(),
                        },
                        {
                            "role": "user",
                            "content": user_message,
                        },
                    ],
                },
                timeout=20,
            )

            print("OPENROUTER STATUS:", response.status_code)
            print("OPENROUTER BODY:", response.text)

            if response.status_code != 200:
                return None

            data = response.json()
            choices = data.get("choices", [])
            if not choices:
                return None

            message = choices[0].get("message", {})
            text = message.get("content", "")
            text = text.strip() if isinstance(text, str) else ""
            return text or None

        except requests.RequestException as e:
            print("OPENROUTER REQUEST ERROR:", e)
            return None
        except Exception as e:
            print("OPENROUTER UNKNOWN ERROR:", e)
            return None

    def generate_reply(self, user_message: str) -> tuple[str, str]:
        gemini_reply = self._try_gemini(user_message)
        if gemini_reply:
            return gemini_reply, "gemini"

        openrouter_reply = self._try_openrouter(user_message)
        if openrouter_reply:
            return openrouter_reply, "openrouter"

        return self._smart_text_fallback(), "fallback"