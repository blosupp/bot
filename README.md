# 🤖 Telegram AI Бот (на GPT-4o)

Этот бот предназначен для генерации постов с помощью GPT-4o и автоматической публикации их в Telegram-каналы пользователей. Имеет гибкую систему ролей (superadmin → admin → user) и управление через интерфейс Telegram.

---

## 🚀 Возможности

- ✍️ Генерация постов (текст / изображение + подпись)
- 📢 Автопубликация в каналы, привязанные к пользователю
- ⚙️ Интерактивная админ-панель через /доступ
- 🔐 Ролевой доступ (`user`, `admin`, `superadmin`)
- 🧠 Настройки памяти GPT (remember, history_limit)
- 🧩 Работа с базой SQLite (`access.db`, `dialogues.db`)
- 🌐 Используется OpenAI GPT-4o через API

---

## ⚙️ Установка

```bash
git clone https://github.com/your_username/your_repo.git
cd your_repo
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

---

## 📦 Переменные окружения (.env)

Создайте файл `.env` в корне проекта:

```
BOT_TOKEN=xxx:yyy
OPENAI_API_KEY=sk-...
CHANNEL_ID=-1001234567890
ADMIN_ID=123456789
```

> 📌 Хотя `CHANNEL_ID` и `ADMIN_ID` указаны, всё управление делается через базу данных (`access.db`).

---

## 🧠 GPT-модель

Используется модель `gpt-4o` через [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create).

---

## 🗂 Структура проекта

```
bot/
├── handlers/
│   ├── start.py
│   ├── help.py
│   ├── text.py
│   ├── photo.py
│   └── admin_panel.py
├── middleware/
│   └── access_control.py
├── services/
│   └── openai_service.py
├── db.py
├── access.py
├── config.py
├── main.py
```

---

## 🔐 Роли

| Роль         | Возможности                                |
|--------------|---------------------------------------------|
| `superadmin` | управляет пользователями и их каналами      |
| `admin`      | может генерировать и публиковать посты      |
| `user`       | (ограничено, можно отключить генерацию)     |

Все роли и каналы хранятся в базе `access.db`.

---

## 💬 Команды

| Команда       | Доступ        | Описание                                      |
|---------------|---------------|-----------------------------------------------|
| `/start`      | все           | Запуск бота                                   |
| `/help`       | все           | Все команды с учётом роли                     |
| `/myid`       | все           | Узнать свой Telegram ID                       |
| `/доступ`     | admin+        | Интерактивная панель                          |
| `/add_admin`  | superadmin    | Назначить админа                              |
| `/list_users` | superadmin    | Просмотреть всех пользователей и роли         |

---

## 📤 Публикация постов

- Напиши текст — будет сгенерирован и отправлен в канал
- Отправь фото с подписью — подпись будет дополнена и отправлена

---

## 💾 Хранилище

- `access.db` — пользователи, роли, каналы
- `dialogues.db` — история общения с GPT

---

## 🧪 Запуск

```bash
python main.py
```

---

## 🧑‍💻 Автор

Проект тестируется вручную и может быть расширен по задачам.