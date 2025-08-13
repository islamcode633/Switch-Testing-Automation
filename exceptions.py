"""
Exception for Reset button
"""

class CommandNotFound(Exception):
    """
    Сommand was not passed to the function
    for remote execution on the switch
    """


class RequiredVLANNotFound(Exception):
    """ Failed to add VLAN 10 on switch """


class ResetModeNotSelected(Exception):
    """ One of the reset modes is not selected """


class ShortPeriodOfTimeToConnect(Exception):
    """ Required time to connect 120 seconds or more """
