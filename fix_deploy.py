import paramiko
import time
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = "144.31.25.159"
PORT = 22
USER = "root"
PASS = "BYAgu5iR5RgE0XuA"

commands = [
    "cd /root/tg-post-bot && python3 -m venv venv",
    "cd /root/tg-post-bot && ./venv/bin/pip install -r requirements.txt",
    "cp /root/tg-post-bot/tg-post-bot.service /etc/systemd/system/",
    "systemctl daemon-reload",
    "systemctl enable tg-post-bot",
    "systemctl restart tg-post-bot",
    "systemctl status tg-post-bot --no-pager 2>&1",
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=15)
print("Connected!")

for cmd in commands:
    print(f"\n$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True, timeout=180)
    for line in iter(stdout.readline, ""):
        if line.strip():
            print(line, end="")
    err = stderr.read().decode(errors='replace').strip()
    if err:
        print(f"[stderr] {err}")
    exit_code = stdout.channel.recv_exit_status()
    if exit_code != 0:
        print(f"[exit code: {exit_code}]")

ssh.close()
print("\nDone!")
