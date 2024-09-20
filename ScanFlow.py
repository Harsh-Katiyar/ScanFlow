import subprocess

# Define colors
NC = '\033[0m'  # No Color
BOLD = '\033[1m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Function to check if a command exists
def check_command(command):
    result = subprocess.run(["where", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"{RED}{command} is required but not installed. Aborting.{NC}")
        exit(1)

# Function to display a menu and take user input
def display_menu(prompt, *options):
    print(f"\n{CYAN}{prompt}{NC}")
    for i, option in enumerate(options, 1):
        print(f"{BLUE}{i}: {option}{NC}")
    while True:
        choice = input("Choose an option (or press Enter to skip): ").strip()
        if choice == '':
            return None
        try:
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
            else:
                print(f"{RED}Invalid option. Please select a valid number.{NC}")
        except ValueError:
            print(f"{RED}Please enter a valid number.{NC}")

# Check if nmap is installed
check_command("nmap")

# Start the tool
print(f"{BOLD}{CYAN}Welcome to nmapmate{NC}")
print(f"{YELLOW}This tool helps you scan networks using nmap with custom options.{NC}")

# Step 1: Target Specification
target_choice = display_menu("Target Specification",
    "Scan a single IP",
    "Scan specific IPs",
    "Scan a range of IPs",
    "Scan a domain",
    "Scan using CIDR notation",
    "Scan targets from a file",
    "Exclude listed hosts")

target = None
if target_choice == "Scan a single IP":
    target = input("Enter the IP address (e.g., 192.168.1.1): ").strip()
elif target_choice == "Scan specific IPs":
    target = input("Enter the IP addresses separated by space (e.g., 192.168.1.1 192.168.2.1): ").strip()
elif target_choice == "Scan a range of IPs":
    target = input("Enter the IP range (e.g., 192.168.1.1-254): ").strip()
elif target_choice == "Scan a domain":
    target = input("Enter the domain (e.g., scanme.nmap.org): ").strip()
elif target_choice == "Scan using CIDR notation":
    target = input("Enter the CIDR notation (e.g., 192.168.1.0/24): ").strip()
elif target_choice == "Scan targets from a file":
    target = input("Enter the file path containing targets: ").strip()
    if not target.endswith('.txt'):
        print(f"{RED}Please provide a valid file path.{NC}")
        exit(1)
    target = f"-iL {target}"
elif target_choice == "Exclude listed hosts":
    exclude = input("Enter the IP to exclude (e.g., 192.168.1.1): ").strip()
    target = f"--exclude {exclude}"

# Step 2: Scan Techniques
scan_technique = display_menu("Scan Techniques",
    "-sS: TCP SYN scan (default)",
    "-sT: TCP connect scan (non-root users)",
    "-sU: UDP scan",
    "-sA: TCP ACK scan",
    "-sW: TCP Window scan",
    "-sM: TCP Maimon scan")

# Step 3: Host Discovery
host_discovery = display_menu("Host Discovery",
    "-sL: List scan (no scan, list targets only)",
    "-sn: Disable port scan (ping scan only)",
    "-Pn: No ping (only port scan)",
    "-PS: TCP SYN discovery",
    "-PA: TCP ACK discovery",
    "-PU: UDP discovery",
    "-PR: ARP discovery (local network)")

# Step 4: Port Specification
port_choice = display_menu("Port Specification",
    "Scan a specific port",
    "Scan a range of ports",
    "Scan multiple TCP and UDP ports",
    "Fast scan (100 default ports)",
    "Scan top 2000 ports",
    "Scan all 65535 ports")

port = None
if port_choice == "Scan a specific port":
    port = f"-p {input('Enter the port (e.g., 80): ').strip()}"
elif port_choice == "Scan a range of ports":
    port = f"-p {input('Enter the port range (e.g., 21-100): ').strip()}"
elif port_choice == "Scan multiple TCP and UDP ports":
    port = f"-p {input('Enter multiple ports (e.g., U:53,T:21-25,80): ').strip()}"
elif port_choice == "Fast scan (100 default ports)":
    port = "-F"
elif port_choice == "Scan top 2000 ports":
    port = "--top-ports 2000"
elif port_choice == "Scan all 65535 ports":
    port = "-p-"

# Step 5: Service and Version Detection
version_detection = display_menu("Service and Version Detection",
    "No version detection",
    "-sV: Version detection",
    "--version-intensity: Set intensity level (0-9)")

if version_detection == "--version-intensity: Set intensity level (0-9)":
    intensity = input("Enter version intensity (0-9): ").strip()
    version_detection = f"--version-intensity {intensity}" if intensity.isdigit() and 0 <= int(intensity) <= 9 else None

# Step 6: OS Detection
os_detection = display_menu("OS Detection",
    "No OS detection",
    "-O: Enable OS detection",
    "--osscan-guess: Aggressive OS detection guess",
    "--max-os-tries: Set max number of tries")

if os_detection == "--max-os-tries: Set max number of tries":
    max_tries = input("Enter max number of OS detection tries: ").strip()
    os_detection = f"--max-os-tries {max_tries}" if max_tries.isdigit() else None

# Step 7: Timing and Performance
timing_performance = display_menu("Timing and Performance",
    "-T0: Paranoid (IDS evasion)",
    "-T4: Aggressive (fast)",
    "--max-retries: Set max retry attempts",
    "--min-rate: Set minimum packet rate")

if timing_performance == "--max-retries: Set max retry attempts":
    retries = input("Enter the number of retries: ").strip()
    timing_performance = f"--max-retries {retries}" if retries.isdigit() else None
elif timing_performance == "--min-rate: Set minimum packet rate":
    min_rate = input("Enter minimum packet rate (e.g., 100): ").strip()
    timing_performance = f"--min-rate {min_rate}" if min_rate.isdigit() else None

# Step 8: Firewall/IDS Evasion
firewall_evasion = display_menu("Firewall/IDS Evasion",
    "No firewall evasion",
    "-f: Use tiny fragmented IP packets",
    "--mtu: Set custom offset size",
    "-D: Use decoys",
    "-S: Spoof source IP",
    "--proxies: Use proxies")

if firewall_evasion == "--mtu: Set custom offset size":
    mtu_size = input("Enter MTU size: ").strip()
    firewall_evasion = f"--mtu {mtu_size}" if mtu_size.isdigit() else None
elif firewall_evasion == "-D: Use decoys":
    decoys = input("Enter decoy IPs separated by commas: ").strip()
    firewall_evasion = f"-D {decoys}"
elif firewall_evasion == "-S: Spoof source IP":
    spoofed_ip = input("Enter the spoofed IP address: ").strip()
    firewall_evasion = f"-S {spoofed_ip}"
elif firewall_evasion == "--proxies: Use proxies":
    proxies = input("Enter proxies separated by commas: ").strip()
    firewall_evasion = f"--proxies {proxies}"
else:
    firewall_evasion = None

# Build the final nmap command
nmap_command_parts = [f"nmap"]
if target:
    nmap_command_parts.append(target)
if scan_technique:
    nmap_command_parts.append(scan_technique.split(":")[0])  # Get the actual option, not the description
if host_discovery:
    nmap_command_parts.append(host_discovery.split(":")[0])
if port:
    nmap_command_parts.append(port)
if version_detection:
    nmap_command_parts.append(version_detection.split(":")[0])
if os_detection:
    nmap_command_parts.append(os_detection.split(":")[0])
if timing_performance:
    nmap_command_parts.append(timing_performance.split(":")[0])
if firewall_evasion:
    nmap_command_parts.append(firewall_evasion.split(":")[0])

nmap_command = " ".join(nmap_command_parts)

# Execute the command
print(f"\n{BOLD}{CYAN}Executing the command:{NC} {GREEN}{nmap_command}{NC}")

# Using subprocess to execute the command
result = subprocess.run(nmap_command, shell=True, text=True, capture_output=True)

# Print the output and error messages
print(result.stdout)
print(result.stderr)
