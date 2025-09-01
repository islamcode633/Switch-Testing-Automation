"""
This module checks the support of the LLDP protocol in the Switch
"""

from typing import (
    List,
    LiteralString,
    Union
)
from time import sleep
from subprocess import run
from subprocess import CalledProcessError

from data import RemoteConnection


def get_lldp_from_client() -> Union[str, None]:
    """ Returns info about Client [ interface, portDescr, mac and etc...] """
    command: List[LiteralString] = 'sudo lldpcli show neighbors'.split()
    try:
        raw = run(command, capture_output=True, text=True, check=True, encoding='utf8')
        return ' Client Info:\n' + raw.stdout
    except CalledProcessError:
        print('Command execution error')
    except FileNotFoundError:
        print(f'Command {command} not found')

    return None


def get_lldp_from_switch() -> Union[str, None]:
    """ Returns info about Switch [ local interface, mac, portDescr and etc...] """
    command: str = 'show lldp neighbors'
    with RemoteConnection().init_conn_session() as ssh_conn:
        return 'Switch Info:\n' + str(ssh_conn.send_command(command))


def lldp_ctl() -> Union[str, None]:
    """ Control of test execution flow """
    print('--- Start LLDP ---')
    sleep(3)
    client: Union[str, None] = get_lldp_from_client()
    switch: Union[str, None] = get_lldp_from_switch()

    if client and switch:
        return client + switch

    return None
