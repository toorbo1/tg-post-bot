# Локальное приложение для генерации постов

## Описание
Приложение `app.py` — локальная версия бота с той же логикой:
- **DeepSeek** для генерации больших текстов (10-12 абзацев)
- **Шедеврум** для создания пиксельных городов в формате 4:3

## Установка

### 1. Получи API ключи:

**DeepSeek:**
1. Иди на https://platform.deepseek.com/api_keys
2. Создай аккаунт (если нет)
3. Сгенерируй API key
4. Скопируй ключ

**Шедеврум:**
1. Иди на https://shedevrum.yandex.ru/api
2. Авторизуйся через Яндекс
3. Получи API key
4. Скопируй ключ

### 2. Настрой .env файл:

Открой `.env` в корне проекта и вставь реальные ключи:

```env
DEEPSEEK_SESSION_ID=реальный_ключ_от_deepseek
SHEDEVRUM_API_KEY=реальный_ключ_от_шедеврум
```

### 3. Установи зависимости:

```bash
cd C:\Users\User\Desktop\tg-post-bot
pip install Pillow requests python-dotenv
```

## Использование

### Генерация поста:
```bash
python app.py generate
```

### Проверка статуса:
```bash
python app.py status
```

## Результат

Посты сохраняются в папку `generated_posts/` в формате JSON:
- `timestamp` — время создания
- `topic` — тема поста
- `text` — сгенерированный текст
- `image` — путь к изображению
- `success` — успешность генерации

## Структура

- `app.py` — главное приложение
- `ai_functions.py` — AI функции (DeepSeek + SheDevrum)
- `bot.py` — Telegram бот (использует те же AI функции)
- `generated_posts/` — результаты генерации

## Важно!

Без реальных API ключей ничего не работает! Ключи из примера (`sk_NzCmH2Q9AZ5BYtfDuXA8QQWt9aiN3EDA`) — невалидные.
