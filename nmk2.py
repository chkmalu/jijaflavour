from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

username = input('Enter your SSH username: ')
password = getpass()

with open('sw_config.cfg') as f:
    commands_list_switch = f.read().splitlines()

with open('rtr_config.cfg') as f:
    commands_list_router = f.read().splitlines()

with open('device_lst.cfg') as f:
    devices_list = f.read().splitlines()

for devices in devices_list:
    print ('Connecting to device: ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password
    }

    try:
        net_connect = ConnectHandler(**ios_device)
        shrun = net_connect.send_command('show run | i host')
        name,hostname = shrun.split(' ')
        backupfile = '/home/malu/Desktop/inventory.ods'
        dvname = shrun.find('hostname')
        dvname = shrun[dvname:(dvname + 12)]
        showver = net_connect.send_command('show version')
        software = showver.find('Software')
        software = showver[software:(software + 53)]
        print(f"{'backing up'} {hostname}")
        logfile = open(backupfile, 'a')
        logfile.write(dvname)
        logfile.write('\n')
        logfile.write(software)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue
