import sys
sys.path.insert(0, 'src/modules')
from cli import Cli
from server import Server
from attacker import Attacker


if __name__ == "__main__":
    try:
        server = Server()
        attacker = Attacker()
        interface = Cli()
        interface.run(server, attacker)
    except Exception as error:
        print(f"An error occured : {error}")
