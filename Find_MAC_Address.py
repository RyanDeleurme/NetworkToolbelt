import json
import getpass
import re

from netmiko import NetMikoAuthenticationException
from paramiko import AuthenticationException
from napalm import get_network_driver


def validate_mac_address(mac_add):
    # regex to validate against
    regex = ("^([0-9A-Fa-f]{2}[:-])" +
             "{5}([0-9A-Fa-f]{2})|" +
             "([0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4})$")

    # compile the regex to start the comparison
    p = re.compile(regex)

    # if the string is empty return false
    if mac_add is None:
        return False

    # return if the string matched the regex 01:00:0C:CC:CC:CC
    if re.search(p, mac_add):
        return mac_add
    else:
        # thank you stack overflow
        new_mac = ':'.join(re.findall('..', mac_add))
        return new_mac


try:

    ip_addr = input('Network Device IP: \n')
    password = getpass.getpass('Network Device Password (this is NOT the enable password): \n')
    enable_pass = getpass.getpass('Network Device Enable Password: \n')
    mac_input = input('Enter the mac address you want to find. Format as 01:00:0C:CC:CC:CC or 01000CCCCCCC \n')
    mac_output = validate_mac_address(mac_input)
    print(mac_output)

    # if the method returned False user is not inputting a mac address
    if not mac_output:
        print('Please input a mac address!')
        exit()

    driver = get_network_driver('ios')

    optional = {'secret': enable_pass}
    device = driver(
        hostname=ip_addr,
        username='tda',
        password=password,
        optional_args=optional
    )

    # create connection to the network device
    device.open()

    mac_table = device.get_mac_address_table()
    # print(mac_table)
    dump = json.dumps(mac_table, sort_keys=True, indent=4)
    counter = 0
    new_mac = None

    for m in mac_table:
        if m['mac'] == mac_output:
            # validate if the mac was found and add to variable
            # we do this since if we applied the else loop, whatever we print would print for each value not found
            # and the output would be bloated...
            counter += 1
            new_mac = m

    if counter == 1:
        print('\n')
        print(f'Mac Address:{new_mac["mac"]}')
        print(f'Interface:{new_mac["interface"]}')
        print(f'Vlan:{new_mac["vlan"]}')
        print(f'Static:{new_mac["static"]}')
    else:
        print(f'Mac address {mac_output} was not found. Double check with the full table below.')
        print(dump)

    device.close()

except (AttributeError, ConnectionRefusedError) as e:
    print(e)
except (NetMikoAuthenticationException, AuthenticationException) as e:
    print(e)
except Exception as e:
    print(e)
