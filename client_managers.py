from datetime import datetime
from threading import Lock
from window_et_al import Window


class ClientManager:
    """
    Base class for the static and dynamic client managers
    """
    def __init__(self) -> None:
        self._client_manager_lock = Lock()

    def can_open_thread(self, time_now: datetime) -> bool:
        """
        Checks the ClientManager in question can be responded with a 200 response and a wfile  (approved) or a 503 error
        (denied). The check is done according the window's anti-DoS logic.
        :param time_now: - what time is it when the request is sent to the client manager
        :return: Request approved or denied
        """
        pass

    def get_wfile(self) -> str:
        """
        Returns the string version of a very primitive HTML file, written primitively, so I could focus on the rest of
        this coding assignment
        :return: wfile string
        """
        pass


class StaticClientManager(ClientManager):
    """
    Client manager for all the static window requests of a certain client.
    It has one window that it renews every time the window's life span is over. While a window is alive, its hits number
    can only reach up to 5 before it starts causing the request to be refused.
    """
    def __init__(self) -> None:
        super().__init__()

        self._window = Window()

    def can_open_thread(self, time_now: datetime) -> bool:
        """
        Checks the ClientManager in question can be responded with a 200 response and a wfile  (approved) or a 503 error
        (denied). The time frame for approving requests starts on each client’s first request and ends 5 seconds later.
        After the time frame has ended, the client’s first request will open a new time frame, and so forth.
        :param time_now: - what time is it when the request is sent to the client manager
        :return: Request approved or denied
        """
        if self._window.is_after_end_time(time_now):
            self._window = Window()

        return self._window.check_hit()

    def get_wfile(self) -> str:
        return "<html><body><h1>HELLO WORLD! STATIC</h1></body></html>"


class DynamicClientManager(ClientManager):
    """
    Client manager for all the dynamic window requests of a client.
    It has a list of all its windows (ledger), each request opening a new window and every request increases the
    window's hit counter. If one of the windows in the ledger is experiencing a hit number beyond the maximum hits
    allowed, the request will be denied.
    """
    def __init__(self) -> None:
        super().__init__()

        # a ledger of all the windows opened
        self._windows_ledger = []

    def can_open_thread(self, time_now: datetime) -> bool:
        """
        Checks the ClientManager in question can be responded with a 200 response and a wfile (approved) or a 503 error
        (denied). TThe time frame for approving requests slides with each client request, upon each received request
        make sure no more than 5 requests are being processed in each time frame.
        :param time_now: - what time is it when the request is sent to the client manager
        :return: Request approved or denied
        """
        current_hit_window = Window()
        thread_request_answer = True

        self._windows_ledger.append(current_hit_window)

        with self._client_manager_lock:
            for window in self._windows_ledger:
                if window.is_after_end_time(time_now):
                    self._windows_ledger.remove(window)
                    continue

                if window.is_in_window(time_now):
                    if not window.check_hit():
                        thread_request_answer = False

        return thread_request_answer

    def get_wfile(self) -> str:
        return "<html><body><h1>HELLO WORLD! DYNAMIC</h1></body></html>"

