SSH bruteforce for cheking default passwords on my servers

Command to create targets list:
nmap --open -n -p 22 192.168.1.1/24 | grep open -B 3 | grep -vE "Host|PORT|ssh" | awk '{print $NF}' | grep -v '\-\-' >> targets.lst 
