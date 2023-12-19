import nmap
import argparse
from colorama import Fore,Style

parser = argparse.ArgumentParser("Parsing target and ports for vuln scan")

parser.add_argument("-i", type=str, required=True, help="Target ip")
parser.add_argument("-p", type=int, nargs="+", required=True, help="ports that might be vulnerable")

args = parser.parse_args()

def vulns_in_open_ports(target: str, ports: list[int]) -> None:
    nm = nmap.PortScanner()
    for port in ports:
        arguments = f'-p{port} -sV -v --script ALL'
        nm.scan(target, arguments=arguments)
        
        for host in nm.all_hosts():
            print(Fore.RED + "-" * 20 + Style.RESET_ALL)
            print(f"Host: {host}")
            print("Host State: {0}".format(nm[host].state()))
            
            for proto in nm[host].all_protocols():
                print("Protocol: {0}".format(proto))
                scanned_ports = nm[host][proto].keys()
                
                for scanned_port in scanned_ports:
                    print("Ports: {0}\tState: {1}".format(scanned_port, nm[host][proto][scanned_port]['state']))
                    
                    if 'script' in nm[host][proto][scanned_port]:
                        print("Script: ")
                        for script in nm[host][proto][scanned_port]['script']:
                            print("\t{0} : {1}".format(script, nm[host][proto][scanned_port]['script'][script]))
                        print(Fore.RED + "-" * 20 + Style.RESET_ALL)

if __name__ == "__main__":
    vulns_in_open_ports(args.i, args.p)
