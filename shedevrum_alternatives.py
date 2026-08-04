"""Альтернативы Шедеврума - бесплатные API для генерации изображений"""
import os
import random
import requests
from PIL import Image
import io


def generate_pixel_city_huggingface():
    """Генерирует через HuggingFace Kandinsky (бесплатно, без ключа)"""

    style_prompt = "pixel art cyberpunk city, neon purple cyan, detailed buildings, 16-bit retro, sharp pixels, 4:3 aspect ratio"

    try:
        # HuggingFace Inference API
        url = "https://api-inference.huggingface.co/models/kandinsky-community/kandinsky-2-2-prior"

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={"inputs": style_prompt, "width": 1024, "height": 768},
            timeout=120
        )

        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            temp_file = f"kandinsky_{random.randint(1, 999999)}.png"
            img.save(temp_file, format='PNG')
            return temp_file
        else:
            print(f"HuggingFace error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
