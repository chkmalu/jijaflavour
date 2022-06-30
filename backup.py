from netmiko import ConnectHandler, SCPConn
from getpass import getpass
from datetime import date
import os
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
#get user credentials
user = input('username: ')
password = getpass()

current_date = date.today()
#open list of ip address
with open('device_list') as f:
    device_lst = f.read().splitlines()
#creat backup folder with datetime
folder_name = f'BACKUP@{str(current_date)}'    
make_dir = os.mkdir(f'/home/malu/Documents/BACKUP/{folder_name}')
def BACKUP():
    file_name = f'{device_name}@{str(current_date)}'
    file_path = f'/home/malu/Documents/BACKUP/{folder_name}/{file_name}'
    sh_start = net_con.send_command('show start')
    with open(file_path, 'w+') as f:
        save_file = f.write(sh_start)
    net_con.disconnect()

for ip in device_lst:
    ip_add = ip
    router = {
    'device_type' : 'cisco_ios',
    'ip' : ip_add,
    'username' : user,
    'password' : password
    } 
     
    try:
        net_con = ConnectHandler(**router)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_add)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_add)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_add)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_add)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    get_hostname = net_con.send_command('show run | i hostname')
    hostname, device_name = get_hostname.split()
    print(f'BACKING UP {device_name}')
    BACKUP()
    print('DONE')