import os
import sys
import paramiko

HOST = "144.31.25.159"
PORT = 22
USER = "root"
PASS = "BYAgu5iR5RgE0XuA"

LOCAL_DIR = r"C:\Users\User\Desktop\tg-post-bot"
REMOTE_DIR = "/root/tg-post-bot"

def deploy():
    print(f"Connecting to {USER}@{HOST}:{PORT}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=15)
    print("SSH Connected successfully!")

    sftp = ssh.open_sftp()
    
    # Create remote directory
    try:
        sftp.mkdir(REMOTE_DIR)
    except IOError:
        pass # Already exists
        
    files = ["bot.py", "requirements.txt", "tg-post-bot.service", "deploy.sh", "README.md"]
    for filename in files:
        local_path = os.path.join(LOCAL_DIR, filename)
        remote_path = f"{REMOTE_DIR}/{filename}"
        print(f"Uploading {filename} -> {remote_path}...")
        sftp.put(local_path, remote_path)
    
    sftp.close()
    print("Files uploaded successfully!")

    print("Running deploy.sh on remote server...")
    cmd = f"cd {REMOTE_DIR} && chmod +x deploy.sh && bash deploy.sh"
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    
    for line in iter(stdout.readline, ""):
        print(line, end="")
        
    exit_code = stdout.channel.recv_exit_status()
    print(f"Deployment finished with exit code: {exit_code}")
    
    ssh.close()

if __name__ == "__main__":
    deploy()
