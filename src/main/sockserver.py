import sys
sys.path.insert(0, 'src/modules')
from cli import Cli
from server import Server
from attacker import Attacker


if __name__ == "__main__":
    try:
        communication_server = Server()
        main_attacker = Attacker()
        interface = Cli()
        interface.run(communication_server, main_attacker)
    except Exception as error:
        print(f"An error occured : {error}")
