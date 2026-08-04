# Инструкция по замене бота на сервере

## Шаг 1: Подключение к серверу

Когда SSH станет доступен, подключитесь:
```bash
ssh root@144.31.25.159
# Пароль: BYAgu5iR5RgE0XuA
```

## Шаг 2: Поиск текущего бота

Выполните поиск файлов с токеном:
```bash
grep -r "8760700962:AAFHtirhjGkDQMN7nC5VthqB0e3DU2Zatjo" /root/ /home/ /opt/ /var/ 2>/dev/null
```

Или найдите запущенный процесс Python:
```bash
ps aux | grep python
# или
ps aux | grep bot
```

## Шаг 3: Определение директории бота

После нахождения файла определите директорию:
```bash
ls -la /путь/к/директории/бота
```

## Шаг 4: Бэкап текущих файлов

```bash
cp -r /путь/к/директории/бота /root/tg-bot-backup-$(date +%Y%m%d)
```

## Шаг 5: Замена файлов

### Вариант A: Через git clone (рекомендуется)
```bash
cd /путь/к/директории/бота
git clone https://github.com/toorbo1/tg-post-bot.git . 2>/dev/null || git pull origin main
```

### Вариант B: Вручную
Скачайте файлы из репозитория и замените:
- bot.py
- requirements.txt
- deploy.sh
- и другие файлы проекта

## Шаг 6: Настройка переменных окружения

Создайте файл `.env` в директории бота:
```bash
cat > .env << 'EOF'
BOT_TOKEN=your_bot_token_here
AI_STUDIO_KEY=your_ai_studio_key_here
POLLINATIONS_KEY=your_pollinations_key_here
EOF
```

## Шаг 7: Обновление зависимостей

```bash
pip3 install -r requirements.txt
# или если используется venv
./venv/bin/pip install -r requirements.txt
```

## Шаг 8: Перезапуск бота

Если используется systemd:
```bash
systemctl restart tg-post-bot
systemctl status tg-post-bot
```

Если используется PM2:
```bash
pm2 restart all
pm2 status
```

Или просто запустите:
```bash
python3 bot.py &
```

## Проверка работы

Откройте Telegram и найдите вашего бота. Он должен отвечать на команды.
