# NetworkToolbelt
This is a collection of common scripts I haved used consistently for network automation.

## DEV_Backup_Devices
This script will take in the net_devices.json file and use the information in the JSON file to backup all devices and place them in a file share.

## net_devices
This contains an array of network device objects that are used in the DEV_Backup_Devices script. 

## Find_MAC_Address
This will have the user input a mac address and search for it in the mac address table on the switch. This is useful when you know hte mac address of the device and need to know which interface it is plugged into along with other information.

## mynetmiko
this is a helper python file with useful functions that are used in the DEV_Backup_Devices script.

## td_automation
this is another helper file that contains functions that are used in the DEV_Backup_Devices script.
