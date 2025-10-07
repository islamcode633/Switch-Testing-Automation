"""
"""

import sys
import subprocess as sp

from dataclasses import dataclass

from data import RemoteConnection


@dataclass
class EndPoints:
    """  """
    common: str = 'http://192.168.127.253/json_rpc'
    login: str = 'http://192.168.127.253/login'


@dataclass
class User:
    """  """
    Switch = RemoteConnection()
    username: str = Switch.username
    password: str = Switch.password


@dataclass
class DataQuery:
    """  """
    header: str = '-H Content-Type: application/json'
    path_to_cookie: str = '/tmp/auth.cookie'


class BaseCurlOpts:
    """  """
    @staticmethod
    def base_query():
        # 
        return ['curl', '-s', '-b', f"{DataQuery.path_to_cookie}", f"{DataQuery.header}",]


class CookieAuth():
    """  """
    @staticmethod
    def query():
        """ """
        command = f"curl -c {DataQuery.path_to_cookie} -d {User.username}:{User.password} {EndPoints.login}".split()        
        if not sp.run(command, check=True).check_returncode():
            return True


class MethodHandler:
    """  """ 
    @staticmethod
    def exec_method(method, operation):
        """  """
        mapping_operations_on_the_answer_set = {
            'clear_history': '.error',
            'get_current_history': '.result',
            'get_current_interface': '.result|from_entries|has("VLAN 50")',
            'add_interface': '.error',
            'get_after_edit_interface': '.result|from_entries|has("VLAN 50")',
            'get_after_edit_history': '.result[0].val.MsgText'
        }
        command =  BaseCurlOpts.base_query() + ['-d', method, EndPoints.common ]
        result = sp.Popen(command, stdout=sp.PIPE)
        output = sp.check_output(('jq', mapping_operations_on_the_answer_set[operation]), stdin=result.stdout)
        result.wait()
        return output

    """
    @staticmethod
    def clear_history():
        """  """
        method = '{"id":"1","method":"syslog.control.history.set","params":[1, "all", {"Clear": true}]}'
        command =  BaseCurlOpts.base_query() + ['-d', method, EndPoints.common ]
        res = sp.Popen(command, stdout=sp.PIPE)
        output = sp.check_output(('jq', '.error'), stdin=res.stdout)
        res.wait()
        return output

    @staticmethod
    def get_history():
        """ """
        method = '{"id":"1","method":"syslog.status.history.get","params":[]}'
        command = BaseCurlOpts.base_query() + ['-d', method, EndPoints.common ]
        if not sp.run(command, check=True).check_returncode():
            return True

    @staticmethod
    def get_interface():
        """ """
        method = '{"id":"1","method":"ip.config.interface.get","params":[]}'
        command = BaseCurlOpts.base_query() + ['-d', method, EndPoints.common ]
        if not sp.run(command, check=True).check_returncode():
            return True
    
    @staticmethod
    def add_interface():
        method = '{"id":"1","method":"ip.config.interface.add","params":["VLAN 40"]}'
        command = BaseCurlOpts.base_query() + ['-d', method, EndPoints.common ]
        if not sp.run(command, check=True).check_returncode():
            return True
    """
