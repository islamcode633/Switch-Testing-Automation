"""
The module checks for a return to default settings
"""

import sys
from typing import (
    List,
    Union,
    Any
)
from time import sleep

from data import RemoteConnection
from exceptions import (
    CommandNotFound,
    RequiredVLANNotFound,
    ResetModeNotSelected,
    ShortPeriodOfTimeToConnect
)


def execute_commands(command: Union[str, None] = None,
                    config_commands: Union[List[str], None] = None
                ) -> Any:
    """ Runs commands on the switch """
    if command is not None:
        return ssh_conn.send_command(command)
    if config_commands is not None:
        return ssh_conn.send_config_set(config_commands)

    raise CommandNotFound


def isadded_vlan(output: Any) -> bool:
    """ Check previously created vlan """
    strings: List[str] = str(output).split()
    for string in strings:
        if string == 'VLAN0010':
            return True
    return False


def do_reconnect(short_reset: bool = False,
                long_reset: bool = False,
                wait_for_reconnect: int = 0
            ) -> Any:
    """ Re-establishing SSH connection """
    mode: str = ""
    if short_reset:
        mode = 'Short Reset'
    elif long_reset:
        mode = 'Long Reset'
    else:
        raise ResetModeNotSelected

    if wait_for_reconnect >= 120:
        ssh_conn.disconnect()
        print(f'Connect aborting ... reconnect after {wait_for_reconnect}s Use {mode} !\n')
        sleep(wait_for_reconnect)
        return RemoteConnection().init_conn_session()

    raise ShortPeriodOfTimeToConnect


if __name__ == '__main__':
    try:
        # First init SSH session
        ssh_conn: Any = RemoteConnection().init_conn_session()
        # Output default VLANs interface
        vlans: str = 'show vlan all'
        print(execute_commands(command=vlans))

        config_commands: List[str] = [
                'vlan 10',
                'interface GigabitEthernet 1/1',
                'switchport mode access',
                'switchport access vlan 10'
            ]
        # Set vlan 10
        execute_commands(config_commands=config_commands)

        # Check was added vlan 10
        if isadded_vlan(output=execute_commands(command=vlans)):
            print(execute_commands(command='copy running-config startup-config'))
        else:
            raise RequiredVLANNotFound

        # Re-initiate SSH session after Short reset
        ssh_conn = do_reconnect(short_reset=True, wait_for_reconnect=120)
        print(execute_commands(command=vlans))

        # Re-initiate SSH session after Long reset
        ssh_conn = do_reconnect(long_reset=True, wait_for_reconnect=150)
        print(execute_commands(command=vlans))
    except CommandNotFound:
        print('Сommand was not passed !')
    except RequiredVLANNotFound:
        print('Failed to add VLAN 10 on switch !')
    except ResetModeNotSelected:
        print('One of the reset modes is not selected !')
    except ShortPeriodOfTimeToConnect:
        print('Required time to connect 120 seconds or more !')
    except Exception:
        print('The error may be related to SSH connection using netmiko !')
    finally:
        sys.exit()
