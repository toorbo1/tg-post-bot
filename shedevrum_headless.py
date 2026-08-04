"""Шедеврум в фоновом режиме (headless Chrome)"""
import os
import random
import time
import requests
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)


def generate_pixel_city_shedevrum_headless():
    """Генерирует ПИКСЕЛЬНЫЙ ГОРОД через Шедеврум в headless режиме"""

    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Промпт для пиксельного города
        style_prompt = "pixel art cyberpunk city, neon purple and cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio"

        logger.info("🎨 Opening SheDevrum in headless mode...")

        # Запускаем Chrome в headless режиме
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Новый headless режим
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")  # Скрываем автоматизацию
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)

        try:
            # Открываем Шедеврум
            logger.info("Loading SheDevrum page...")
            driver.get("https://shedevrum.ai/")

            # Ждём загрузки
            time.sleep(5)

            # Проверяем нет ли редиректа на авторизацию
            current_url = driver.current_url
            if "passport.yandex" in current_url or "auth" in current_url:
                logger.error("SheDevrum requires Yandex auth - redirect detected")
                raise Exception("Требуется авторизация Яндекса")

            # Ищем поле ввода
            logger.info("Searching for input field...")

            input_box = None
            selectors = [
                "textarea",
                "input[type='text']",
                "[contenteditable='true']",
                ".TextInput textarea",
                "#prompt-input"
            ]

            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        if elem.is_displayed():
                            input_box = elem
                            logger.info(f"Found input: {selector}")
                            break
                    if input_box:
                        break
                except:
                    continue

            if not input_box:
                raise Exception("Не удалось найти поле ввода")

            # Вводим промпт
            logger.info("Entering prompt...")
            input_box.click()
            time.sleep(0.5)

            # Вводим текст посимвольно
            for char in style_prompt:
                try:
                    input_box.send_keys(char)
                except:
                    break
                time.sleep(0.01)

            logger.info("Prompt entered")
            time.sleep(1)

            # Ищем и кликаем кнопку генерации
            logger.info("Finding generate button...")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            generate_btn = None

            for btn in buttons:
                if btn.is_displayed():
                    text = btn.text.lower()
                    if any(word in text for word in ["сгенерировать", "generate", "создать"]):
                        generate_btn = btn
                        break

            if generate_btn:
                generate_btn.click()
                logger.info("Clicked generate button")
            else:
                from selenium.webdriver.common.keys import Keys
                input_box.send_keys(Keys.RETURN)
                logger.info("Pressed Enter")

            # Ждём результат (до 3 минут)
            logger.info("Waiting for generation (up to 3 minutes)...")

            result_img = None
            wait = WebDriverWait(driver, 180)

            img_selectors = [
                "img.generated",
                "img.result",
                ".image-container img",
                ".Result img",
                "[class*='result'] img"
            ]

            for selector in img_selectors:
                try:
                    result_img = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    logger.info(f"Found image with: {selector}")
                    break
                except:
                    continue

            if not result_img:
                raise Exception("Generation timed out after 3 minutes")

            # Получаем URL изображения
            img_src = result_img.get_attribute("src") or result_img.get_attribute("data-src")

            if not img_src:
                raise Exception("No image source found")

            # Скачиваем изображение
            logger.info(f"Downloading from: {img_src[:100]}...")
            img_response = requests.get(img_src, timeout=60)

            if img_response.status_code == 200:
                img = Image.open(io.BytesIO(img_response.content))
                width, height = img.size
                logger.info(f"✅ SheDevrum generated: {width}x{height}")

                # Обрезаем до 4:3
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
                temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"shedevrum_{random.randint(1, 999999)}.png")
                with open(temp_file, 'wb') as f:
                    f.write(buffer.getvalue())

                logger.info(f"Saved to: {temp_file}")
                return temp_file
            else:
                raise Exception(f"Failed to download: {img_response.status_code}")

        finally:
            driver.quit()

    except ImportError:
        logger.error("Selenium not installed. Install with: pip install selenium")
        return None
    except Exception as e:
        logger.error(f"SheDevrum headless failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


if __name__ == "__main__":
    result = generate_pixel_city_shedevrum_headless()
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED")
