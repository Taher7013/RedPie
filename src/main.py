import os
import argparse
import threading
import nmap3
from modules import port_scanner, web_fuzzer, password_cracker, serverftp, clientftp,websnap
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the path to NSE scripts
NSE_PATH = "/modules/utils/NSE"

def print_banner():
    """Print the banner with colors"""
    banner = r"""
     ____  __________  ____  _ ______
   / __ \/ ____/ __ \/ __ \(_) ____/
  / /_/ / __/ / / / / /_/ / / __/   
 / _, _/ /___/ /_/ / ____/ / /___   
/_/ |_/_____/_____/_/   /_/_____/   
                                    
    """
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "Welcome to the Python Multi-Tool suite!")
    print(Fore.GREEN + "Select a module to run from the options below:")
    print(Fore.MAGENTA + "=" * 50)

def service_version(port, banner=None):
    """Get service version from banner."""
    # (Add your logic here)

def scan_tcp_port(target, port, verbose, timeout):
    """Scan TCP port with optional verbosity and custom timeout."""
    # (Add your logic here)

def scan_udp_port(target, port, verbose, timeout):
    """Scan UDP port with optional verbosity and custom timeout."""
    # (Add your logic here)

def nmap_scan(target, scripts=None):
    """Perform Nmap scan with optional NSE scripts."""
    print(f"Running Nmap scan on {target}...")
    nmap = nmap3.Nmap()

    try:
        if scripts:
            # Fetch and run scripts from the utils/NSE path
            for script in scripts:
                script_path = os.path.join(NSE_PATH, f"{script}.nse")  # Append .nse extension
                if os.path.isfile(script_path):
                    print(f"Running script {script} from {script_path}...")
                    scan_results = nmap.nmap_run_script(target, scripts=[script_path])
                    if scan_results:
                        print(f"Results for script {script}:")
                        print(scan_results)
                    else:
                        print(f"No results from script {script}.")
                else:
                    print(f"Script {script} not found in {NSE_PATH}.")
        else:
            # Perform normal OS detection or basic scan
            scan_results = nmap.nmap_os_detection(target)
            if scan_results:
                print(scan_results)
            else:
                print("No results from Nmap scan.")
    except Exception as e:
        print(f"An error occurred during the Nmap scan: {e}")

def list_nse_scripts():
    """List available NSE scripts and provide a brief explanation of what NSE is."""
    # Brief explanation of NSE
    
    nse_info = """
    =======================================================================================================================
    # The Nmap Scripting Engine (NSE) is one of Nmap's most powerful features.                                            #
    # It allows users to write and share simple scripts that automate a wide variety of networking tasks.                 #
    # These scripts are used to perform a wide range of tasks including network discovery, vulnerability detection,       #
    # and more specialized tasks such as backdoor detection and advanced fingerprinting.                                  #
    #                                                                                                                     #
    # Here are the available NSE scripts in the '/modules/utils/NSE' directory:                                           #
    # Usage :                                                                                                             #
    #       python3 main.py portscan --script<NSE>                                                                        #
    =======================================================================================================================
    +----+---------------------------------------+-----------------------------------------------------------------------------------+-----------------+
    | id | script_name                           | description                                                                       | category        |
    +----+---------------------------------------+-----------------------------------------------------------------------------------+-----------------+
    | 1  | broadcast-avahi-dos.nse               | Detects and exploits the Avahi daemon to perform a denial-of-service (DoS) attack | Exploitation   |
    | 2  | broadcast-dhcp-discover.nse           | Discovers DHCP servers on the network                                             | Discovery      |
    | 3  | broadcast-dropbox-listener.nse        | Detects Dropbox listeners on the network                                          | Discovery      |
    | 4  | broadcast-eigrp-discovery.nse         | Discovers EIGRP neighbors on the network                                          | Discovery      |
    | 5  | broadcast-http-cheerios.nse           | Discovers HTTP servers on the network                                             | Discovery      |
    | 6  | broadcast-igmp-discovery.nse          | Discovers IGMP multicast groups on the network                                    | Discovery      |
    | 7  | broadcast-listener.nse                | Detects listeners on the network                                                  | Discovery      |
    | 8  | broadcast-ms-sql-discover.nse         | Discovers Microsoft SQL Server instances on the network                           | Discovery      |
    | 9  | broadcast-netbios-master-browser.nse  | Discovers NetBIOS master browsers on the network                                  | Discovery      |
    | 10 | broadcast-novell-locate.nse           | Discovers Novell servers on the network                                           | Discovery      |
    | 11 | broadcast-ping.nse                    | Sends a ping request to hosts on the network to discover them                     | Discovery      |
    | 12 | broadcast-rip-discovery.nse           | Discovers RIPv1 and RIPv2 neighbors on the network                                | Discovery      |
    | 13 | broadcast-upnp-info.nse               | Discovers UPnP devices on the network                                             | Discovery      |
    | 14 | broadcast-wsdd-discover.nse           | Discovers WS-Discovery devices on the network                                     | Discovery      |
    | 15 | brute-ssh.nse                         | Performs a brute-force attack on SSH servers to guess passwords                   |Brute Force     |
    | 16 | cassandra-brute.nse                   | Performs a brute-force attack on Cassandra databases to guess passwords          _|Brute Force     |____
    | 17 | cassandra-info.nse                    | Gathers information about Cassandra databases                                   | Information Gathering |
    | 18 | citrix-enum.nse                       | Enumerates Citrix servers and their published applications                      | Information Gathering |
    | 19 | clock-skew.nse                        | Detects clock skew between the target system and the Nmap scanner               | Information Gathering |
    +----+---------------------------------------+---------------------------------------------------------------------------------+-----------------------+
    """
    print(nse_info)
    
    try:
        # List files in the NSE_PATH directory
        scripts = [f for f in os.listdir(NSE_PATH) if os.path.isfile(os.path.join(NSE_PATH, f))]
        if scripts:
            for script in scripts:
                print(script)
        else:
            print("No scripts found in the NSE directory.")
    except Exception as e:
        print(f"An error occurred while listing NSE scripts: {e}")

