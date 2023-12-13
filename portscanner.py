import sys
import argparse
import modules1
from modules1 import *

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
        open_ports = port_scanner.scan_range()
        print(f"Open Ports: {open_ports}")
    except KeyboardInterrupt:
        print("\n[*]YOU STOPPED THE ATTACK[*]\n")