"""
CLI for managing test scripts
Catch common exceptions
"""

import sys
from typing import Any
from argparse import ArgumentParser

# General exceptions
# for all test cases using netmiko interface
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetMikoAuthenticationException,
    ConnectionException,
    ReadException,
    WriteException,
    NetmikoBaseException
)
# Private exceptions raised in test cases
from exceptions import (
    ConnectTimeOut,
    CommandNotFound,
    RequiredVLANNotFound,
    ResetModeNotSelected,
    ShortPeriodOfTimeToConnect,
    HostNotAvailable
)

from lldp.checking_lldp_support import lldp_ctl
from telnet.checking_telnet_support import telnet_ctl
from ssh.checking_ssh_support import ssh_ctl
from reset_button.reset_to_default_settings import reset_ctl
from ipv4_6_support.check_ipv_protocol_support import ipv4_6_ctl
from dip_switch.checking_dip_switch import dip_ctl
from displaying_netport.display_netports_activity import net_ports_ctl


def parser() -> Any:
    """ Parsing command line arguments """
    parse: Any = ArgumentParser()
    # validate flags
    parse.add_argument('--all', action='store_true',
                       help='Run all Test-Cases')
    parse.add_argument('--lldp', action='store_true',
                       help='Print neighbor information')
    parse.add_argument('--telnet', action='store_true',
                       help='Test Telnet connection')
    parse.add_argument('--ssh', action='store_true',
                       help='Test SSH connection')
    parse.add_argument('--reset', action='store_true',
                       help='Test Reset settings to default')
    parse.add_argument('--ipv', action='store_true',
                       help='Checking ipv4/6 protocol support')
    parse.add_argument('--dip', action='store_true',
                       help='Checking the functionality of the DIP switch')
    parse.add_argument('--ports', action='store_true',
                       help='Check the switch network port indicator')
    return parse.parse_args()


def run() -> None:
    """ Run all or specified tests """
    prefix_err_msg: str = '\nError msg: '
    try:
        try:
            args: Any = parser()
            if args.all:
                print(func() for func in [ 
                                    lldp_ctl, telnet_ctl,
                                    ssh_ctl, reset_ctl,
                                    ipv4_6_ctl, dip_ctl,
                                    net_ports_ctl
                                ]
                            )
            else:
                if args.lldp:
                    print(lldp_ctl())
                if args.telnet:
                    print(telnet_ctl())
                if args.ssh:
                    print(ssh_ctl())
                if args.reset:
                    reset_ctl()
                if args.ipv:
                    ipv4_6_ctl()
                if args.dip:
                    dip_ctl()
                if args.ports:
                    net_ports_ctl()
        except ConnectTimeOut as e:
            print(f'Module: checking_telnet_support Func: telnet_ctl()\
                  {prefix_err_msg} {e}')
        except CommandNotFound as e:
            print(f'Module: reset_to_default_settings Func: execute_commands() \
                  {prefix_err_msg} {e}')
        except RequiredVLANNotFound as e:
            print(f'Module: reset_to_default_settings Func: reset_ctl() \
                  {prefix_err_msg} {e}')
        except ResetModeNotSelected as e:
            print(f'Module: reset_to_default_settings Func: do_reconnect() \
                  {prefix_err_msg} {e}')
        except ShortPeriodOfTimeToConnect as e:
            print(f'Module: reset_to_default_settings Func: do_reconnect() \
                  {prefix_err_msg} {e}')
        except HostNotAvailable as e:
            print(f'Module: display_netports_activity Func: net_ports_ctl() \
                  {prefix_err_msg} {e}')

    except NetmikoTimeoutException:
        print('SSH session timed trying to connect to the device')
    except NetMikoAuthenticationException:
        print('SSH authentication exception based on Paramiko AuthenticationException')
    except ConnectionException:
        print('Generic exception indicating the connection failed')
    except (ReadException, WriteException):
        print('An error occurred during a read or write operation')
    except NetmikoBaseException:
        print('Possible errors are related with:\n' \
                ' Generic exception indicating the connection failed\n' \
                ' Exception raised for invalid configuration error\n' \
                ' General exception indicating an error occurred during a Netmiko write operation\n'
            )
    finally:
        sys.exit()


if __name__ == '__main__':
    run()
