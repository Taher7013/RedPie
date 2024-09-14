import os
import socket
import threading
import nmap3

# Define the path to NSE scripts
NSE_PATH = "/modules/utils/NSE"

def service_version(port, banner=None):
    """Get service version from banner."""
    # (Same as before)

def scan_tcp_port(target, port, verbose, timeout):
    """Scan TCP port with optional verbosity and custom timeout."""
    # (Same as before)

def scan_udp_port(target, port, verbose, timeout):
    """Scan UDP port with optional verbosity and custom timeout."""
    # (Same as before)

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
    """List available NSE scripts."""
    try:
        # List files in the NSE_PATH directory
        scripts = [f for f in os.listdir(NSE_PATH) if os.path.isfile(os.path.join(NSE_PATH, f))]
        print("Available NSE scripts:")
        for script in scripts:
            print(script)
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
