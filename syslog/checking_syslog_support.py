"""
Checking the logging support system
"""

import sys
import subprocess as sp

from time import sleep
from dataclasses import dataclass

from syslog_excepts import CookieGenerateError


@dataclass
class EndPoints:
    """ 
    Contains API.

    :common: api for all calls
    :login: api only for auth
    """
    common: str = 'http://192.168.127.253/json_rpc'
    login: str = 'http://192.168.127.253/login'


@dataclass
class User:
    """ Init User """
    username: str = 'admin'
    password: str = 'password'


@dataclass
class DataQuery:
    """
    Data for the request.
 
    :header: JSON
    :path_to_cookie: generated cookie
    """
    header: str = '-H Content-Type: application/json'
    path_to_cookie: str = '/tmp/auth.cookie'


class BaseCurlOpts:
    """ Curl options """
    @staticmethod
    def base_query() -> list[str]:
        """ Return basic command in every request """
        return ['curl', '-s', '-b', f"{DataQuery.path_to_cookie}", f"{DataQuery.header}",]


class Auth():
    """ Auth via cookie """
    @staticmethod
    def generate_cookie() -> bool | None:
        """ Creating a cookie file at the specified path """
        command: list[str] = f"curl -c {DataQuery.path_to_cookie} -d {User.username}:{User.password} {EndPoints.login}".split()
        if not sp.run(command, check=True).check_returncode():
            return True
        return None


class MethodHandler:
    """ All methods to one Exec """
    @staticmethod
    def exec_method(method: str = '', operation: str = '') -> bytes:
        """ Сommon method for all requests """
        mapping_operations_on_the_answer_set: dict[str, str] = {
            'clear_history': '.error',
            'get_current_history': '.result',
            'get_current_interface': '.result|from_entries|has("VLAN 2")',
            'add_interface': '.error',
            'get_after_edit_interface': '.result|from_entries|has("VLAN 2")',
            'get_after_edit_history': '.result[0].val.MsgText'
        }
        command: list[str] = BaseCurlOpts.base_query() + ['-d', method, EndPoints.common ]
        with sp.Popen(command, stdout=sp.PIPE) as proc:
            output: bytes = sp.check_output((
                        'jq',
                        mapping_operations_on_the_answer_set[operation]
                        ),
                        stdin=proc.stdout
                    )
        return output


def syslog_ctl() -> None:
    """ Control of test execution flow """
    try:
        if Auth.generate_cookie():
            print('Cookies Generated\n')
        else:
            raise CookieGenerateError

        methods: dict[str, str] = {
            'clear_history': '{"id":"1","method":"syslog.control.history.set","params":[1, "all", {"Clear": true}]}',
            'get_current_history': '{"id":"1","method":"syslog.status.history.get","params":[]}',
            'get_current_interface': '{"id":"1","method":"ip.config.interface.get","params":[]}',
            'add_interface': '{"id":"1","method":"ip.config.interface.add","params":["VLAN 2"]}',
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
