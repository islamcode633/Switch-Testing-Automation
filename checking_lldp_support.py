"""
This module checks the support of the lldp protocol in the switch
"""

import sys
from subprocess import run, CalledProcessError

from data import RemoteConnection


def get_lldp_from_client() -> str:
    """ Returns info about Client [ interface, portDescr, mac and etc...] """
    cmd: list = 'sudo lldpcli show neighbors'.split()
    err: str = ''
    try:
        raw = run(cmd, capture_output=True, text=True, check=True, encoding='utf8')
    except CalledProcessError as e:
        err = f'Command execution error {e} !'
    except FileNotFoundError as e:
        err = 'Command {e} not Found !'
    finally:
        if err:
            sys.exit(err)
        return ' Client Info:\n' + raw.stdout


def get_lldp_from_switch() -> str:
    """ Returns info about Switch [ local interface, mac, portDescr and etc...] """
    cmd: str = 'show lldp neighbors'
    err: str = ''
    try:
        ssh_conn = RemoteConnection().init_conn_session()
    except Exception:
        err = f'NetmikoBaseErrors !'
    finally:
        if err:
            sys.exit(err)
        return 'Switch Info:\n' + str(ssh_conn.send_command(cmd))


def main():
    sys.stdout.write(get_lldp_from_client() + get_lldp_from_switch())


main()
