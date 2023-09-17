import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 4444

def listener_handler():
    sock.bind((HOST_IP, HOST_PORT))
    print("[+] Awaiting connection from client...")
    sock.listen()
    remote_target, remote_ip = sock.accept()
    print(f"[+] Connection recieved from {remote_ip[0]}.")
    print(f"    \___ port used on the client : {remote_ip[1]}")
    while True:
        try:
            message = input("Message_to_send#> ")
            # special behaviour for exit command : send kill signal
            if message == "exit":
                remote_target.send(message.encode())
                print("[-] sending kill signal...")
                remote_target.close()
                print("[-] Connection closed.")
                break
            remote_target.send(message.encode())
            response = remote_target.recv(4096).decode(errors="replace")
            print(response)
        except KeyboardInterrupt:
            print("Keyboard interrupt issued.")
            remote_target.send("exit".encode())
            print("[-] sending kill signal...")
            remote_target.close()
            print("[-] Connection closed.")
            break
        except Exception:
            sock.close()
            break
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener_handler()


