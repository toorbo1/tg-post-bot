"""AI функции для генерации постов и изображений"""
import os
import random
import requests
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

DEEPSEEK_SESSION_ID = os.environ.get("DEEPSEEK_SESSION_ID", "")
SHEDEVRUM_API_KEY = os.environ.get("SHEDEVRUM_API_KEY", "")


def generate_ai_post(topic, style="long"):
    """Генерирует БОЛЬШОЙ и МАСШТАБНЫЙ пост через DeepSeek от лица Каролины"""

    if not DEEPSEEK_SESSION_ID:
        logger.error("❌ DEEPSEEK_SESSION_ID not set! Cannot generate post.")
        return None

    prompts = [
        f"Напиши ОЧЕНЬ ПОДРОБНЫЙ и МАСШТАБНЫЙ пост про '{topic}' от лица пиксельной девочки Каролины. Минимум 10-12 абзацев. Используй HTML теги <b> для выделения. Добавь много списков с эмодзи (✅, 💡, 📌, 🎮). В конце 3-4 хештега. Добавь личный опыт, истории из пиксельного мира, глубокий анализ темы.",
        f"Расскажи ПРО '{topic}' максимально подробно и масштабно от лица Каролины. Минимум 10 абзацев. Выдели важное через <b>. Добавь личный опыт, практические советы, примеры. Используй эмодзи-списки. Заверши 3-4 хештегами. Пост должен быть ОЧЕНЬ большим и информативным!",
        f"Масштабный пост о '{topic}' от пиксельной девочки. Минимум 8-10 абзацев. Будь максимально конкретной, добавь примеры из жизни, личный опыт, глубокий анализ. Используй <b>теги</b>, эмодзи-списки, подзаголовки. Заверши хештегами."
    ]

    prompt = random.choice(prompts)

    # Генерация через DeepSeek API (реальное подключение)
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_SESSION_ID}",
            "Content-Type": "application/json"
        }

        system_instruction = """Ты — Каролина, пиксельная 2D-девочка из цифрового мира! Ты пишешь ОЧЕНЬ ПОДРОБНЫЕ и МАСШТАБНЫЕ посты для Telegram-канала.

ТВОЙ СТИЛЬ:
- Живой, неформальный язык с эмоциями
- ОЧЕНЬ ПОДРОБНО — минимум 10-12 абзацев
- Короткие абзацы (2-4 предложения)
- Личное мнение, истории из пиксельного мира
- Без шаблонных фраз типа 'в современном мире'
- Пиши так, как будто рассказываешь лучшей подруге

ФОРМАТИРОВАНИЕ:
- Используй HTML теги <b> для выделения ВАЖНЫХ моментов
- Добавляй списки с эмодзи (✅, 💡, 📌, 🎮, 💜)
- Делай подзаголовки через <b>
- В конце добавь 3-4 хештега по теме

ВАЖНО:
- Пост должен быть БОЛЬШИМ и МАСШТАБНЫМ
- Минимум 10-12 абзацев подробного текста
- Добавляй личные истории из пиксельного мира
- Глубокий анализ темы с примерами
- Каждый пост уникален и отличается от других"""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 4096,
            "top_p": 0.95,
            "stream": False
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            text = text.strip()
            if len(text) > 200:
                logger.info(f"✅ DeepSeek generated BIG post: {len(text)} chars")
                return text
            else:
                logger.warning(f"DeepSeek returned short text: {len(text)} chars")
                return None
        else:
            logger.error(f"❌ DeepSeek API error: {response.status_code} - {response.text[:300]}")
            return None
    except Exception as e:
        logger.error(f"❌ DeepSeek generation failed: {e}")
        return None


def generate_pixel_city_image():
    """Генерирует ПИКСЕЛЬНЫЙ ГОРОД через Pollinations.ai в высоком качестве 4:3"""

    # Промпт для пиксельного города
    style_prompt = "pixel art cyberpunk city, neon purple and cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio, high quality, crisp edges, ultra detailed"

    try:
        # Используем Pollinations.ai (работает без ключа)
        encoded_prompt = requests.utils.quote(style_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&seed={random.randint(1, 999999)}&nologo=true&model=turbo"

        logger.info(f"Generating pixel city via Pollinations...")

        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            from PIL import Image
            import io

            img = Image.open(io.BytesIO(response.content))
            width, height = img.size
            logger.info(f"Generated image: {width}x{height}")

            # Проверяем соотношение сторон и обрезаем до 4:3
            target_ratio = 4/3
            current_ratio = width / height

            if abs(current_ratio - target_ratio) > 0.1:
                logger.info(f"Cropping from {current_ratio:.2f} to 4:3")
                if current_ratio > target_ratio:
                    new_width = int(height * target_ratio)
                    left = (width - new_width) // 2
                    img = img.crop((left, 0, left + new_width, height))
                else:
                    new_height = int(width / target_ratio)
                    top = (height - new_height) // 2
                    img = img.crop((0, top, width, top + new_height))

                buffer = io.BytesIO()
                img.save(buffer, format='PNG', quality=95)
                temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"pixel_city_{random.randint(1, 999999)}.png")
                with open(temp_file, 'wb') as f:
                    f.write(buffer.getvalue())
                logger.info(f"Cropped to: {img.size[0]}x{img.size[1]} (4:3)")
                return temp_file
            else:
                temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"pixel_city_{random.randint(1, 999999)}.png")
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Saved pixel city: {width}x{height}")
                return temp_file
        else:
            logger.error(f"Pollinations error: {response.status_code}")
    except Exception as e:
        logger.error(f"SheDevrum generation failed: {e}")

    return None
