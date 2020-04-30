import getpass

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

DEBUG=0

# ask for credentials
username = input ("Username:")
password = getpass.getpass(prompt='Password: ')


#ask for MAC
mac_tofind = input("Please enter MAC address like 0018.bc00.9813: ").lower().strip()
found=0

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = username
nr.inventory.defaults.password = password

int_list = nr.run(task=netmiko_send_command, command_string='show interfaces switchport | i Name|Operational Mode:', use_textfsm=True)
mac_list = nr.run(task=netmiko_send_command, command_string='show mac address-table', use_textfsm=True)

#scan mac-address-table for mac
for device in mac_list:
    for mac in mac_list[device].result:
        #if found - find the corresponding interface
        if mac['destination_address'] == mac_tofind:
            if DEBUG: print(mac)
            for int in int_list[device].result:
                #check the mode is access
                if int['interface'] == mac['destination_port'] and 'access' in int['mode']:
                    print(f"Client with MAC {mac_tofind} was found at {device} interface {int['interface']}")
                    found=1
                    break
if not found:
    print("MAC was not found")

