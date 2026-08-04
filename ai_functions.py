import os
import random
import requests


def generate_pixel_city_image():
    """Генерирует изображение через Pollinations"""

    try:
        url = "https://image.pollinations.ai/prompt/pixel%20art%20city?width=512&height=512"

        response = requests.get(url, timeout=60)
        print(f"Status: {response.status_code}, Size: {len(response.content)} bytes")

        if response.status_code == 200 and len(response.content) > 1000:
            filename = f"city_{random.randint(1000, 9999)}.png"
            filepath = os.path.join(os.path.dirname(__file__), filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"SUCCESS: {filepath}")
            return filepath

    except Exception as e:
        print(f"Error: {e}")

    return None


if __name__ == "__main__":
    result = generate_pixel_city_image()
    print(f"Test result: {result}")
