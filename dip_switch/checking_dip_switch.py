"""
Checking the functionality of the DIP switch
"""
from typing import (
    List,
    Dict,
    Any
)
from time import sleep
from netmiko import NetmikoTimeoutException

from data import RemoteConnection


def check_for_remote_connection() -> (str | List[Any] | Dict[str, Any]):
    """ Checking remote access via ssh """
    ssh_conn: Any = RemoteConnection().init_conn_session()
    return ssh_conn.send_command('show dipinfo functional')


def dip_ctl() -> None:
    """ Executing a test case """
    print('--- Start Dip-Switch ---')
    sleep(3)
    try:
        print(check_for_remote_connection())
        print(' 30s - OFF Dip-Switch - ')
        sleep(30)
        print('Trying to connect remotely ... ')
        check_for_remote_connection()
    except NetmikoTimeoutException:
        print('Error: Connect time out !')
        print(' 30s - ON Dip-Switch - ')
        sleep(30)
        print(check_for_remote_connection())
