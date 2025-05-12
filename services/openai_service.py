import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(
    prompt: str,
    system_prompt: str = "Ты — дружелюбный ассистент в Telegram, общаешься как человек. Отвечай просто, по-доброму, с юмором. Если пользователь просит пост — пиши чётко, кратко и без воды.",
    memory: list = None
) -> str:
    """
    Отправляет запрос в OpenAI GPT и возвращает ответ.
    Если что-то пойдёт не так — возвращает текст ошибки.
    """
    messages = [{"role": "system", "content": system_prompt}]

    if memory:
        messages.extend(memory)

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[GPT ERROR]", e)
        return "❌ Что-то пошло не так... Я пока молчу. Попробуй позже, ок?)"
