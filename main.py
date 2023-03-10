from server import ShbksHandler, ShbksThreadedHTTPServer
from threading import Thread


HOST = "localhost"
PORT = 8080


def run_server() -> None:
    server = ShbksThreadedHTTPServer((HOST, PORT), ShbksHandler)
    print("Server now running...")
    server.serve_forever()


if __name__ == "__main__":

    try:
        server_thread = Thread(target=run_server).start()

    except KeyboardInterrupt:
        print("Server stopped")
