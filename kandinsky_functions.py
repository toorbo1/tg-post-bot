"""Генерация изображений через Kandinsky API (бесплатный аналог Шедеврума)"""
import os
import random
import time
import requests
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)


def generate_pixel_city_kandinsky():
    """Генерирует ПИКСЕЛЬНЫЙ ГОРОД через Kandinsky API (бесплатно, без ключа!)"""

    try:
        # Промпт для пиксельного города
        style_prompt = "pixel art cyberpunk city, neon purple and cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio, ultra detailed"

        logger.info(f"🎨 Generating via Kandinsky API (free, no key needed)...")

        # Kandinsky API endpoint
        url = "https://kandinsky2.dair.tech/api/v2/generate"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "type": "TEXT_TO_IMAGE",
            "params": {
                "model_version": "4.2",
                "seed": random.randint(1, 999999),
                "width": 1024,
                "height": 768,
                "num_images": 1,
                "style": "pixel art"
            },
            "messages": [
                {"role": "user", "text": style_prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=180)

        if response.status_code == 200:
            data = response.json()

            # Получаем URL изображения
            if "result" in data and "images" in data["result"]:
                img_url = data["result"]["images"][0]

                logger.info(f"Downloading image from Kandinsky...")
                img_response = requests.get(img_url, timeout=60)

                if img_response.status_code == 200:
                    img = Image.open(io.BytesIO(img_response.content))
                    width, height = img.size
                    logger.info(f"✅ Kandinsky generated: {width}x{height}")

                    # Обрезаем до 4:3 если нужно
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
                    temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"kandinsky_{random.randint(1, 999999)}.png")
                    with open(temp_file, 'wb') as f:
                        f.write(buffer.getvalue())

                    logger.info(f"Saved to: {temp_file}")
                    return temp_file
                else:
                    logger.error(f"Failed to download image: {img_response.status_code}")
            else:
                logger.error(f"No image in response: {data}")
        else:
            logger.error(f"Kandinsky API error: {response.status_code} - {response.text[:300]}")

    except Exception as e:
        logger.error(f"Kandinsky generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())

    return None


if __name__ == "__main__":
    result = generate_pixel_city_kandinsky()
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED")
