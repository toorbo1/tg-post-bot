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
    """Генерирует ПИКСЕЛЬНЫЙ ГОРОД через Pollinations.ai (быстро и без ключа)"""

    # Промпт для пиксельного города
    style_prompt = "pixel art cyberpunk city, neon purple and cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio, high quality, crisp edges, ultra detailed"

    try:
        # Используем Pollinations.ai (работает без ключа, быстро!)
        encoded_prompt = requests.utils.quote(style_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&seed={random.randint(1, 999999)}&nologo=true&model=turbo"

        logger.info(f"Generating pixel city via Pollinations (fast)...")

        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            from PIL import Image
            import io

            img = Image.open(io.BytesIO(response.content))
            width, height = img.size
            logger.info(f"Generated image: {width}x{height}")

            # Проверяем соотношение сторон и обрезаем до 4:3
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
                temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"pixel_city_{random.randint(1, 999999)}.png")
                with open(temp_file, 'wb') as f:
                    f.write(buffer.getvalue())
                logger.info(f"Cropped to: {img.size[0]}x{img.size[1]} (4:3)")
                return temp_file
            else:
                temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"pixel_city_{random.randint(1, 999999)}.png")
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Saved pixel city: {width}x{height}")
                return temp_file
        else:
            logger.error(f"Pollinations error: {response.status_code}")
    except Exception as e:
        logger.error(f"Image generation failed: {e}")

    return None


def generate_pixel_city_shedevrum():
    """Генерирует ПИКСЕЛЬНЫЙ ГОРОД через РЕАЛЬНЫЙ Шедеврум с Selenium (медленно, но качественно)"""

    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
        import io
        from PIL import Image

        # Промпт для пиксельного города
        style_prompt = "pixel art cyberpunk city, neon purple and cyan colors, detailed skyscrapers, 16-bit retro game style, sharp pixels, no blur, high contrast, futuristic skyline, flying cars, holograms, clean lines, professional pixel art, 4:3 aspect ratio"

        logger.info(f"🎨 Opening REAL SheDevrum via Selenium...")

        # Запускаем браузер
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)

        try:
            # Открываем Шедеврум (актуальный URL)
            logger.info("Loading SheDevrum page...")
            driver.get("https://shedevrum.ai/")

            # Ждём полной загрузки страницы
            time.sleep(5)

            # Ищем поле ввода разными способами
            logger.info("Searching for input field...")

            input_box = None
            selectors = [
                "textarea",
                "input[type='text']",
                "[contenteditable='true']",
                ".TextInput textarea",
                "#prompt-input",
                "[role='textbox']"
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
                raise Exception("Could not find input field - SheDevrum may have changed their UI")

            # Кликаем и вводим промпт
            logger.info("Entering prompt...")
            input_box.click()
            time.sleep(0.5)

            # Вводим текст
            for char in style_prompt:
                try:
                    input_box.send_keys(char)
                except:
                    break
                time.sleep(0.01)

            logger.info("Prompt entered")
            time.sleep(1)

            # Ищем кнопку генерации
            logger.info("Finding generate button...")
            generate_btn = None

            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if btn.is_displayed():
                    text = btn.text.lower()
                    if any(word in text for word in ["сгенерировать", "generate", "создать"]):
                        generate_btn = btn
                        break

            if generate_btn:
                logger.info("Clicking generate button...")
                generate_btn.click()
            else:
                # Пробуем Enter
                logger.info("Pressing Enter...")
                input_box.send_keys(Keys.RETURN)

            # Ждём результат (до 3 минут)
            logger.info("Waiting for generation (up to 3 minutes)...")

            result_img = None
            wait = WebDriverWait(driver, 180)

            img_selectors = [
                "img.generated",
                "img.result",
                ".image-container img",
                ".Result img",
                "[class*='result'] img",
                "img[src^='data:image']"
            ]

            for selector in img_selectors:
                try:
                    result_img = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    logger.info(f"Found image with: {selector}")
                    break
                except TimeoutException:
                    continue

            if not result_img:
                raise Exception("Generation timed out after 3 minutes")

            # Получаем URL изображения
            img_src = result_img.get_attribute("src") or result_img.get_attribute("data-src")

            if not img_src or img_src.startswith("data:"):
                # Если base64, используем напрямую
                if img_src and img_src.startswith("data:"):
                    img_data = img_src.split(",")[1]
                    import base64
                    img = Image.open(io.BytesIO(base64.b64decode(img_data)))
                else:
                    raise Exception("No valid image source found")
            else:
                # Скачиваем по URL
                logger.info(f"Downloading from: {img_src[:100]}...")
                img_response = requests.get(img_src, timeout=60)
                if img_response.status_code != 200:
                    raise Exception(f"Failed to download: {img_response.status_code}")
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
            temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"shedevrum_real_{random.randint(1, 999999)}.png")
            with open(temp_file, 'wb') as f:
                f.write(buffer.getvalue())

            logger.info(f"Saved to: {temp_file}")
            return temp_file

        finally:
            driver.quit()

    except ImportError:
        logger.error("Selenium not installed. Install with: pip install selenium")
        return None
    except Exception as e:
        logger.error(f"REAL SheDevrum failed: {e}")
        import traceback
        logger.error(traceback.format_exc())

    return None
