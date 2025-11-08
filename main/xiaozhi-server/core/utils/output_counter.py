import datetime
from typing import Dict, Tuple

# A global dictionary that stores the daily output word count for each device
_device_daily_output: Dict[Tuple[str, datetime.date], int] = {}
# Record the date of last inspection
_last_check_date: datetime.date = None


def reset_device_output():
    """Reset daily output word count for all devices
    Call this function at 0 o'clock every day"""
    _device_daily_output.clear()


def get_device_output(device_id: str) -> int:
    """Get the number of words output by the device on the day"""
    current_date = datetime.datetime.now().date()
    return _device_daily_output.get((device_id, current_date), 0)


def add_device_output(device_id: str, char_count: int):
    """Increase the output word count of the device"""
    current_date = datetime.datetime.now().date()
    global _last_check_date

    # If it is the first call or the date changes, clear the counter
    if _last_check_date is None or _last_check_date != current_date:
        _device_daily_output.clear()
        _last_check_date = current_date

    current_count = _device_daily_output.get((device_id, current_date), 0)
    _device_daily_output[(device_id, current_date)] = current_count + char_count


def check_device_output_limit(device_id: str, max_output_size: int) -> bool:
    """Check if the device exceeds output limits
    :return: True if the limit is exceeded, False if it is not exceeded"""
    if not device_id:
        return False
    current_output = get_device_output(device_id)
    return current_output >= max_output_size
