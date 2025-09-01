"""
The module checks the indication of the switch network ports
"""

import subprocess
from time import sleep

from exceptions import HostNotAvailable


def checking_switch_availability(host: str) -> bool:
    """ Checks the availability of the switch. """
    ping: list[str] = f'ping -c 4 {host}'.split()
    status_code: int = subprocess.run(ping, check=True).returncode
    if not status_code:
        sleep(10)
        return True

    return False


def generate_icmp_packets(host: str) -> None:
    """ Generates icmp network packets to send them to switch ports. """
    ping: list[str] = f'ping {host}'.split()
    subprocess.run(ping, check=True)


def net_ports_ctl() -> None:
    """ Controlling flow of execution. """
    print('--- Start DispPortActivity ---\n' \
        'terminate the script [ CTRL + C ]\n')
    sleep(3)
    try:
        ipaddr: str = '192.168.127.253'
        if checking_switch_availability(host=ipaddr):
            while True:
                generate_icmp_packets(host=ipaddr)
        raise HostNotAvailable('Host not available !')
    except KeyboardInterrupt:
        # Not Error
        print('\nKeyboard interruption of script execution !')
