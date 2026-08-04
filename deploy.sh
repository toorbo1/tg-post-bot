#!/bin/bash
# Telegram Post Generator Bot Deployment Script for Debian 13
set -e

echo "=== Deploying Telegram Post Bot ==="

# 1. Update packages and install python3 & venv
echo "[1/5] Updating packages and installing Python 3..."
apt-get update -y
apt-get install -y python3 python3-pip python3-venv curl

# 2. Setup project directory
APP_DIR="/root/tg-post-bot"
echo "[2/5] Creating application directory $APP_DIR..."
mkdir -p "$APP_DIR"
cp -r . "$APP_DIR/"
cd "$APP_DIR"

# 3. Virtual environment & dependencies
echo "[3/5] Setting up Virtual environment and installing dependencies..."
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 4. Setup systemd service
echo "[4/5] Setting up systemd service..."
cp tg-post-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable tg-post-bot
systemctl restart tg-post-bot

# 5. Check status
echo "[5/5] Checking service status..."
sleep 2
systemctl status tg-post-bot --no-pager

echo ""
echo "========================================="
echo " 🎉 Telegram Post Bot successfully deployed!"
echo " Token: ${BOT_TOKEN:-YOUR_BOT_TOKEN_HERE}"
echo " Service name: tg-post-bot"
echo " To check logs: journalctl -u tg-post-bot -f"
echo "========================================="
