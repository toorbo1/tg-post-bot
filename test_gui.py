import sys
sys.path.insert(0, '.')

from ai_functions import generate_pixel_city_image

print("Testing image generation...")
result = generate_pixel_city_image()

if result:
    print(f"SUCCESS: {result}")
else:
    print("FAILED: No image generated")
