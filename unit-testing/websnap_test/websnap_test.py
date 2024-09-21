import subprocess
import os

# Define the command as a list
script_path = r'../../src/main.py'
command = ['python3', script_path, 'websnap','-f','urls.txt']

try:
    # Execute the command
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    
    # Print the output and any errors
    print("Output:", result.stdout)
    print("Errors:", result.stderr)

except subprocess.CalledProcessError as e:
    print("An error occurred:", e)
    print("Return code:", e.returncode)
    print("Output:", e.stdout)
    print("Errors:", e.stderr)

except FileNotFoundError:
    print(f"Error: The script '{script_path}' was not found.")

except Exception as e:
    print("An unexpected error occurred:", e)