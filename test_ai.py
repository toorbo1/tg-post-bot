#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_functions import generate_ai_post, generate_pixel_city_image

print("Testing DeepSeek...")
result = generate_ai_post("кибербезопасность", "long")
if result:
    print(f"DeepSeek OK: {len(result)} chars")
    print(f"First 200 chars: {result[:200]}")
else:
    print("DeepSeek FAILED")

print("\nTesting SheDevrum...")
img = generate_pixel_city_image()
if img:
    print(f"SheDevrum OK: {img}")
else:
    print("SheDevrum FAILED")
