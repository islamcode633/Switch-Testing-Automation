"""
Checking ipv4/6 protocol support
"""

import subprocess
from time import sleep

from data import RemoteConnection


def check_ip_protocol_version(host: str) -> list[str]:
    """ Сhecking IP address in version 4/6. """
    try:
        for isdigite in host:
            if isdigite == '.':
                continue
            int(isdigite)
        clear_ip_stat = 'clear ip statistics'
        show_ip_stat = 'show ip statistics'
        ping = f'ping -4 -c 10 {host}'
    except ValueError:
        clear_ip_stat = 'clear ipv6 statistics'
        show_ip_stat = 'show ipv6 statistics interface vlan 1'
        ping = f'ping -6 -c 10 {host}'

    return [clear_ip_stat, show_ip_stat, ping]


def clear_ip_statistics(command, ssh_session) -> None:
    """ Сlears statistics of transmitted packets. """
    ssh_session.send_command(command)


def icmp_request(command) -> None:
    """ Checking support protocol IP version 4/6. """
    subprocess.run(command.split(), check=True)


def output_ip_statistics(command, ssh_session) -> None:
    """ Displays current statistics of transmitted packets. """
    print(ssh_session.send_command(command) + '\n')


def ipv4_6_ctl() -> None:
    """ Control of test execution flow """
    print('--- Start IPv4/6 ---')
    sleep(3)
    with RemoteConnection().init_conn_session() as ssh_session:
        nm800 = RemoteConnection()
        clear_ip_stat, show_ip_stat, ping = check_ip_protocol_version(nm800.ipv4_switch)
        clear_ip_statistics(command=clear_ip_stat, ssh_session=ssh_session)
        output_ip_statistics(command=show_ip_stat, ssh_session=ssh_session)
        icmp_request(command=ping)
        output_ip_statistics(command=show_ip_stat, ssh_session=ssh_session)
