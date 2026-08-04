"""Генерация изображений через веб-интерфейс Шедеврум"""
import os
import time
import random
import requests
from pathlib import Path


def generate_pixel_city_via_web(prompt=None):
    """Генерирует пиксельный город через веб Шедеврума используя API без ключа"""

    if prompt is None:
        prompt = "pixel art cyberpunk city, neon purple cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio"

    # Используем публичный endpoint Шедеврума без авторизации
    url = "https://shedevrum.yandex.ru/api/generation"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 768,
        "model": "yandex-art",
        "seed": random.randint(1, 999999)
    }

    try:
        print(f"Generating image via SheDevrum web...")
        response = requests.post(url, headers=headers, json=payload, timeout=120)

        if response.status_code == 200:
            data = response.json()
            # Получаем URL изображения
            image_url = data.get("result", {}).get("image") or data.get("result", {}).get("imageUrl")

            if image_url:
                print(f"Image URL: {image_url}")
                # Скачиваем изображение
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    from PIL import Image
                    import io

                    img = Image.open(io.BytesIO(img_response.content))
                    width, height = img.size
                    print(f"Generated image: {width}x{height}")

                    # Обрезаем до 4:3 если нужно
                    target_ratio = 4/3
                    current_ratio = width / height

                    if abs(current_ratio - target_ratio) > 0.1:
                        print(f"Cropping from {current_ratio:.2f} to 4:3")
                        if current_ratio > target_ratio:
                            new_width = int(height * target_ratio)
                            left = (width - new_width) // 2
                            img = img.crop((left, 0, left + new_width, height))
                        else:
                            new_height = int(width / target_ratio)
                            top = (height - new_height) // 2
                            img = img.crop((0, top, width, top + new_height))

                    # Сохраняем
                    output_dir = Path(__file__).parent / "generated_images"
                    output_dir.mkdir(exist_ok=True)
                    temp_file = str(output_dir / f"shedevrum_{random.randint(1000, 9999)}.png")

                    img.save(temp_file, "PNG", quality=95)
                    print(f"Saved to: {temp_file}")
                    return temp_file
            else:
                print("No image URL in response")
        else:
            print(f"API error: {response.status_code}")
            print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

    return None


if __name__ == "__main__":
    result = generate_pixel_city_via_web()
    if result:
        print(f"Success! Image saved: {result}")
    else:
        print("Failed to generate image")
