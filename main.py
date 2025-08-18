import sys
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetMikoAuthenticationException,
    ConnectionException,
    ReadException,
    WriteException,
    NetmikoBaseException
)

from checking_lldp_support import lldp_ctl
from checking_support_telnet import telnet_ctl
from ssh import ssh_ctl
from reset_to_default_settings import reset_ctl


def parser():
    pass


def run():
    try:
        match 'telnet':
            case 'lldp':
                lldp_ctl()
            case 'telnet':
                telnet_ctl()
            case 'ssh':
                ssh_ctl()
            case 'reset':
                reset_ctl()
    except NetmikoTimeoutException:
        print('SSH session timed trying to connect to the device')
    except NetMikoAuthenticationException:
        print('SSH authentication exception based on Paramiko AuthenticationException')
    except ConnectionException:
        print('Generic exception indicating the connection failed')
    except (ReadException, WriteException):
        print('An error occurred during a read or write operation')
    except NetmikoBaseException:
        print('Possible errors are related with:\n' \
                ' Generic exception indicating the connection failed\n' \
                ' Exception raised for invalid configuration error\n' \
                ' General exception indicating an error occurred during a Netmiko write operation\n'
            )
    except Exception as e:
        print(e)
    finally:
        sys.exit()


if __name__ == '__main__':
    run()


# add exceps +
# add return in module functions
# add parse
# add comm module
# add comm func
