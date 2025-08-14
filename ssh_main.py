"""
Checking SSH connection support on the Switch
"""

import sys
from time import sleep
from netmiko.exceptions import (
        NetmikoTimeoutException,
        NetMikoAuthenticationException,
        ReadException,
        WriteException,
        NetmikoBaseException
)

from data import RemoteConnection
from ssh_service import SSHConnect


def main():
    """ Test case: Support SSH """
    try:
        with RemoteConnection(type_conn='telnet').init_conn_session() as tn_connect:
            output: str = SSHConnect.get_info_about_ssh(tn_connect=tn_connect)
            reuslt: bool = SSHConnect.is_enabled(output=output)
            if not reuslt:
                SSHConnect.activate(tn_connect=tn_connect)

        sleep(5)
        with RemoteConnection().init_conn_session() as ssh_connect:
            print(ssh_connect.send_command('show ip interface'))

    except NetmikoTimeoutException:
        print('SSH session timed trying to connect to the device')
    except NetMikoAuthenticationException:
        print('SSH authentication exception based on Paramiko AuthenticationException')
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
    main()
