from enum import Enum
from datetime import datetime, timedelta
from threading import Lock


class Window:
    """
    Time frame management.
    Provides methods for knowing whether a client's request is within the allowed 5-second time frame and can approve a
    new request that is within the requests quota.
    """
    WINDOW_TIME = timedelta(seconds=5)
    MAX_NUM_OF_HITS = 5

    def __init__(self) -> None:
        self._start_time = datetime.now()
        self._end_time = self._start_time + self.WINDOW_TIME
        self._lock = Lock()
        self._num_of_hits = 0

    def is_in_window(self, date_and_time: datetime) -> bool:
        """
        Returns whether the request is done within the time frame
        :param date_and_time: what time is it when this function is called
        :return: are we in the time frame or not
        """
        return (date_and_time >= self._start_time) and (date_and_time <= self._end_time)

    def is_after_end_time(self, date_and_time: datetime) -> bool:
        """
        Whether the time frame's 5-second lifespan is over
        :param date_and_time: what time is it when this function is called
        :return: whether this time frame exceeded its approved age
        """
        return date_and_time > self._end_time

    def check_hit(self) -> bool:
        """
        Add hit to number of hits in window and check if total number of hits in window is above maximum
        :return: True - hit is not above maximum, False otherwise
        """
        self._num_of_hits += 1
        return self._num_of_hits <= self.MAX_NUM_OF_HITS


class WindowType(Enum):
    """
    Simple enum to manage which type of window are we dealing with
    """
    DYNAMIC = 1
    STATIC = 2
