import paramiko, sys, io
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HOST = '144.31.25.159'
USER = 'root'
PASS = 'BYAgu5iR5RgE0XuA'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

# Upload updated files
sftp = ssh.open_sftp()
local = r'C:\Users\User\Desktop\tg-post-bot\bot.py'
sftp.put(local, '/root/tg-post-bot/bot.py')
print('bot.py uploaded')

# Restart
stdin, stdout, stderr = ssh.exec_command('systemctl restart tg-post-bot', get_pty=True)
stdout.channel.recv_exit_status()
print('Service restarted')

# Check logs
stdin, stdout, stderr = ssh.exec_command('journalctl -u tg-post-bot --no-pager -n 15', get_pty=True)
output = stdout.read().decode(errors='replace')
for line in output.split('\n'):
    print(line)

sftp.close()
ssh.close()
