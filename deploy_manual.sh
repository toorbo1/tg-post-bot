#!/bin/bash
# Ручная установка Telegram бота на сервер
# Запустить на сервере: bash deploy_manual.sh

set -e

echo "=== Установка Telegram Post Bot ==="

# Создаем директорию
APP_DIR="/root/tg-post-bot"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Клонируем репозиторий
git clone https://github.com/toorbo1/tg-post-bot.git . 2>/dev/null || git pull origin main

# Устанавливаем зависимости
apt-get update -y
apt-get install -y python3 python3-pip python3-venv curl systemd

# Создаем виртуальное окружение
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Создаем файл .env с ключами (заполните позже)
cat > .env << 'EOF'
BOT_TOKEN=your_bot_token_here
AI_STUDIO_KEY=your_ai_studio_key_here
POLLINATIONS_KEY=your_pollinations_key_here
EOF

# Настраиваем systemd сервис
cat > /etc/systemd/system/tg-post-bot.service << 'EOF'
[Unit]
Description=Telegram Post Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/tg-post-bot
EnvironmentFile=/root/tg-post-bot/.env
ExecStart=/root/tg-post-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Включаем и запускаем сервис
systemctl daemon-reload
systemctl enable tg-post-bot
systemctl restart tg-post-bot

echo ""
echo "========================================="
echo " Бот установлен!"
echo " Для проверки: systemctl status tg-post-bot"
echo " Для логов: journalctl -u tg-post-bot -f"
echo " Не забудьте заполнить .env ключами!"
echo "========================================="
