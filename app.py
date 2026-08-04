"""Локальное приложение для генерации постов с DeepSeek и Шедеврум"""
import os
import sys
import json
import random
import threading
import datetime
import time
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

DEEPSEEK_SESSION_ID = os.environ.get("DEEPSEEK_SESSION_ID", "")
SHEDEVRUM_API_KEY = os.environ.get("SHEDEVRUM_API_KEY", "")

# Импортируем AI функции
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ai_functions import generate_ai_post, generate_pixel_city_image


def save_config():
    """Сохраняет конфигурацию"""
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_config.json")
    config = {
        "last_generated": datetime.datetime.now().isoformat(),
        "deepseek_key_set": bool(DEEPSEEK_SESSION_ID),
        "shedevrum_key_set": bool(SHEDEVRUM_API_KEY)
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def generate_post():
    """Генерирует пост: текст + изображение"""
    topics = [
        "кибербезопасность", "искусственный интеллект", "приватность в сети",
        "обход блокировок", "пиксельная эстетика", "анонимность",
        "big data", "облачные технологии", "интернет вещей",
        "будущее технологий", "VPN и прокси", "шифрование данных"
    ]

    topic = random.choice(topics)
    print(f"\n🎯 Тема поста: {topic}")

    # Генерация текста
    print("⏳ Генерирую текст через DeepSeek...")
    if not DEEPSEEK_SESSION_ID:
        print("❌ DEEPSEEK_SESSION_ID не настроен!")
        text = None
    else:
        text = generate_ai_post(topic, "long")
        if text:
            print(f"✅ Текст готов: {len(text)} символов")
        else:
            print("❌ DeepSeek не смог сгенерировать текст")

    # Генерация изображения
    print("⏳ Генерирую пиксельный город через Шедеврум...")
    if not SHEDEVRUM_API_KEY:
        print("❌ SHEDEVRUM_API_KEY не настроен!")
        image = None
    else:
        image = generate_pixel_city_image()
        if image:
            print(f"✅ Изображение готово: {image}")
        else:
            print("❌ Шедеврум не смог сгенерировать изображение")

    # Сохраняем результат
    result = {
        "timestamp": datetime.datetime.now().isoformat(),
        "topic": topic,
        "text": text,
        "image": image,
        "success": bool(text or image)
    }

    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_posts")
    os.makedirs(results_dir, exist_ok=True)
    filename = f"post_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(results_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Результат сохранён: {filepath}")
    return result


def show_status():
    """Показывает статус системы"""
    print("\n" + "="*60)
    print("📊 СТАТУС СИСТЕМЫ")
    print("="*60)

    print(f"\n🔑 API Ключи:")
    print(f"  DeepSeek: {'✅ Настроен' if DEEPSEEK_SESSION_ID else '❌ Не настроен'}")
    print(f"  Шедеврум: {'✅ Настроен' if SHEDEVRUM_API_KEY else '❌ Не настроен'}")

    # Проверяем сгенерированные посты
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_posts")
    if os.path.exists(results_dir):
        posts = [f for f in os.listdir(results_dir) if f.endswith(".json")]
        print(f"\n📝 Сгенерированные посты: {len(posts)}")
        if posts:
            latest = sorted(posts)[-1]
            with open(os.path.join(results_dir, latest), "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"  Последний: {data.get('timestamp', 'неизвестно')}")
            print(f"  Тема: {data.get('topic', 'неизвестно')}")
            print(f"  Текст: {'✅' if data.get('text') else '❌'}")
            print(f"  Картинка: {'✅' if data.get('image') else '❌'}")
    else:
        print(f"\n📝 Сгенерированных постов: 0")

    print("="*60)


def main_menu():
    """Главное меню приложения"""
    while True:
        print("\n" + "="*60)
        print("🚀 ГЕНЕРАТОР ПОСТОВ С DEEPSEEK И ШЕДЕВРУМ")
        print("="*60)
        print("1. Сгенерировать новый пост")
        print("2. Показать статус")
        print("3. Выйти")
        print("="*60)

        choice = input("\nВыбери действие (1-3): ").strip()

        if choice == "1":
            result = generate_post()
            if result["success"]:
                print("\n🎉 Пост успешно сгенерирован!")
                if result.get("text"):
                    print(f"\n📄 Текст ({len(result['text'])} символов):")
                    print("-" * 60)
                    print(result["text"][:500] + "..." if len(result["text"]) > 500 else result["text"])
            else:
                print("\n❌ Генерация не удалась. Проверь API ключи!")

        elif choice == "2":
            show_status()

        elif choice == "3":
            print("\n👋 Пока!")
            break

        else:
            print("\n❌ Неверный выбор!")


if __name__ == "__main__":
    print("Запускаю приложение...")
    main_menu()
