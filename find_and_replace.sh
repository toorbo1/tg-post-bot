#!/bin/bash
# Скрипт для поиска и замены файлов бота на сервере
# Использование: ssh root@SERVER "bash -s" < find_and_replace.sh

set -e

echo "=== Поиск текущего бота по токену ==="

# Ищем файлы с токеном бота
TOKEN="8760700962:AAFHtirhjGkDQMN7nC5VthqB0e3DU2Zatjo"
FOUND_FILES=$(grep -r "$TOKEN" /root/ 2>/dev/null || true)
FOUND_FILES+=$'\n'$(grep -r "$TOKEN" /home/ 2>/dev/null || true)
FOUND_FILES+=$'\n'$(grep -r "$TOKEN" /opt/ 2>/dev/null || true)
FOUND_FILES+=$'\n'$(grep -r "$TOKEN" /var/ 2>/dev/null || true)
FOUND_FILES+=$'\n'$(grep -r "$TOKEN" /usr/ 2>/dev/null || true)

if [ -z "$FOUND_FILES" ]; then
    echo "Не найдены файлы с токеном бота!"
    echo "Возможно, бот запущен в другом месте или токен в env переменных."
    exit 1
fi

echo "Найдены файлы:"
echo "$FOUND_FILES"

# Определяем директорию бота
BOT_DIR=$(echo "$FOUND_FILES" | head -1 | cut -d: -f1 | xargs dirname)
echo ""
echo "Директория бота: $BOT_DIR"

# Создаем бэкап
BACKUP_DIR="/root/tg-bot-backup-$(date +%Y%m%d_%H%M%S)"
echo "Создаем бэкап в $BACKUP_DIR..."
mkdir -p "$BACKUP_DIR"
cp -r "$BOT_DIR"/* "$BACKUP_DIR"/

echo "Бэкап создан."

# Заменяем файлы
echo "Заменяем файлы из GitHub репозитория..."
cd "$BOT_DIR"
git clone https://github.com/toorbo1/tg-post-bot.git . 2>/dev/null || git pull origin main

echo "Файлы заменены!"
echo "Перезапустите бота: systemctl restart tg-post-bot (или ваш сервис)"
