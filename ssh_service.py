"""
Provides services for activation/deactivation
 and verification of connections via ssh.
"""

class SSHConnect():
    """ Checking ssh protocol support """
    @staticmethod
    def is_enabled(output: str) -> bool:
        """ Checking ssh connection activity """
        can_active: str = 'enabled'
        if can_active in output:
            return True
        return False

    @staticmethod
    def get_info_about_ssh(tn_connect) -> str:
        """ Get information about the presence of a connection via ssh """
        mode: str = 'do show ip ssh'
        output: str = tn_connect.send_command(mode).split()
        return output

    @staticmethod
    def activate(tn_connect) -> None:
        """ Activate ssh connection """
        enable_ssh_connection: list[str] = ['ip ssh']
        tn_connect.send_config_set(enable_ssh_connection)

    @staticmethod
    def deactivate(tn_connect) -> None:
        """ Deactivate ssh connection """
        disable_ssh_connection: list[str] = ['no ip ssh']
        tn_connect.send_config_set(disable_ssh_connection)
