"""
The module checks for a return to default settings
"""

from typing import (
    List,
    Union,
    Any,
    Callable
)
from time import sleep

from data import RemoteConnection
from exceptions import (
    CommandNotFound,
    RequiredVLANNotFound,
    ResetModeNotSelected,
    ShortPeriodOfTimeToConnect
)


def run_commands_context_conn_session(ssh_conn: Any = "") -> Callable:
    """ Executing commands in a specific connection session """
    def execute_commands(command: Union[str, None] = None,
                        config_commands: Union[List[str], None] = None
                    ) -> Any:
        """ Runs commands on the switch """
        if command is not None:
            return ssh_conn.send_command(command)
        if config_commands is not None:
            return ssh_conn.send_config_set(config_commands)
        raise CommandNotFound('Сommand was not passed !')
    return execute_commands


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
            ) -> None:
    """ Re-establishing SSH connection """
    mode: str = ""
    if short_reset:
        mode = 'Short Reset'
    elif long_reset:
        mode = 'Long Reset'
    else:
        raise ResetModeNotSelected('One of the reset modes is not selected !')

    if wait_for_reconnect >= 120:
        print(f'Connect aborting ... reconnect after {wait_for_reconnect}s Use {mode} !\n')
        sleep(wait_for_reconnect)
    else:
        raise ShortPeriodOfTimeToConnect('Required time to connect 120 seconds or more !')


def reset_ctl():
    """ Control of test execution flow """
    print('--- Start Reset ---')
    try:
        # First init SSH session
        with RemoteConnection().init_conn_session() as ssh_conn:
            execute_commands = run_commands_context_conn_session(ssh_conn=ssh_conn)
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
                raise RequiredVLANNotFound('Failed to add VLAN 10 on switch !')

        do_reconnect(short_reset=True, wait_for_reconnect=120)
        with RemoteConnection().init_conn_session() as ssh_conn:
            # Re-init SSH session after Short reset
            execute_commands = run_commands_context_conn_session(ssh_conn=ssh_conn)
            print(execute_commands(command=vlans))

        do_reconnect(long_reset=True, wait_for_reconnect=150)
        with RemoteConnection().init_conn_session() as ssh_conn:
            # Re-init SSH session after Long reset
            execute_commands = run_commands_context_conn_session(ssh_conn=ssh_conn)
            print(execute_commands(command=vlans))
    except CommandNotFound as e:
        print(e)
    except RequiredVLANNotFound as e:
        print(e)
    except ResetModeNotSelected as e:
        print(e)
    except ShortPeriodOfTimeToConnect as e:
        print(e)
