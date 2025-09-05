"""
Checking support reading time from RTC
"""

from typing import Union, Any

import sys
from datetime import datetime
from time import sleep

from data import RemoteConnection


def configure_datetime(ssh_conn: Any, flag: str = "") -> str:
    """
    Set time on Switch
    and return datetime
    """
    if flag == 'set_dt':
        print('Setting time on Switch ...')
        sleep(3)
        config_commands: list[str] = [
            "clock time \
            day 01 month 01 year 2023 \
            hour 00 minute 00 second 00"
        ]
        ssh_conn.send_config_set(config_commands=config_commands)

    return str(ssh_conn.send_command('show clock')).split()[-1]


def convert_datetime_to_unix(dt: str = "", seconds: int = 0) -> int:
    """ Date and time to Unix epoch """
    try:
        date: str = dt[:dt.index('T')]
        time: str = dt[dt.index('T') + 1:dt.index('+')]
        seconds = int(datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S').timestamp())
        return seconds
    except ValueError:
        print('Error converting date and time to unix !')
        sys.exit(1)


def counter_time() -> int:
    """ Counting the time elapsed """
    try:
        print('To stop timer and continue test press Ctrl+C')
        secs: int = 0
        while True:
            secs += 1
            print(f'   timer: {secs}', end='\r')
            sleep(1)
    except KeyboardInterrupt:
        return secs


def convert_unix_to_datetime(total_time: int) -> Union[str, None]:
    """ Seconds from Unix epoch in date and time """
    if isinstance(total_time, int):
        dt: str = str(datetime.fromtimestamp(total_time))
        return dt
    return None


def rtc_ctl() -> None:
    """ Control of test execution flow """
    print('--- Start RTC ---')
    sleep(3)
    with RemoteConnection().init_conn_session() as ssh_conn:
        default_datetime: str = configure_datetime(ssh_conn=ssh_conn, flag='set_dt')

    seconds: int = convert_datetime_to_unix(dt=default_datetime)
    timer: int = counter_time()
    # constant 6 approximately the time spent on an SSH Session
    total_time: int = timer + seconds + 6

    print(f'\nSet time:     {default_datetime}')
    print(f'Expected time: {convert_unix_to_datetime(total_time=total_time)} deviation by +-[2:3] sec')
    with RemoteConnection().init_conn_session() as ssh_conn:
        print(f'Current time: {configure_datetime(ssh_conn=ssh_conn)}')
