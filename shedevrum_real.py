"""Реальная генерация через Шедеврум без авторизации"""
import os
import random
import time
import requests
from PIL import Image
import io


def generate_via_shedevrum_web(prompt, width=1024, height=768):
    """Генерирует изображение через веб Шедеврума имитируя браузер"""

    # Промпт для пиксельного города
    if not prompt:
        prompt = "pixel art cyberpunk city, neon purple and cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio"

    print(f"Generating via SheDevrum web (no auth)...")

    # Шаг 1: Создаём задачу на генерацию
    session_url = "https://art.yandex.ru/api/session"
    generate_url = "https://art.yandex.ru/api/generate"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://art.yandex.ru",
        "Referer": "https://art.yandex.ru/"
    }

    session_data = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": "yandex-art"
    }

    try:
        # Создаём сессию
        print("Creating session...")
        session_resp = requests.post(session_url, headers=headers, json=session_data, timeout=30)

        if session_resp.status_code != 200:
            print(f"Session error: {session_resp.status_code}")
            return None

        session_id = session_resp.json().get("session_id")
        print(f"Session created: {session_id}")

        # Запускаем генерацию
        print("Starting generation...")
        generate_data = {
            "session_id": session_id,
            "prompt": prompt
        }

        gen_resp = requests.post(generate_url, headers=headers, json=generate_data, timeout=180)

        if gen_resp.status_code != 200:
            print(f"Generate error: {gen_resp.status_code}")
            return None

        task_id = gen_resp.json().get("task_id")
        print(f"Task ID: {task_id}")

        # Ждём завершения (polling каждые 5 секунд)
        print("Waiting for generation (up to 2 minutes)...")
        status_url = f"https://art.yandex.ru/api/status/{task_id}"

        for attempt in range(24):  # 2 минуты с интервалом 5 сек
            time.sleep(5)

            status_resp = requests.get(status_url, headers=headers, timeout=30)

            if status_resp.status_code == 200:
                status_data = status_resp.json()
                status = status_data.get("status")

                if status == "completed":
                    image_url = status_data.get("image_url")
                    print(f"✅ Generation complete! URL: {image_url[:80]}...")

                    # Скачиваем изображение
                    img_resp = requests.get(image_url, timeout=60)
                    if img_resp.status_code == 200:
                        img = Image.open(io.BytesIO(img_resp.content))
                        temp_file = f"shedevrum_{random.randint(1, 999999)}.png"
                        img.save(temp_file, format='PNG', quality=95)
                        print(f"Saved to: {temp_file}")
                        return temp_file
                    else:
                        print(f"Download error: {img_resp.status_code}")
                        return None

                elif status == "failed":
                    print(f"Generation failed: {status_data.get('error')}")
                    return None
                else:
                    print(f"Status: {status}...")

        print("Timeout after 2 minutes")
        return None

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = generate_via_shedevrum_web(None)
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED")
