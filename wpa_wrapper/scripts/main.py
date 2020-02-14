# Comments included btw
import os
import subprocess

networks = []
ssids = []
passwords = []
encryptions = []

# Get interface name from file or from user
try:
    interfacefile = open("interface", "r")
    interface = interfacefile.readline()
except:
    print("Please input interface name:")
    interface = str(input("> "))
    os.system("echo {} > interface".format(interface))

interface = interface.replace("\n", "")

# Clear screen
def clear():
    os.system('clear')

# Create list
def makelist():
    os.system('ls ../networks > netlist.txt')
    netlist = open("netlist.txt", "r")

    # Read network numbers
    current = str('0')
    while current != '':
        current = str(netlist.readline())
        current = current.replace("\n", "") 
        networks.append(current)

    # Get ssids and passwords from files
    networks.remove('')
    for network in networks:
        netfile = open("../networks/{}".format(network), "r")
        ssid = netfile.readline()
        ssid = ssid.replace("\n", "")
        password = netfile.readline()
        password = password.replace("\n", "")
        encryption = netfile.readline()
        encryption = encryption.replace("\n", "")
        ssids.append(ssid)
        passwords.append(password)
        encryptions.append(encryption)


# Input/output
clear()
print("Welcome to CuBeRJAN3's WPA supplicant wrapper!\n")
# Print network card state
statel = str(subprocess.check_output('ip link show | grep {}'.format(interface), shell=True)) 
if 'UP' in statel:
    state = 'on'
else:
    state = 'off'
print("Interface {} is currently {}".format(interface, state))
os.system("iw {} info | grep ssid > current.txt".format(interface))
currentf = open("current.txt", "r")
currl = currentf.readline()
# Check for connection + SSID
if 'ssid' not in currl:
    print("Interface {} is not currently connected.\n".format(interface))
else:
    currl = currl.replace("	ssid ", "")
    currl = currl.replace("\n", "")
    print("Interface {} is currently connected to '{}'\n".format(interface, currl))

print("Options: -2 Refresh\n         -1. Toggle interface state\n          0. Exit\n          1. Connect to a network\n          2. Delete a known network\n          3. Delete all known networks\n          4. Clear all config\n\n")
option = str(input("> "))

# Toggle state
while option == '-1':
    if state == 'on':
        os.system("rfkill block wlan;ip link set {} down;iw {} set power_save on;killall wpa_supplicant".format(interface,interface))
    else:
        os.system("rfkill unblock wlan;ip link set {} up;iw {} set power_save off;killall wpa_supplicant;wpa_supplicant -i {} -B -c ../conf/wpa_supplicant-{}.conf".format(interface,interface,interface,interface))
    option = 'exit'

