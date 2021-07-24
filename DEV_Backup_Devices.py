from paramiko import AuthenticationException
from netmiko import ConnectHandler, NetMikoAuthenticationException

import td_automation
import json
import threading
import logging

# creating log settings
logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='mylog.log',level=logging.INFO)


def backup(net_device: dict):
    try:
        logging.info(f'connecting to {net_device["host"]}')
        con = ConnectHandler(**net_device)
        hostname = td_automation.get_hostname(con)

        # creating backup file and grabbing hostname
        filename = td_automation.create_backup_file(con)

        # entering enable mode on the router and getting running config
        con.enable()
        output = con.send_command('show run')

        # writing running config to backup file
        with open(filename, 'w') as b:
            b.write(output)
            logging.info(f'backup created for {hostname} | {net_device["host"]}!')
        logging.info(f'closing connection to {hostname} | {net_device["host"]}...')
        con.disconnect()

    # log errors that might come up
    except (AttributeError, ConnectionRefusedError) as e:
        logging.error(e)
    except (NetMikoAuthenticationException, AuthenticationException) as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)


with open("net_devices.json", 'r') as f:
    j = json.load(f)

# go through devices and add them to threads
threads = []
for device in j:

    # decode string from json
    decoded_str = td_automation.decode_string(device['password'])

    # create new object to give to thread
    net_device = {
        'device_type': device['device_type'],
        'host': device['host'],
        'username': device['username'],
        'password': decoded_str,
        'port': device['port'],
        'secret': device['secret'],
    }

    # for debugging
    # print(net_device)

    th = threading.Thread(target=backup, args=(net_device,))
    threads.append(th)

for th in threads:
    th.start()

for th in threads:
    th.join()
