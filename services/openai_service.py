# services/openai_service.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(
    prompt: str,
    system_prompt: str = "Ты копирайтер для Telegram-канала. Пиши готовые посты. Без объяснений, без кода, без воды. Обязательное требование: текст не должен превышать 1024 символа.",
    memory: list = None
) -> str:
    """
    Отправляет запрос в OpenAI ChatGPT и возвращает текст.
    """
    messages = [{"role": "system", "content": system_prompt}]

    if memory:
        messages.extend(memory)

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content.strip()