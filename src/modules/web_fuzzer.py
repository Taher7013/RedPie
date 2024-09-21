import os
import requests
import argparse
import threading

# Function to fuzz directories
def fuzz(url, wordlist_path, verbose=False, filter_status=None, headers=None, timeout=5):
    with open(wordlist_path, "r") as wordlist:
        for line in wordlist:
            directory = line.strip()
            full_url = f"{url}/{directory}"
            try:
                response = requests.get(full_url, headers=headers, timeout=timeout)
                # Check if the user wants to filter specific status codes
                if filter_status:
                    if response.status_code in filter_status:
                        print(f"Found ({response.status_code}): {full_url}")
                elif response.status_code == 200:
                    print(f"Found: {full_url}")
                # Verbose mode: Print all attempts
                if verbose:
                    print(f"Checked: {full_url} - Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to {full_url}: {e}")

# Function to run fuzzing with optional threading for speed
def threaded_fuzz(url, wordlist_path, verbose=False, filter_status=None, headers=None, timeout=5, threads=10):
    with open(wordlist_path, "r") as wordlist:
        directories = [line.strip() for line in wordlist]

    def worker(directories_chunk):
        for directory in directories_chunk:
            full_url = f"{url}/{directory}"
            try:
                response = requests.get(full_url, headers=headers, timeout=timeout)
                if filter_status:
                    if response.status_code in filter_status:
                        print(f"Found ({response.status_code}): {full_url}")
                elif response.status_code == 200:
                    print(f"Found: {full_url}")
                if verbose:
                    print(f"Checked: {full_url} - Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to {full_url}: {e}")

    # Split wordlist into chunks and run in threads
    chunk_size = len(directories) // threads
    threads_list = []
    for i in range(0, len(directories), chunk_size):
        chunk = directories[i:i + chunk_size]
        t = threading.Thread(target=worker, args=(chunk,))
        t.start()
        threads_list.append(t)

    # Wait for all threads to finish
    for t in threads_list:
        t.join()

# Main CLI interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Directory Fuzzing Tool")
    parser.add_argument("url", help="Target URL to fuzz (e.g., http://example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file (e.g., /path/to/wordlist.txt)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode to show all attempts")
    parser.add_argument("-f", "--filter-status", nargs="+", type=int, help="Filter results by status codes (e.g., 200 403 500)")
    parser.add_argument("--headers", nargs="+", help="Custom headers to add to the request (e.g., User-Agent:Test Authorization:Bearer abc123)")
    parser.add_argument("--timeout", type=int, default=5, help="Set request timeout in seconds (default is 5)")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads to use (default is 1)")

    args = parser.parse_args()

    # Prepare custom headers if provided
    headers_dict = None
    if args.headers:
        headers_dict = {}
        for header in args.headers:
            key, value = header.split(":")
            headers_dict[key.strip()] = value.strip()

    # Run the fuzzing tool (with or without threading)
    if args.threads > 1:
        threaded_fuzz(args.url, args.wordlist, args.verbose, args.filter_status, headers_dict, args.timeout, args.threads)
    else:
        fuzz(args.url, args.wordlist, args.verbose, args.filter_status, headers_dict, args.timeout)