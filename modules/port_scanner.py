import socket
import re
import threading
import nmap3

def service_version(port, banner=None):
    """Get service version from banner"""
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
        "ssh": r"SSH-(\d+\.\d+)",  # SSH version detection pattern
        "telnet": r"Telnet\/(\d+\.\d+)",
        "smtp": r"ESMTP|SMTP\/(\d+\.\d+)",
        "http": r"HTTP\/(\d+\.\d+)",
        "mysql": r"Ver (\d+\.\d+\.\d+)",
        "postgresql": r"PostgreSQL (\d+\.\d+)",
        "redis": r"Redis server v=(\d+\.\d+\.\d+)",
        "mongodb": r"MongoDB (\d+\.\d+\.\d+)"
    }
    
    service = services.get(port, "unknown")
    version = "unknown "
    if banner:
        if service in version_patterns:
            match = re.search(version_patterns[service], banner)
            if match:
                version = match.group(1)
        # Fallback to extract a generic version format if no specific pattern found
        if version == "unknown":
            general_version_match = re.search(r"(\d+\.\d+\.\d+)", banner)
            if general_version_match:
                version = general_version_match.group(1)
    
    return f"{service}/{version}"

def scan_tcp_port(target, port, verbose, timeout):
    """Scan TCP port with optional verbosity and custom timeout."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                sock.send(b'HEAD / HTTP/1.1\r\n\r\n')  # For HTTP services
                banner = sock.recv(1024).decode().strip()
                service_info = service_version(port, banner)
                if verbose:
                    print(f"Verbose: Received banner: {banner}")
            except Exception:
                service_info = service_version(port)
            print(f"PORT {port}/tcp\tOPEN\t{service_info}")
        elif verbose:
            print(f"Verbose: PORT {port}/tcp is closed")
    finally:
        sock.close()

def scan_udp_port(target, port, verbose, timeout):
    """Scan UDP port with optional verbosity and custom timeout."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(b'', (target, port))
        try:
            banner, _ = sock.recvfrom(1024)
            service_info = service_version(port, banner.decode().strip())
            if verbose:
                print(f"Verbose: Received banner: {banner.decode().strip()}")
            print(f"PORT {port}/udp\tOPEN\t{service_info}")
        except socket.error:
            if verbose:
                print(f"Verbose: No response for port {port}/udp")
            print(f"PORT {port}/udp\tOPEN\t(no banner)")
    except socket.timeout:
        print(f"PORT {port}/udp\tFILTERED")
    except Exception as e:
        if verbose:
            print(f"Verbose: Error scanning UDP Port {port}: {e}")
        print(f"Error scanning UDP Port {port}: {e}")
    finally:
        sock.close()

def scan_ports(target, start_port=1, end_port=65535, protocol='tcp', os_detect=False, verbose=False, timeout=4):
    """Scan ports with optional OS detection, verbosity, and timeout."""
    print(f"Starting {protocol.upper()} port scan on {target} from port {start_port} to {end_port}...")
    if verbose:
        print(f"Verbose mode enabled. Timeout set to {timeout} seconds.")
    
    threads = []
    for port in range(start_port, end_port + 1):
        if protocol == 'tcp':
            thread = threading.Thread(target=scan_tcp_port, args=(target, port, verbose, timeout))
        elif protocol == 'udp':
            thread = threading.Thread(target=scan_udp_port, args=(target, port, verbose, timeout))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    if os_detect:
        nmap_scan(target)

def nmap_scan(target):
    """Perform Nmap scan"""
    print(f"Running Nmap scan on {target}...")
    nmap = nmap3.Nmap()
    try:
        # Perform OS detection
        os_result = nmap.nmap_os_detection(target)
        if os_result:
            for os_entry in os_result:
                os_class = os_entry.get('osclass', 'Unknown')
                os_name = os_entry.get('osfamily', 'Unknown')
                print(f"OS Class: {os_class}, OS Name: {os_name}")
        else:
            print("No OS detection results.")
    except Exception as e:
        print(f"An error occurred during Nmap OS detection: {e}")
