__all__ = (
    'datetime2timestamp',
)
import time


def datetime2timestamp(dt):
    return int(time.mktime(dt.timetuple()))


def get_current_timestamp():
    return int(time.time())
