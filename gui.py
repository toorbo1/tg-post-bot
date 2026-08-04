"""Простой GUI для генератора постов"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
import sys
from datetime import datetime

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_functions import generate_ai_post, generate_pixel_city_image


class PostGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор постов")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Проверяем API ключи
        from dotenv import load_dotenv
        load_dotenv()
        self.deepseek_key = os.environ.get("DEEPSEEK_SESSION_ID", "")
        self.shedevrum_key = os.environ.get("SHEDEVRUM_API_KEY", "")

        # Создаём интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Верхняя панель с кнопками
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)

        # Кнопка генерации
        self.gen_btn = ttk.Button(
            top_frame,
            text="Сгенерировать пост",
            command=self.generate_post,
            style="Accent.TButton"
        )
        self.gen_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Кнопка выхода
        ttk.Button(
            top_frame,
            text="Выход",
            command=self.root.quit
        ).pack(side=tk.LEFT)

        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(
            top_frame,
            textvariable=self.status_var,
            anchor=tk.W
        )
        status_bar.pack(side=tk.RIGHT)

        # Основная область с вкладками
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка текста
        text_frame = ttk.Frame(notebook, padding="10")
        notebook.add(text_frame, text="Текст поста")

        self.text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            state=tk.DISABLED
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Вкладка изображения
        img_frame = ttk.Frame(notebook, padding="10")
        notebook.add(img_frame, text="Изображение")

        self.img_status = ttk.Label(img_frame, text="Изображение будет здесь", anchor=tk.CENTER)
        self.img_status.pack(expand=True, pady=(0, 10))

        # Область для отображения картинки
        self.img_label = tk.Label(img_frame, bg="#f0f0f0")
        self.img_label.pack(expand=True)

        # Вкладка настроек
        settings_frame = ttk.Frame(notebook, padding="10")
        notebook.add(settings_frame, text="Настройки")

        # Информация о ключах
        keys_text = f"""
API Ключи:

DeepSeek: {'✓ Настроен' if self.deepseek_key else '✗ Не настроен'}
Изображения: Pollinations.ai (без ключа)

Для настройки DeepSeek:
1. Получи ключ на https://platform.deepseek.com/api_keys
2. Добавь в .env файл:
   DEEPSEEK_SESSION_ID=твой_ключ
"""
        keys_label = ttk.Label(
            settings_frame,
            text=keys_text,
            justify=tk.LEFT,
            font=("Consolas", 10)
        )
        keys_label.pack(anchor=tk.NW)

    def generate_post(self):
        """Запускает генерацию в отдельном потоке"""
        if not self.deepseek_key:
            messagebox.showwarning(
                "Внимание",
                "DeepSeek ключ не настроен!\n\n"
                "Получи ключ на https://platform.deepseek.com/api_keys\n"
                "и добавь в .env файл"
            )
            return

        # Блокируем кнопку
        self.gen_btn.config(state=tk.DISABLED)
        self.status_var.set("Генерация...")

        # Очищаем виджеты
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, "Генерация текста...\n")
        self.text_widget.config(state=tk.DISABLED)

        self.img_status.config(text="Генерация изображения...")

        # Запускаем генерацию в фоне
        thread = threading.Thread(target=self._do_generate, daemon=True)
        thread.start()

    def _do_generate(self):
        try:
            # Генерируем текст
            topics = [
                "кибербезопасность", "искусственный интеллект",
                "приватность в сети", "обход блокировок",
                "пиксельная эстетика", "анонимность",
                "big data", "облачные технологии"
            ]
            topic = topics[os.urandom(1)[0] % len(topics)]

            text = generate_ai_post(topic, "long")

            # Обновляем UI в главном потоке
            self.root.after(0, lambda: self._update_text(text))

            # Генерируем изображение
            self.root.after(0, lambda: self.img_status.config(text="Генерация пиксельного города..."))
            image = generate_pixel_city_image()

            # Показываем результат
            self.root.after(0, lambda: self._show_image(image))

        except Exception as e:
            self.root.after(0, lambda: self._show_error(str(e)))
        finally:
            self.root.after(0, lambda: self.gen_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_var.set("Готов"))

    def _update_text(self, text):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        if text:
            self.text_widget.insert(tk.END, text)
            self.text_widget.insert(tk.END, f"\n\n---\nДлина: {len(text)} символов")
        else:
            self.text_widget.insert(tk.END, "Ошибка генерации текста")
        self.text_widget.config(state=tk.DISABLED)

    def _show_image(self, image_path):
        if image_path and os.path.exists(image_path):
            filename = os.path.basename(image_path)

            # Загружаем и показываем изображение
            try:
                from PIL import Image, ImageTk

                img = Image.open(image_path)

                # Масштабируем под размер окна (макс 400x300)
                max_size = (400, 300)
                img.thumbnail(max_size, Image.LANCZOS)

                # Конвертируем в формат для tkinter
                photo = ImageTk.PhotoImage(img)
                self.img_label.config(image=photo)
                self.img_label.image = photo  # сохраняем ссылку

                self.img_status.config(
                    text=f"✓ Изображение сохранено\n{filename} ({img.size[0]}x{img.size[1]})",
                    foreground="green"
                )
            except ImportError:
                self.img_status.config(
                    text=f"✓ Файл сохранён\n{filename}\nУстанови Pillow для просмотра",
                    foreground="green"
                )
            except Exception as e:
                self.img_status.config(
                    text=f"Ошибка отображения: {e}",
                    foreground="red"
                )
        else:
            self.img_status.config(
                text="✗ Ошибка генерации изображения",
                foreground="red"
            )
            self.img_label.config(image='')
            self.img_label.image = None

    def _show_error(self, error_msg):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, f"Ошибка:\n{error_msg}")
        self.text_widget.config(state=tk.DISABLED)
        self.img_status.config(text="Отменено из-за ошибки", foreground="red")
        messagebox.showerror("Ошибка", error_msg)


def main():
    root = tk.Tk()
    app = PostGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
