"""
Checking SSH connection support on the Switch
"""

from typing import (
    List,
    Dict,
    Any
)
from time import sleep

from data import RemoteConnection


class SSHConnect():
    """
    Provides services for activation/deactivation
    and verification of connections via ssh.
    """
    @staticmethod
    def is_enabled(output: str) -> bool:
        """ Checking ssh connection activity """
        can_active: str = 'enabled'
        return can_active in output

    @staticmethod
    def get_info_about_ssh(tn_connect) -> str:
        """ Get information about the presence of a connection via ssh """
        mode: str = 'do show ip ssh'
        output: str = tn_connect.send_command(mode).split()
        return output

    @staticmethod
    def activate(tn_connect) -> None:
        """ Activate ssh connection """
        enable_ssh_connection: list[str] = ['ip ssh']
        tn_connect.send_config_set(enable_ssh_connection)

    @staticmethod
    def deactivate(tn_connect) -> None:
        """ Deactivate ssh connection """
        disable_ssh_connection: list[str] = ['no ip ssh']
        tn_connect.send_config_set(disable_ssh_connection)


def ssh_ctl() -> (str | List[Any] | Dict[str, Any] | None):
    """ Control of test execution flow """
    print('--- Start SSH ---')
    sleep(3)
    with RemoteConnection(type_conn='telnet').init_conn_session() as tn_connect:
        output: str = SSHConnect.get_info_about_ssh(tn_connect=tn_connect)
        reuslt: bool = SSHConnect.is_enabled(output=output)
        if not reuslt:
            SSHConnect.activate(tn_connect=tn_connect)

    with RemoteConnection().init_conn_session() as ssh_connect:
        return ssh_connect.send_command('show ip interface')

    return None
