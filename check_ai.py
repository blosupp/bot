import os
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем .env переменные
load_dotenv()

# Проверяем ключ
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY не найден. Добавь его в .env или переменные окружения.")

# Инициализация OpenAI клиента
client = OpenAI(api_key=api_key)

# Путь к твоему проекту (можно изменить)
PROJECT_PATH = r"C:\Users\indje\Documents\GitHub\bot"

# Показать все .py, .txt, .md файлы
def list_files(path):
    print("\n📁 Файлы проекта:")
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".md", ".txt")):
                print(os.path.join(root, file))

# Прочитать файл
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return "❌ Ошибка: файл не в UTF-8"
    except Exception as e:
        return f"❌ Ошибка при чтении файла: {e}"

# Задать вопрос GPT
def ask_gpt(prompt, system_prompt="Ты опытный Python-разработчик. Отвечай по делу."):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Показать помощь
def show_help():
    print("""
📜 Команды:
  list                  — Показать все файлы проекта
  read <файл>           — Показать содержимое файла
  ask <вопрос>          — Вопрос GPT без файла
  context <файл>        — Прочитать файл и задать вопрос по его коду
  help                  — Показать эту справку
  exit / quit           — Выйти
""")

# Главный цикл
def main():
    print("🤖 GPT-помощник запущен. Напиши `help` для списка команд.")
    while True:
        user_input = input("> ").strip()

        if user_input == "help":
            show_help()

        elif user_input == "list":
            list_files(PROJECT_PATH)

        elif user_input.startswith("read "):
            _, filename = user_input.split(" ", 1)
            full_path = os.path.join(PROJECT_PATH, filename)
            content = read_file(full_path)
            print(f"\n📄 {filename}:\n{'-'*40}\n{content}\n{'-'*40}")

        elif user_input.startswith("ask "):
            _, question = user_input.split(" ", 1)
            print("💬 GPT думает...")
            answer = ask_gpt(question)
            print(f"\n🤖 Ответ:\n{answer}")

        elif user_input.startswith("context "):
            _, filename = user_input.split(" ", 1)
            full_path = os.path.join(PROJECT_PATH, filename)
            file_content = read_file(full_path)
            print(f"\n📄 Прочитал файл {filename}. Теперь задай вопрос:")
            follow_up = input(">> ").strip()
            combined_prompt = f"Вот код:\n\n{file_content}\n\nВопрос: {follow_up}"
            print("💬 GPT анализирует...")
            answer = ask_gpt(combined_prompt)
            print(f"\n🤖 Ответ:\n{answer}")

        elif user_input in ["exit", "quit"]:
            print("👋 Пока, босс.")
            break

        else:
            print("⚠️ Неизвестная команда. Напиши `help`, чтобы увидеть список.")

if __name__ == "__main__":
    main()
