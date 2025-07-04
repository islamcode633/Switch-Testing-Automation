"""
Checking ssh connection support on the switch
"""

import sys
import subprocess
from netmiko.exceptions import (
        NetmikoTimeoutException,
        NetMikoAuthenticationException,
        ReadException,
        NetmikoBaseException
)

from data import DataToConnecting as DtConn
from ssh_service import SSHConnect


def main():
    """ Test case: Support SSH """
    try:
        error = ''
        # BaseConnection
        telnet_connect = DtConn.connect_to_host_using_telnet()

        output: str = SSHConnect.get_info_about_ssh(tn_connect=telnet_connect)
        reuslt: bool = SSHConnect.is_enabled(output=output)

        if not reuslt:
            SSHConnect.activate(tn_connect=telnet_connect)

        ssh_connect: str = DtConn.get_command_ssh()
        subprocess.run(ssh_connect.split(), check=True)

    except NetmikoTimeoutException:
        error = 'SSH session timed trying to connect to the device\n'
    except NetMikoAuthenticationException:
        error = 'SSH authentication exception based on Paramiko AuthenticationException\n'
    except ReadException:
        error = 'General exception indicating an error occurred during a Netmiko read operation\n'
    except NetmikoBaseException:
        error = 'Possible errors are related with:\n' \
                ' Generic exception indicating the connection failed\n' \
                ' Exception raised for invalid configuration error\n' \
                ' General exception indicating an error occurred during a Netmiko write operation\n'
    finally:
        if error:
            sys.stdout.write(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
