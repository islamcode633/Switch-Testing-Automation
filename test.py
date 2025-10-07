"""
"""

import sys
import subprocess as sp
from time import sleep

from rewrite import (
    CookieAuth,
    MethodHandler,
)
from syslog_excepts import CookieGenerateError


def syslog_ctl():
    """ """
    try:
        if CookieAuth.query():
            print('Cookies Generated\n')
        else:
            raise CookieGenerateError

        methods = {
            'clear_history': '{"id":"1","method":"syslog.control.history.set","params":[1, "all", {"Clear": true}]}',
            'get_current_history': '{"id":"1","method":"syslog.status.history.get","params":[]}',
            'get_current_interface': '{"id":"1","method":"ip.config.interface.get","params":[]}',
            'add_interface': '{"id":"1","method":"ip.config.interface.add","params":["VLAN 50"]}',
            'get_after_edit_interface': '{"id":"1","method":"ip.config.interface.get","params":[]}',
            'get_after_edit_history': '{"id":"1","method":"syslog.status.history.get","params":[]}',
        }

        for operation, method in methods.items():
            print(f"{operation}: ", \
                    MethodHandler.exec_method(
                        method=method,
                        operation=operation
                    ).decode('utf-8'))
            sleep(3)
        
    except sp.CalledProcessError as e:
        print(e)
        sys.exit()

syslog_ctl()


# transfer vlans and check if false increment and again step
# grep stdout wit jq (+) 
# handlermethods -> SysLog (+)
# exec_methods -> SysLog (+)
