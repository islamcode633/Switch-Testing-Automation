"""

"""
from typing import (
    List,
    Dict,
    Any
)
from threading import Thread
from time import sleep

from data import RemoteConnection as Connect




def output_ipaddr_of_interface(tn_connect):
    """ """
    print(tn_connect.send_command('show ip interface'))


def conn_first_connect():
    """ """
    tn_connect = Connect()
    return tn_connect.connect_to_host_using_telnet()


def setting_new_ipaddr(tn_connect, ipaddr):
    """ """
    config_commands = [ 'interface vlan 1', f'ip address {ipaddr} 255.255.255.0' ]
    print(tn_connect.send_config_set(config_commands))


def conn_after_change(ipaddr):
    """ """
    new_tn_connect = Connect()
    return new_tn_connect.connect_to_host_using_telnet(ipaddr)


"""
def set_default_settings():
    """  """
    config_commands = [ 'interface vlan 1', f'ip address 192.168.127.253 255.255.255.0' ]

    tn_connect = Connect().connect_to_host_using_telnet('192,168.127.250')
    tn_connect.send_config_set(config_commands)
    print('Default Setting Activated !')    

"""


def main():
    """ """
    telnet_connect = conn_first_connect()
    output_ipaddr_of_interface(tn_connect=telnet_connect)
    sleep(3)

    # try connect at ssh maybe abort connect after change ip addr for connect againe
    # search timeout connect. conn on 30sec after disconnect automation
    ipaddr = '192.168.127.250'
    #setting_new_ipaddr(tn_connect=telnet_connect, ipaddr=ipaddr)
    thread1 = Thread(target=setting_new_ipaddr, args=(telnet_connect, ipaddr))
    thread1.start()
    sleep(30)

    #thread2 = Thread(target=conn_after_change, args=(ipaddr))
    #thread2.start()

    telnet_connect = conn_after_change(ipaddr=ipaddr)
    output_ipaddr_of_interface(tn_connect=telnet_connect)

    #ssh_session.send_command('reload defaults force')


main()
