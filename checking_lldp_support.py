"""
This module checks the support of the LLDP protocol in the switch
"""

import sys
from subprocess import run, CalledProcessError

from data import RemoteConnection


def get_lldp_from_client() -> str:
    """ Returns info about Client [ interface, portDescr, mac and etc...] """
    command: list = 'sudo lldpcli show neighbors'.split()
    try:
        raw = run(command, capture_output=True, text=True, check=True, encoding='utf8')
        return ' Client Info:\n' + raw.stdout
    except CalledProcessError:
        print('Command execution error')
        sys.exit()
    except FileNotFoundError:
        print(f'Command {command} not found')
        sys.exit()


def get_lldp_from_switch() -> str:
    """ Returns info about Switch [ local interface, mac, portDescr and etc...] """
    command: str = 'show lldp neighbors'
    try:
        with RemoteConnection().init_conn_session() as ssh_conn:
            return 'Switch Info:\n' + str(ssh_conn.send_command(command))
    except Exception:
        print('NetmikoBaseErrors')
        sys.exit()


if __name__ == '__main__':
    print(get_lldp_from_client() + get_lldp_from_switch())
