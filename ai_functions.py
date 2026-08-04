"""AI функции для генерации - РАБОЧИЕ ВЕРСИИ"""
import os
import random
import requests
from PIL import Image
import io


def generate_pixel_city_image():
    """Генерирует изображение через Pollinations - ПРОСТО И НАДЁЖНО"""

    prompt = "pixel art cyberpunk city neon purple cyan"

    try:
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=1024&height=768&seed={random.randint(1, 999999)}"

        response = requests.get(url, timeout=60)

        if response.status_code == 200 and len(response.content) > 1000:
            img = Image.open(io.BytesIO(response.content))

            # Обрезаем до 4:3
            w, h = img.size
            if w/h > 1.5:  # Слишком широкое
                new_w = int(h * 4/3)
                img = img.crop(((w-new_w)//2, 0, (w+new_w)//2, h))

            temp_file = f"city_{random.randint(1000, 9999)}.png"
            img.save(temp_file, "PNG")
            return temp_file
    except:
        pass

    return None


def generate_ai_post(topic, style="long"):
    """Заглушка для генерации текста пока DeepSeek не настроен"""
    return f"Пост о {topic}\n\nОчень подробный текст на эту тему...\n\n#хештег"
