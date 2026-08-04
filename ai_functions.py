"""AI функции для генерации постов и изображений"""
import os
import random
import time
import requests
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

DEEPSEEK_SESSION_ID = os.environ.get("DEEPSEEK_SESSION_ID", "")
SHEDEVRUM_API_KEY = os.environ.get("SHEDEVRUM_API_KEY", "")


def generate_ai_post(topic, style="long"):
    """Генерирует БОЛЬШОЙ и МАСШТАБНЫЙ пост через DeepSeek от лица Каролины"""

    if not DEEPSEEK_SESSION_ID:
        logger.error("❌ DEEPSEEK_SESSION_ID not set! Cannot generate post.")
        return None

    prompts = [
        f"Напиши ОЧЕНЬ ПОДРОБНЫЙ и МАСШТАБНЫЙ пост про '{topic}' от лица пиксельной девочки Каролины. Минимум 10-12 абзацев. Используй HTML теги <b> для выделения. Добавь много списков с эмодзи (✅, 💡, 📌, 🎮). В конце 3-4 хештега. Добавь личный опыт, истории из пиксельного мира, глубокий анализ темы.",
        f"Расскажи ПРО '{topic}' максимально подробно и масштабно от лица Каролины. Минимум 10 абзацев. Выдели важное через <b>. Добавь личный опыт, практические советы, примеры. Используй эмодзи-списки. Заверши 3-4 хештегами. Пост должен быть ОЧЕНЬ большим и информативным!",
        f"Масштабный пост о '{topic}' от пиксельной девочки. Минимум 8-10 абзацев. Будь максимально конкретной, добавь примеры из жизни, личный опыт, глубокий анализ. Используй <b>теги</b>, эмодзи-списки, подзаголовки. Заверши хештегами."
    ]

    prompt = random.choice(prompts)

    # Генерация через DeepSeek API (реальное подключение)
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_SESSION_ID}",
            "Content-Type": "application/json"
        }

        system_instruction = """Ты — Каролина, пиксельная 2D-девочка из цифрового мира! Ты пишешь ОЧЕНЬ ПОДРОБНЫЕ и МАСШТАБНЫЕ посты для Telegram-канала.

ТВОЙ СТИЛЬ:
- Живой, неформальный язык с эмоциями
- ОЧЕНЬ ПОДРОБНО — минимум 10-12 абзацев
- Короткие абзацы (2-4 предложения)
- Личное мнение, истории из пиксельного мира
- Без шаблонных фраз типа 'в современном мире'
- Пиши так, как будто рассказываешь лучшей подруге

ФОРМАТИРОВАНИЕ:
- Используй HTML теги <b> для выделения ВАЖНЫХ моментов
- Добавляй списки с эмодзи (✅, 💡, 📌, 🎮, 💜)
- Делай подзаголовки через <b>
- В конце добавь 3-4 хештега по теме

ВАЖНО:
- Пост должен быть БОЛЬШИМ и МАСШТАБНЫМ
- Минимум 10-12 абзацев подробного текста
- Добавляй личные истории из пиксельного мира
- Глубокий анализ темы с примерами
- Каждый пост уникален и отличается от других"""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 4096,
            "top_p": 0.95,
            "stream": False
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            text = text.strip()
            if len(text) > 200:
                logger.info(f"✅ DeepSeek generated BIG post: {len(text)} chars")
                return text
            else:
                logger.warning(f"DeepSeek returned short text: {len(text)} chars")
                return None
        else:
            logger.error(f"❌ DeepSeek API error: {response.status_code} - {response.text[:300]}")
            return None
    except Exception as e:
        logger.error(f"❌ DeepSeek generation failed: {e}")
        return None


