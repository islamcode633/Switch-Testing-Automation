"""
The module checks the indication of the switch network ports
"""

import sys
import subprocess
from time import sleep

#FIX import err from module data

# Label: global_task.txt
def checking_presence_argument() -> str:
    """ Check for IP presence address. """
    try:
        return sys.argv[1]
    except IndexError:
        try:
            from data import IPV4_SWITCH
            sys.stdout.write(f'IP default: {IPV4_SWITCH}\n')
            return IPV4_SWITCH
        except ModuleNotFoundError:
            raise ModuleNotFoundError('Module [ data ] was not found in the catalog !')
        except ImportError:
            raise ImportError('Name IPV4_SWITCH not found in module [ data ] !')


def checking_bridge_settings() -> bool:
    """ Gets information about the virtual network bridge configuration. """
    eth_interfaces = subprocess.check_output(args='ip -br a'.split(), encoding='utf-8').split()
    if 'br0' in eth_interfaces:
        link_status = eth_interfaces[eth_interfaces.index('br0') + 1]
        ip_addr_with_netmask = eth_interfaces[eth_interfaces.index('br0') + 2]
        if link_status == 'UP' and ip_addr_with_netmask == '192.168.127.200/24':
            return True

    return False


def checking_switch_availability(host: str) -> bool:
    """ Checks the availability of the switch. """
    status_code = subprocess.run(args=f'ping -c 4 {host}'.split(), check=True)
    if not status_code.returncode:
        sys.stdout.write('\n--- Running the test ! \n')
        sleep(10)
        return True

    return False


def generate_icmp_packets(host: str) -> None:
    """ Generates icmp network packets to send them to switch ports. """ 
    subprocess.run(args=['ping', host], check=True)


# Label: put in main()
def test_case_control() -> None:
    """ Controlling flow of execution. """
    ipv4 = checking_presence_argument()
    if checking_bridge_settings() and checking_switch_availability(host=ipv4):
        while True:
            generate_icmp_packets(host=ipv4)


if __name__ == '__main__':
    test_case_control()
