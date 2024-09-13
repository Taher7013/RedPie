import argparse
import socket
import re
import threading
import nmap3

# Define services and version patterns
services = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    3306: "mysql",
    3389: "rdp",
    5432: "postgresql",
    5900: "vnc",
    8000: "http-proxy",
    9000: "http",
    9200: "elasticsearch",
    27017: "mongodb"
}

version_patterns = {
    "ftp": r"FTP\/(\d+\.\d+)",
    "ssh": r"SSH-(\d+\.\d+)",
    "telnet": r"Telnet\/(\d+\.\d+)",
    "smtp": r"ESMTP|SMTP\/(\d+\.\d+)",
    "http": r"HTTP\/(\d+\.\d+)",
    "mysql": r"Ver (\d+\.\d+\.\d+)",
    "postgresql": r"PostgreSQL (\d+\.\d+)",
    "redis": r"Redis server v=(\d+\.\d+\.\d+)",
    "mongodb": r"MongoDB (\d+\.\d+\.\d+)"
}

def service_version(port, banner=None):
    service = services.get(port, "unknown")
    version = "unknown"
    if banner:
        if service in version_patterns:
            match = re.search(version_patterns[service], banner)
            if match:
                version = match.group(1)
        # Default to version extraction if service pattern not found
        if version == "unknown":
            general_version_match = re.search(r"(\d+\.\d+\.\d+)", banner)
            if general_version_match:
                version = general_version_match.group(1)
    
    return f"{service}/{version}"

def scan_tcp_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                sock.send(b'HEAD / HTTP/1.1\r\n\r\n')
                banner = sock.recv(1024).decode().strip()
                service_info = service_version(port, banner)
            except Exception:
                service_info = service_version(port)
            print(f"PORT {port}/tcp\tOPEN\t{service_info}")
    finally:
        sock.close()

def scan_udp_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    try:
        sock.sendto(b'', (target, port))
        try:
            banner, _ = sock.recvfrom(1024)
            service_info = service_version(port, banner.decode().strip())
            print(f"PORT {port}/udp\tOPEN\t{service_info}")
        except socket.error:
            print(f"PORT {port}/udp\tOPEN\t(no banner)")
    except socket.timeout:
        print(f"PORT {port}/udp\tFILTERED")
    except Exception as e:
        print(f"Error scanning UDP Port {port}: {e}")
    finally:
        sock.close()

def scan_ports(target, start_port=1, end_port=65535, protocol='tcp'):
    print(f"Starting {protocol.upper()} port scan on {target} from port {start_port} to {end_port}...")
    threads = []
    for port in range(start_port, end_port + 1):
        if protocol == 'tcp':
            thread = threading.Thread(target=scan_tcp_port, args=(target, port))
        elif protocol == 'udp':
            thread = threading.Thread(target=scan_udp_port, args=(target, port))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def nmap_scan(target):
    print(f"Running Nmap scan on {target}...")
    nmap = nmap3.Nmap()
    try:
        # Perform OS detection
        os_result = nmap.nmap_os_detection(target)
        if os_result:
            for os_entry in os_result:
                os_class = os_entry.get('osclass', 'Unknown')
                os_name = os_entry.get('osfamily', 'Unknown')
                os_version = os_entry.get('osversion', 'Unknown')
                print(f"OS Details: Class: {os_class}, Name: {os_name}, Version: {os_version}")
        else:
            print("No OS details found.")
        
        # Perform version detection
        version_result = nmap.nmap_version_detection(target)
        if version_result:
            for service in version_result:
                port = service['port']
                protocol = service['protocol']
                service_name = service['service']['name']
                version = service['service']['version']
                print(f"PORT {port}/{protocol}\tOPEN\t{service_name} {version}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Multi-Tool for various functionalities")
    subparsers = parser.add_subparsers(dest="command", help="Choose a tool to run")

    # Port Scanner Module
    parser_scan = subparsers.add_parser("portscan", help="Scan open ports on a target")
    parser_scan.add_argument("target", help="Target IP address or hostname")
    parser_scan.add_argument("--start-port", type=int, default=1, help="Starting port")
    parser_scan.add_argument("--end-port", type=int, default=65535, help="Ending port")
    parser_scan.add_argument("--protocol", choices=['tcp', 'udp'], default='tcp', help="Protocol to scan (default: tcp)")

    # OS Detection Module
    parser_os = subparsers.add_parser("osdetect", help="Perform OS detection on a target")
    parser_os.add_argument("target", help="Target IP address or hostname")

    args = parser.parse_args()

    if args.command == "portscan":
        try:
            target_ip = socket.gethostbyname(args.target)  # Convert hostname to IP
            scan_ports(target_ip, args.start_port, args.end_port, args.protocol)
            nmap_scan(target_ip)
        except socket.error as e:
            print(f"Error resolving IP for {args.target}: {e}")
            print("Invalid target or IP resolution failed.")
    
    elif args.command == "osdetect":
        try:
            target_ip = socket.gethostbyname(args.target)  # Convert hostname to IP
            nmap_scan(target_ip)  # Perform OS detection
        except socket.error as e:
            print(f"Error resolving IP for {args.target}: {e}")
            print("Invalid target or IP resolution failed.")
    
    else:
        parser.print_help()