import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

def run_ssh_command(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(os.getenv("192.168.182.237"), username=os.getenv("root"), password=os.getenv("redhat"))
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    return output if output else error
