import subprocess
import socket
import os

message = "cd test"
directory = str(message.split(" ")[1])
os.chdir(directory)
cur_dir = os.getcwd()
print(f"[+] Changed directory to {cur_dir}.")