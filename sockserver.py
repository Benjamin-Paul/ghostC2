import socket
import sys

HOST_IP = "127.0.0.1"
HOST_PORT = 4444

def comm_in(remote_target) :
    response = remote_target.recv(4096).decode(errors="replace")
    return response

def comm_out(remote_target, message):
    remote_target.send(message.encode())

def comm_handler(remote_target, remote_ip):
    print(f"[+] Connection recieved from {remote_ip[0]}.")
    print(f"    \___ port used on the client : {remote_ip[1]}")
    while True:
        try:
            message = input("Message_to_send#> ")
            if message == "exit":
                comm_out(remote_target, message)
                print("[-] sending kill signal...")
                remote_target.close()
                print("[-] Connection closed.")
                break                
            comm_out(remote_target, message)
            response = comm_in(remote_target)
            print(response)
        except KeyboardInterrupt:
            print("Keyboard interrupt issued.")
            comm_out(remote_target, "exit")
            print("[-] sending kill signal...")
            remote_target.close()
            print("[-] Connection closed.")
            break
        except Exception:
            sock.close()
            break

def listener_handler():
    sock.bind((HOST_IP, HOST_PORT))
    print("[+] Awaiting connection from client...")
    sock.listen()
    remote_target, remote_ip = sock.accept()
    comm_handler(remote_target, remote_ip)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_handler()


