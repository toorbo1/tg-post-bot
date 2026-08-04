import os
import random
import requests


def generate_pixel_city_image():
    """Генерирует изображение - РАБОЧАЯ ВЕРСИЯ"""

    try:
        prompt = "pixel art cyberpunk city neon purple cyan"
        encoded = requests.utils.quote(prompt)
        seed = random.randint(1, 999999)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=768&seed={seed}&nologo=true"
        print(f"Generating...")
        response = requests.get(url, timeout=120)
        print(f"Response: {response.status_code}, {len(response.content)} bytes")

        if response.status_code == 200 and len(response.content) > 5000:
            filename = f"city_{random.randint(1000, 9999)}.png"
            filepath = os.path.join(os.path.dirname(__file__), filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"SUCCESS: {filepath}")
            return filepath
        else:
            print(f"FAILED: status {response.status_code}, content too small")
            return None

    except Exception as e:
        print(f"ERROR: {e}")
        return None


if __name__ == "__main__":
    result = generate_pixel_city_image()
    print(f"Test result: {result}")
