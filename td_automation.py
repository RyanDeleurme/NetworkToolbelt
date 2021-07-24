import random
import string
import base64
import datetime


def generate_password(length: int):

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    all_strings = lower + upper + num + symbols

    temp = random.sample(all_strings, length)

    password = "".join(temp)

    return password


def encode_string(message: string):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decode_string(message):
    base64_bytes = message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message


def create_backup_file(con):
    month = datetime.date.today()
    find_hostname = con.find_prompt()  # this will print >device_host_name
    parse_hostname = find_hostname.replace(">", "")  # remove the greater than and we can get the hostname
    filename = f'//nwfree/it/Route_switch_backups/{month}-BACKUP-{parse_hostname}.txt'  # creates filename of backup
    return filename


def get_hostname(con):
    find_hostname = con.find_prompt()  # this will print >device_host_name
    parse_hostname = find_hostname.replace(">", "")  # remove the greater than and we can get the hostname
    return parse_hostname
