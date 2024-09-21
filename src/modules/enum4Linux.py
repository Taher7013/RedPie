import os
import platform
import socket
import psutil

def get_system_info():
    info = {
        'OS': platform.system(),
        'OS Version': platform.version(),
        'Architecture': platform.architecture(),
        'Machine': platform.machine(),
        'Node Name': platform.node(),
        'Processor': platform.processor(),
        'CPU Cores': psutil.cpu_count(logical=False),
        'Logical CPUs': psutil.cpu_count(logical=True),
        'Memory': f'{psutil.virtual_memory().total / (1024 ** 3):.2f} GB',
        'Uptime': f'{psutil.boot_time()} (timestamp)'
    }
    return info

def get_network_interfaces():
    interfaces = {}
    for iface_name, iface_addrs in psutil.net_if_addrs().items():
        iface_info = []
        for addr in iface_addrs:
            iface_info.append({
                'Address': addr.address,
                'Netmask': addr.netmask,
                'Broadcast': addr.broadcast
            })
        interfaces[iface_name] = iface_info
    return interfaces

def get_installed_packages():
    packages = []
    if os.path.exists('/usr/bin/dpkg'):
        # For Debian-based systems
        result = os.popen('dpkg -l').read()
        lines = result.split('\n')[5:]  # Skip header lines
        for line in lines:
            if line:
                parts = line.split()
                packages.append(parts[1])
    elif os.path.exists('/usr/bin/rpm'):
        # For RPM-based systems
        result = os.popen('rpm -qa').read()
        packages = result.split('\n')
    else:
        packages = ['Package manager not detected']
    return packages

def main():
    print("System Information:")
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")
    
    print("\nNetwork Interfaces:")
    network_interfaces = get_network_interfaces()
    for iface, addrs in network_interfaces.items():
        print(f"\nInterface: {iface}")
        for addr in addrs:
            print(f"  Address: {addr['Address']}")
            print(f"  Netmask: {addr['Netmask']}")
            print(f"  Broadcast: {addr['Broadcast']}")
    
    print("\nInstalled Packages:")
    packages = get_installed_packages()
    for package in packages:
        print(package)

if __name__ == '__main__':
    main()