# Option one
while option == '1':
    makelist()
    if state == 'off':
        os.system("rfkill unblock wlan;ip link set {} up;iw {} set power_save off".format(interface,interface))
    print("Choose a network:\n")

    # Print network list
    print("-1. Scan for networks")
    print("0. New network")
    for network in networks:
        print("{}. {}  [{}]".format(networks[int(network)-1], ssids[int(network)-1], encryptions[int(network)-1]))
    print("\n\n")

    # Get SSID and password
    input1 = str(input("> "))
    # If creating a new network
    if input1 == '0':
        print("Input network SSID:\n\n")
        ssid = str(input("> "))
        os.system("echo {} > ../networks/{}".format(ssid, len(networks)+1))
        print("Network encryption (wep, wpa or open):\n\n")
        encryption = str(input("> "))
        if encryption in ("wep", "wpa"):
            print("Input network password (will not echo):\n\n")
            os.system("stty -echo")
            password = str(input("> "))
            os.system("stty echo")
            if password == '':
                password = str("none")
        if encryption == 'open':
            password = str("none")
        if encryption in ("wep", "wpa"):
            os.system("echo {} >> ../networks/{}".format(password, len(networks)+1))
            os.system("echo {} >> ../networks/{}".format(encryption, len(networks)+1))
        if encryption not in ("wep", "wpa", "open"):
            print("Invalid input")
            option = 'exit'
    # If scanning
    elif input1 == '-1':
        print("\n\n")
        print("Please wait a moment...\n\n")
        # Scan with output into file
        os.system("iw {} scan | grep SSID > lastscan.txt".format(interface))
        scanned = open("lastscan.txt", "r")
        scanned_str = str('0')
        scanned_ls = []
        # Modify returned string and append to list
        while scanned_str != '':
            scanned_str = scanned.readline()
            scanned_str = scanned_str.replace("	SSID: ", "")
            scanned_str = scanned_str.replace("\n", "")
            scanned_ls.append(scanned_str)
        # Remove empty from list
        scanned_ls.remove('')
        # Print output
        print("Choose a network:\n\n")
        int_entry = 1
        for entry in scanned_ls:
            print("{}. {}".format(int_entry, entry))
            int_entry += 1
        # Take input
        scanned_inp = str(input("> "))
        # Check for integer
        try:
            scanned_inp = int(scanned_inp)
        except:
            print("Invalid input")
            option = 'exit'

        # Check if in list
        if int(scanned_inp) > 0 and (int(scanned_inp) < len(scanned_ls)+1):
            ssid = scanned_ls[scanned_inp-1]
            print("Encryption (wep/wpa/open):")
            encryption = str(input("> "))
            if encryption != 'open':
                print("Network password (will not echo):\n")
                os.system("stty -echo")
                password = str(input("> "))
                os.system("stty echo")
            else:
                password=str('none')
            os.system("echo {} > ../networks/{}".format(ssid, len(networks)+1))
            os.system("echo {} >> ../networks/{}".format(password, len(networks)+1))
            os.system("echo {} >> ../networks/{}".format(encryption, len(networks)+1))
        else:
            print("Invalid input")
            option = 'exit'

    # If connecting to known network
    else:
        # Check if input1 matches a network number
        if (input1 in networks):
            ssid = ssids[int(input1)-1]
            password = passwords[int(input1)-1]
            encryption = encryptions[int(input1)-1]
        else:
            print("Invalid input")
            option = 'exit'

    # if connecting to wep
    if encryption == 'wep':
        os.system("echo {} > wep_ssid".format(ssid))
        os.system("echo {} > wep_pass".format(password))
        os.system("rfkill block wlan;ip link set {} down;iw {} set power_save on;killall wpa_supplicant".format(interface,interface))
        os.system("iwconfig {} ap any;iwconfig {} essid {};iwconfig {} key s:'{}';iwconfig {} enc on;ip link set {} up;dhclient {}".format(inteface,interface,ssid,interface,password,interface,interface,interface))
    # If connecting to wpa
    if encryption == 'wpa' or encryption == 'open':

        # Create temprorary template
        os.system("cp ../template/wpa_supplicant temp.conf")

        # Write network info
        configfile = open("temp.conf", "a")
        configfile.write('    ssid="{}"\n'.format(ssid))
        if password == 'none':
            password = ''
            configfile.write("    key_mgmt=NONE")
        else:
            configfile.write('    psk="{}"\n'.format(password))
        configfile.write("""}""")
        configfile.close()

        # Replace existing config file
        os.system('rm -rf ../conf/wpa_supplicant-{}.conf;cp temp.conf ../conf/wpa_supplicant-{}.conf'.format(interface,interface))
        os.system("rfkill unblock wlan;ip link set {} up;iw {} set power_save off;killall wpa_supplicant;wpa_supplicant -i {} -B -c ../conf/wpa_supplicant-{}.conf".format(interface,interface,interface,interface))

        # Chmod network info
        os.system('chmod -rwx ../networks/*')

        option = 'exit'

# Option two
while option == '2':
    makelist()
    if len(networks) > 1 or len(networks) == 1:
        print("Choose a network:\n")

        # Print network list
        for network in networks:
            print("{}. {}".format(networks[int(network)-1], ssids[int(network)-1]))
        print("\n\n")

        input1 = str(input("> "))

        # Check if input1 matches a network number
        if (input1 in networks):
            os.system("rm -rf ../networks/{}".format(input1))
        else:
            print('Invalid input')
            option = 0

        # Update list (if there is more than 1 network)
        if len(networks) > 1:
            os.system("n=1;for file in ../networks/*;do mv ../networks/$file ../networks/$n;n=((n+1));done")

        option = '0'

    # If there are no networks
    else:
        print("No known networks")
    option = 0

while option == '3':
    os.system("rm -rf ../networks/*")
    option = 'exit'

while option == '4':
    os.system("rm -rf interface;rm -rf current.txt;rm -rf lastscan.txt;rm -rf netlist.txt;touch netlist.txt;rm -rf state.txt;rm -rf temp.conf;rm -rf ../conf/*")
    option = 'exit'

if option == '0':
    os.system("rm -rf netlist.txt;rm -rf current.txt;rm -rf lastscan.txt;rm -rf temp.conf;rm -rf state.txt")
    clear()

if option not in ("-1", "0", "1", "2", "3", "4"):
    os.system("rm -rf netlist.txt;rm -rf current.txt;rm -rf lastscan.txt;rm -rf temp.conf;rm -rf state.txt")
    clear()
    os.system("python3 main.py")

# If option not valid
else:
    print("")
