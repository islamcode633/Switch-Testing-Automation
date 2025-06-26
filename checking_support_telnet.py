"""
Checking Telnet Protocol Support
"""

from typing import (
    List,
    Dict,
    Any
)
import sys
from netmiko.exceptions import (
        NetmikoTimeoutException,
        NetMikoAuthenticationException,
        ReadException,
        NetmikoBaseException
)


from data import DataToConnecting as DTConn


def main():
    """ Test Case: Telnet Support """
    try:
        error: str = ''
        # BaseConnection
        tn_connect = DTConn.connect_to_host_using_telnet()

        output: (str | List[Any] | Dict[str, Any]) = tn_connect.send_command('show ip interface')
        if output:
            sys.stdout.write(str(output) + '\n')
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

main()
