import sys
import argparse
import modules1
from modules1 import *
from subprocess import call
from colorama import Fore,Style
import time

parser = argparse.ArgumentParser(description="Parse ip,ports,options and etc for flags")

parser.add_argument("-i", type=str, default="127.0.0.1", help="Ip flag")
parser.add_argument("-s", type=int, default=1, help="starting point")
parser.add_argument("-e", type=int, default=80, help="ending point")
args = parser.parse_args()
IP = args.i
starting_point = args.s
ending_point = args.e

if __name__ == "__main__":
    try:
        port_scanner = PortScanner(IP, starting_point, ending_point)
        open_ports:list[int] = port_scanner.scan_range()
        print(f"Open Ports: {open_ports}")
        opt:str = input(str(Fore.BLUE + "Wanna make a deeper scan with Network maping (y/n): " + Style.RESET_ALL))
        if opt == 'y' or 'Y':
            for port in open_ports:
                call(f"python3 open_ports_functions.py -i {IP} -p {port}", shell=True)
        else:
            sys.stdout.write("Returning to main menu...")
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n[*]YOU STOPPED THE ATTACK[*]\n")