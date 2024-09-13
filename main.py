import argparse
import nmap3
from modules import port_scanner, web_fuzzer, password_cracker

def print_banner():
    """Print the banner"""
    banner = r"""
     ____  __________  ____  _ ______
   / __ \/ ____/ __ \/ __ \(_) ____/
  / /_/ / __/ / / / / /_/ / / __/   
 / _, _/ /___/ /_/ / ____/ / /___   
/_/ |_/_____/_____/_/   /_/_____/   
                                    
    """
    print(banner)
    print("Welcome to the Python Multi-Tool suite!")
    print("Select a module to run from the options below:")
    print("=" * 50)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Python Multi-Tool for various functionalities")
    subparsers = parser.add_subparsers(dest="command", help="Choose a tool to run")
    
    # Port Scanner Module
    parser_scan = subparsers.add_parser("portscan", help="Scan open ports on a target")
    parser_scan.add_argument("target", help="Target IP address or hostname")
    parser_scan.add_argument("--start-port", type=int, default=1, help="Starting port")
    parser_scan.add_argument("--end-port", type=int, default=65535, help="Ending port")
    parser_scan.add_argument("--protocol", choices=['tcp', 'udp'], default='tcp', help="Protocol to scan (default: tcp)")
    parser_scan.add_argument("-O", "--os-detect", action="store_true", help="Enable OS detection using Nmap")
    parser_scan.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser_scan.add_argument("-t", "--timeout", type=int, default=4, help="Set the timeout for each port scan (default is 4 seconds)")
    
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
    
    args = parser.parse_args()
    
    if args.command == "portscan":
        port_scanner.scan_ports(args.target, args.start_port, args.end_port, args.protocol, args.os_detect, args.verbose, args.timeout)
    elif args.command == "webfuzz":
        web_fuzzer.fuzz_directories(args.url, args.wordlist, verbose=args.verbose, filter_status=args.filter_status, headers=args.headers, timeout=args.timeout, threads=args.threads)
    elif args.command == "crack":
        password_cracker.crack_password(args.hash, args.wordlist)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
