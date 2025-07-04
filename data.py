"""
The module contains the necessary data for remote connection via ssh/telnet to the switch
Using ipv4/6 protocols
"""

from netmiko import ConnectHandler


class RemoteConnection:
    """
    Contains data, commands, methods for remote connection to the switch via ssh/telnet
    """
    def __init__(self):
        self.ipv4_switch: str = '192.168.127.253'
        self.ipv6_switch: str = f'fe80::c1ff:fe81:3133%enp4s0'
        self.device_type: str = 'cisco_ios'
        self.username: str = 'admin'
        self.password: str = 'password'

    def connect_to_host_using_telnet(self, new_ipaddr=None):
        """ Returns telnet connection """
        if new_ipaddr:
            self.ipv4_switch: str = new_ipaddr
        return ConnectHandler(
                    device_type=f'{self.device_type}_telnet',
                    host=self.ipv4_switch,
                    username=self.username,
                    password=self.password
                )

    def get_command_ssh(self) -> str:
        """ Command for further connection via ssh """
        return f'sshpass -p {self.password} ssh -o StrictHostKeyChecking=no {self.username}@{self.ipv4_switch}'
