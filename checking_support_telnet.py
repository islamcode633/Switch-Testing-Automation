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
    ConnectionException,
    ReadException,
    WriteException,
    NetmikoBaseException
)

from data import RemoteConnection


def main():
    """ Test Case: Telnet Support """
    try:
        tn_connect = RemoteConnection(type_conn='telnet').init_conn_session()
        output: (str | List[Any] | Dict[str, Any]) = tn_connect.send_command('show ip interface')
        if output:
            print(output)
            tn_connect.disconnect()
    except ConnectionException:
        print('Generic exception indicating the connection failed')
    except (ReadException, WriteException):
        print('An error occurred during a read or write operation')
    except NetmikoBaseException:
        print('Possible errors are related with:\n' \
            ' Generic exception indicating the connection failed\n' \
            ' Exception raised for invalid configuration error\n' \
        )
    finally:
        sys.exit()

main()
