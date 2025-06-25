"""
Checking ipv4/6 protocol support
"""

import sys
import subprocess
from netmiko import BaseConnection, ConnectHandler

# FIX import error
from data import DEVICE_TYPE, USERNAME, PASSWORD


# Label: global_task.txt
def checking_presence_argument() -> str:
    """ Check for IP presence address. """
    try:
        return sys.argv[1]
    except IndexError:
        sys.exit('IP address not specified !')


def check_ip_protocol_version(host: str) -> tuple[str]:
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

    return clear_ip_stat, show_ip_stat, ping


class Switch(BaseConnection):
    """
    Initializes the ssh connection and
    checks whether IP protocol versions 4/6 are supported.
    """
    def __init__(
                self,
                device_type: str,
                host: str,
                username: str,
                password: str
            ) -> None:
        try:
            self.device_type = device_type
            self.host = host
            self.username = username
            self.password = password
            self.ssh_session = ConnectHandler(device_type=self.device_type, ip=self.host,
                                username=self.username, password=self.password
                                )
        except Exception as e:
            sys.exit(e)

        self.clear_ip_stat, self.show_ip_stat, self.ping = check_ip_protocol_version(host=self.host)

    def clear_ip_statistics(self) -> None:
        """ Сlears statistics of transmitted packets. """
        self.ssh_session.send_command(self.clear_ip_stat)

    def output_ip_statistics(self) -> None:
        """ Displays current statistics of transmitted packets. """
        sys.stdout.write(self.ssh_session.send_command(self.show_ip_stat) + '\n')

    def icmp_request(self) -> None:
        """ Checking support protocol IP version 4/6. """
        subprocess.run(args=self.ping.split(), check=True)


# Label: put in main()
def test_case_control():
    """ Controlling flow of execution. """
    nm800 = Switch(device_type=DEVICE_TYPE, host=checking_presence_argument(), username=USERNAME, password=PASSWORD)

    nm800.clear_ip_statistics()
    nm800.output_ip_statistics()
    nm800.icmp_request()
    nm800.output_ip_statistics()

    # release of allocated resources
    nm800.ssh_session.cleanup()


if __name__ == '__main__':
    test_case_control()