def scan_ports(target, start_port=1, end_port=65535, protocol='tcp', os_detect=False, verbose=False, timeout=4, scripts=None):
    """Scan ports with optional OS detection, verbosity, timeout, and NSE scripts."""
    print(f"Starting {protocol.upper()} port scan on {target} from port {start_port} to {end_port}...")
    if verbose:
        print(f"Verbose mode enabled. Timeout set to {timeout} seconds.")
    
    threads = []
    for port in range(start_port, end_port + 1):
        if protocol == 'tcp':
            thread = threading.Thread(target=scan_tcp_port, args=(target, port, verbose, timeout))
        elif protocol == 'udp':
            thread = threading.Thread(target=scan_udp_port, args=(target, port, verbose, timeout))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if os_detect:
        print("Performing OS detection using Nmap...")
        nmap_scan(target, scripts)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description=Fore.CYAN + "Python Multi-Tool for various functionalities")
    subparsers = parser.add_subparsers(dest="command", help="Choose a tool to run")
    
    # Port Scanner Module
    parser_scan = subparsers.add_parser("portscan", help="Scan open ports on a target")
    parser_scan.add_argument("target", help="Target IP address or hostname")
    parser_scan.add_argument("--start-port", type=int, default=1, help="Starting port")
    parser_scan.add_argument("--end-port", type=int, default=65535, help="Ending port")
    parser_scan.add_argument("--protocol", choices=['tcp', 'udp'], default='tcp', help="Protocol to scan (default: tcp)")

    # Web Fuzzer Module
    parser_fuzz = subparsers.add_parser("webfuzz", help="Fuzz for hidden web directories")
    parser_fuzz.add_argument("url", help="Target URL to fuzz (e.g., http://example.com)")
    parser_fuzz.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file (e.g., /path/to/wordlist.txt)")
    parser_fuzz.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode to show all attempts")
    parser_fuzz.add_argument("-f", "--filter-status", nargs="+", type=int, help="Filter results by status codes (e.g., 200 403 500)")
    parser_fuzz.add_argument("--headers", nargs="+", help="Custom headers to add to the request (e.g., User-Agent:Test Authorization:Bearer abc123)")
    parser_fuzz.add_argument("--timeout", type=int, default=5, help="Set request timeout in seconds (default is 5)")
    parser_fuzz.add_argument("-t", "--threads", type=int, default=1, help="Number of threads to use (default is 1)")

    # Password Cracker Module
    parser_crack = subparsers.add_parser("crack", help="Password cracking tool")
    parser_crack.add_argument("hash", help="Hash to crack")
    parser_crack.add_argument("-w", "--wordlist", required=True, help="Wordlist for cracking")

    # Server FTP Module
    parser_serverftp = subparsers.add_parser("serverftp", help="FTP server tool")
    parser_serverftp.add_argument("host", help="FTP server host (e.g., 192.168.1.100)")
    parser_serverftp.add_argument("port", type=int, default=21, help="Port to run the FTP server on (default: 21)")

    # Client FTP Module
    parser_clientftp = subparsers.add_parser("clientftp", help="FTP client tool")
    parser_clientftp.add_argument("host", help="FTP server host to connect to (e.g., 192.168.1.100)")
    parser_clientftp.add_argument("username", help="FTP username")
    parser_clientftp.add_argument("password", help="FTP password")

    # websnap Module
    parser_websnap = subparsers.add_parser("websnap",help='Take a screenshot of a webpage.')
    parser_websnap.add_argument('--url', type=str, help='The URL of the webpage to screenshot.')
    parser_websnap.add_argument('-o', '--output', type=str, help='Optional output filename for the screenshot (default: <webpage>.png)')
    parser_websnap.add_argument('-f', '--fromfile', type=str, help='Optional file containing a list of URLs to screenshot (one per line).')
    parser_websnap.add_argument('-vi', '--view', action='store_true', help='Optional auto view the images after taken')
    parser_websnap.add_argument('-cf', '--clearafter', action='store_true', help='Clear images after viewing')


    # Add --script-help argument globally
    parser.add_argument("--script-help", action="store_true", help="List available NSE scripts and explain what NSE is")

    args = parser.parse_args()

    # Handle the --script-help command
    if args.script_help:
        list_nse_scripts()
    elif args.command == "portscan":
        port_scanner.scan_ports(args.target, args.start_port, args.end_port, args.protocol)
    elif args.command == "webfuzz":
        web_fuzzer.fuzz_directories(args.url, args.wordlist, verbose=args.verbose, filter_status=args.filter_status, headers=args.headers, timeout=args.timeout, threads=args.threads)
    elif args.command == "crack":
        password_cracker.crack_password(args.hash, args.wordlist)
    elif args.command == "serverftp":
        print(Fore.CYAN + f"Starting FTP server on {args.host}:{args.port}...")  # Add your FTP server logic here
    elif args.command == "clientftp":
        print(Fore.CYAN + f"Connecting to FTP server at {args.host} with username {args.username}...")  # Add your FTP client logic here
    elif args.command == 'websnap':
        print(Fore.CYAN + f"websnap !!!")
        websnap.core(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
