from netmiko import ConnectHandler
import datetime
import logging


def backup_config(json: list):
    try:
        for device in json:
            # create connection to the network device
            print(f'connecting to {device["host"]}')
            con = ConnectHandler(**device)

            # build string to save to a location and name the file
            month = datetime.date.today()
            find_hostname = con.find_prompt()  # this will print >device_host_name
            parse_hostname = find_hostname.replace(">", "")  # remove the greater than and we can get the hostname
            s = f'//root/it/folder/Route_switch_backups/{month}-BACKUP-{parse_hostname}.txt'  # creates filename of backup

            # "open" the file we are about to create above
            with open(s, 'w') as f:
                # need to input enable mode before performing show run
                con.enable()
                out = con.send_command('show run')  # get running config
                f.write(out)
            print(f'file saved for device {device["host"]}')
            print(f'Disconnecting from {device["host"]}')
            con.disconnect()
    except Exception as e:  # catch any errors that occur
        logging.error(e)
        print(e)
