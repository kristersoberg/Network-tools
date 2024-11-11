#This is probablty the most overengineered ping-script ive seen in a while.
#The script was useful while testing how long a host would be unresponsive to a ping, during an upgrade of firmware.
#The script prompts the user for an IP address to which the script will send 1 icmp ping packet every 10 seconds. 
#The result of the ping will either be "{timestamp} - {IP_ADDRESS} is reachable" or "{timestamp} - {IP_ADDRESS} is unreachable".
#ChatGPT added some functionality to check the OS, this is because the syntax for pinging with 1 packet is different from Linux to Windows. This feature remains untested for now
#The output file will be stored at the same location where the script is ran, and the terminal will print the results as its running.
#If this solved something for you - happy days

import subprocess
import time
from datetime import datetime
import platform

# IP address to ping
IP_ADDRESS = input("IP to ping: ")
# Log file path
LOG_FILE = f"ping_{IP_ADDRESS}log.txt"

# Determine the ping command and parameters based on the OS
if platform.system().lower() == "windows":
    ping_command = ["ping", "-n", "1", IP_ADDRESS]
else:
    ping_command = ["ping", "-c", "1", IP_ADDRESS]

# Write a header to the log file
with open(LOG_FILE, "w") as file:
    file.write(f"Ping test started on {datetime.now()}\n")
    file.write(f"Pinging {IP_ADDRESS} every 10 seconds...\n")
    file.write("-" * 40 + "\n")

# Ping loop
while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Use subprocess to ping and capture output
    try:
        response = subprocess.run(
            ping_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Check the output text for success or failure indicators
        output = response.stdout.lower()
        
        if "request timed out" in output or "destination host unreachable" in output or response.returncode != 0:
            result = f"{timestamp} - {IP_ADDRESS} is unreachable\n"
        else:
            result = f"{timestamp} - {IP_ADDRESS} is reachable\n"
            
    except Exception as e:
        result = f"{timestamp} - Error pinging {IP_ADDRESS}: {e}\n"
    
    # Log the result
    with open(LOG_FILE, "a") as file:
        file.write(result)
    
    # Print the result to the console as well (optional)
    print(result.strip())
    
    # Wait 10 seconds before the next ping
    time.sleep(10)
