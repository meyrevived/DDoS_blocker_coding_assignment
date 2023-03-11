from socketserver import BaseServer, ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
from datetime import datetime
from re import search

from client_managers import StaticClientManager, DynamicClientManager
from window_et_al import WindowType


class ShbksHandler(BaseHTTPRequestHandler):
    """
    ShbksHandler - handles HTTP requests and manages the various clients that send the server GET requests
    """

    # a ledger of the clients and their ClientManager classes
    _clients_ledger = {}
    _lock = Lock()

    # only going to have a method to deal with GET messages because I'm simulating
    # a denial of service on a landing page
    # Also, I don't have a lot of time to work on this :)
    def do_GET(self) -> int:
        """
        Handles the GET request according to its path. Clients and the windows they are trying to GET influence
        whether a 200 response and a wfile are returned or an 503 error
        :return: int whether the function succeeded (1) or not (-1)
        """
        window_type = None
        time_now = datetime.now()

        try:
            client_id = search("clientId=(.*)", self.path).group(1)
        # I added this because, while testing this project with various web browsers, I discovered some of them
        # follow up their GET with a request for path /favicon.ico without the clientID you gave in the assignment
        # description
        except AttributeError:
            print(f"Path is now {self.path}")
            return -1
        if self.path.find('/StaticWindow') != -1:
            window_type = WindowType.STATIC
        elif self.path.find('/DynamicWindow') != -1:
            window_type = WindowType.DYNAMIC
        else:
            print(f"Client is trying to retrieve a page we don't have")
            self.send_error(404, "We don't have what you're looking for")

        current_client = f"{client_id}_{window_type}"
        with self._lock:
            if current_client not in self._clients_ledger:
                if window_type == WindowType.STATIC:
                    self._clients_ledger[current_client] = StaticClientManager()
                else:
                    self._clients_ledger[current_client] = DynamicClientManager()

        client = self._clients_ledger[current_client]

        if client.can_open_thread(time_now):
            print(f"Starting request for client ID {client_id}")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response_file = client.get_wfile()
            self.wfile.write(bytes(response_file, "utf-8"))
        else:
            print(f"Client {client_id} has exceeded their window's thread quota")
            self.send_error(503, "Don't DoS me")

        return 1


class ShbksThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