def generate_pixel_city_image():
    """Генерирует ПИКСЕЛЬНЫЙ ГОРОД через веб Шедеврума с Selenium"""

    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import io
        from PIL import Image

        # Промпт для пиксельного города
        style_prompt = "pixel art cyberpunk city, neon purple and cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio"

        logger.info(f"🎨 Opening SheDevrum web...")

        # Запускаем браузер
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)

        try:
            # Открываем Шедеврум
            driver.get("https://shedevrum.yandex.ru/")
            logger.info("Page loaded")

            # Ждём загрузки страницы (5 секунд)
            time.sleep(5)

            # Ищем все textarea и input элементы
            logger.info("Searching for input field...")

            # Пробуем разные селекторы
            selectors = [
                "textarea",
                "input[type='text']",
                "[contenteditable='true']",
                ".prompt-input",
                "#prompt-input",
                "div[role='textbox']"
            ]

            input_box = None
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        input_box = elements[0]
                        logger.info(f"Found input with selector: {selector}")
                        break
                except:
                    continue

            if not input_box:
                # Если не нашли по селектору, ищем первый кликабельный элемент
                all_elements = driver.find_elements(By.TAG_NAME, "*")
                for elem in all_elements:
                    try:
                        if elem.is_displayed() and elem.tag_name in ['input', 'textarea', 'div']:
                            input_box = elem
                            logger.info("Found clickable element by tag")
                            break
                    except:
                        continue

            if not input_box:
                raise Exception("Could not find input field on page")

            # Кликаем на поле ввода и вводим промпт
            input_box.click()
            time.sleep(1)

            # Вводим текст посимвольно (как человек)
            for char in style_prompt:
                input_box.send_keys(char)
                time.sleep(0.01)

            logger.info("Prompt entered successfully")
            time.sleep(1)

            # Ищем и кликаем кнопку генерации
            buttons = driver.find_elements(By.TAG_NAME, "button")
            generate_btn = None

            for btn in buttons:
                if btn.is_displayed():
                    text = btn.text.lower()
                    if any(word in text for word in ["сгенерировать", "generate", "создать", "create", "go"]):
                        generate_btn = btn
                        break

            if not generate_btn:
                # Если не нашли кнопку по тексту, ищем по типичным классам
                try:
                    generate_btn = driver.find_element(By.CSS_SELECTOR, "button[class*='submit'], button[class*='send'], .action-button")
                except:
                    # Последняя надежда - Enter в поле ввода
                    logger.info("No button found, pressing Enter in input")
                    input_box.send_keys(Keys.RETURN)
                    generate_btn = True  # Фейковая кнопка

            if generate_btn and isinstance(generate_btn, type(True)) == False:
                generate_btn.click()
                logger.info("Generation button clicked")

            # Ждём результат (может занять 30-120 секунд)
            logger.info("Waiting for generation (this may take 1-2 minutes)...")

            # Ждём появления изображения с разными селекторами
            result_img = None
            img_selectors = [
                "img.generated",
                "img.result",
                ".image-container img",
                ".result-image",
                "[class*='image'] img",
                "img[src]"
            ]

            wait = WebDriverWait(driver, 180)  # 3 минуты ожидания

            for selector in img_selectors:
                try:
                    result_img = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector)),
                    )
                    logger.info(f"Found image with selector: {selector}")
                    break
                except:
                    continue

            if not result_img:
                raise Exception("Image generation timed out")

            # Получаем src изображения
            img_src = result_img.get_attribute("src")
            logger.info(f"Image generated: {img_src[:100]}...")

            # Скачиваем изображение
            img_response = requests.get(img_src, timeout=60)
            if img_response.status_code == 200:
                img = Image.open(io.BytesIO(img_response.content))
                width, height = img.size
                logger.info(f"✅ SheDevrum generated pixel city: {width}x{height}")

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
                temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"shedevrum_city_{random.randint(1, 999999)}.png")
                with open(temp_file, 'wb') as f:
                    f.write(buffer.getvalue())
                logger.info(f"Saved to: {temp_file}")
                return temp_file
            else:
                logger.error(f"Failed to download image: {img_response.status_code}")

        finally:
            driver.quit()

    except ImportError:
        logger.error("Selenium not installed. Install with: pip install selenium")
        return None
    except Exception as e:
        logger.error(f"SheDevrum web generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())

    return None
