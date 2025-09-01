"""
Checking Telnet Protocol Support
"""

from typing import (
    List,
    Dict,
    Any
)
from time import sleep

from exceptions import ConnectTimeOut
from data import RemoteConnection


def telnet_ctl() -> (str | List[Any] | Dict[str, Any]):
    """ Control of test execution flow """
    print('--- Start Telnet ---')
    sleep(3)
    with RemoteConnection(type_conn='telnet').init_conn_session() as tn_connect:
        output: (str | List[Any] | Dict[str, Any]) = tn_connect.send_command('show ip interface')
        if output:
            return output
    raise ConnectTimeOut('Connection timed out !')
