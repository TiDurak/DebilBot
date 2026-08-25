import asyncio
import aiohttp
from config import ai_settings


class ChatSession:
    def __init__(self, api_key: str, model: str):
        self.__model = model
        self.__messages = [
            ai_settings.get("ai_instructions")
        ]
        self.__headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://discord.com/",
            "X-Title": "Discord Bot"
        }
        self.__timeout = aiohttp.ClientTimeout(
            total=60,
            connect=10
        )

    async def send_message(self, text: str) -> str:
        self.__messages.append({
            "role": "user",
            "content": text
        })

        payload = {
            "model": self.__model,
            "messages": self.__messages
        }

        try:
            async with aiohttp.ClientSession(timeout=self.__timeout) as session:
                async with session.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=self.__headers,
                        json=payload
                ) as response:
                    data = await response.json()

                    if response.status != 200:
                        self.__messages.pop()

                        error = data.get("error", {})
                        raise Exception(
                            f"OpenRouter {response.status}: "
                            f"{error.get('message', data)}"
                        )

                    answer = data["choices"][0]["message"]["content"]

        except asyncio.TimeoutError:
            self.__messages.pop()
            raise Exception("OpenRouter не ответил за 60 секунд.")

        except aiohttp.ClientError as e:
            self.__messages.pop()
            raise Exception(f"Ошибка соединения с OpenRouter: {e}")

        except Exception:
            # Если ошибка произошла после добавления user-сообщения
            # и оно ещё осталось в истории — удаляем его.
            if self.__messages and self.__messages[-1].get("role") == "user":
                self.__messages.pop()

            raise

        self.__messages.append({
            "role": "assistant",
            "content": answer
        })

        return answer