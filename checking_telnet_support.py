"""
Checking Telnet Protocol Support
"""

from typing import (
    List,
    Dict,
    Any
)

from data import RemoteConnection


def telnet_ctl() -> (str | List[Any] | Dict[str, Any] | None):
    """ Control of test execution flow """
    print('--- Start Telnet ---')
    with RemoteConnection(type_conn='telnet').init_conn_session() as tn_connect:
        output: (str | List[Any] | Dict[str, Any]) = tn_connect.send_command('show ip interface')
        if output:
            return output

        return None
