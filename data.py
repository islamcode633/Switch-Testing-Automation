"""
The module contains the necessary data for remote connection via ssh/telnet to the switch
Using ipv4/6 protocols
"""

from netmiko import ConnectHandler


class DataToConnecting:
    """
    Contains data, commands, methods for remote connection to the switch via ssh/telnet
    """
    ipv4_switch: str = '192.168.127.253'
    ipv6_switch: str = f'fe80::c1ff:fe81:3133%enp4s0'
    device_type: str = 'cisco_ios'
    username: str = 'admin'
    password: str = 'password'

    @classmethod
    def connect_to_host_using_telnet(cls):
        """ Returns telnet connection """
        return ConnectHandler(
                    device_type=f'{cls.device_type}_telnet',
                    host=cls.ipv4_switch,
                    username=cls.username,
                    password=cls.password
                )

    @classmethod
    def get_command_ssh(cls) -> str:
        """ Command for further connection via ssh """
        return f'sshpass -p {cls.password} ssh -o StrictHostKeyChecking=no {cls.username}@{cls.ipv4_switch}'
