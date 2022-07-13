import socket
from threading import Thread
import json
import requests
import ssl
import urllib.parse


class Request:
    def __init__(self, conn: socket.socket) -> None:
        self.conn = conn
        self.closed = False

    def get(self) -> None:
        path = self.conn.recv(64000).decode().split(' ')
        # print(path)
        path = path[1].split("/")

        self.method = path[1]
        self.body = ""

        try:
            self.body = urllib.parse.unquote_plus(path[2])
            self.body = json.loads(self.body)
        except:
            pass

    def end(self, body="", code: int = 200) -> None:

        if self.closed:
            return

        self.closed = True

        if not isinstance(body, str):
            try:
                body = json.dumps(body)
            except:
                pass

        self.conn.send(b"HTTP/1.1 " + str(code).encode() +
                       b"\nAccess-Control-Allow-Origin: *\n\n" +
                       body.encode())
        self.conn.close()


class Server:

    def start_server(self, port: int, certfile: str, keyfile: str) -> None:

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind(('', port))
        self.sock.listen()

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile, keyfile)

        self.sock = context.wrap_socket(self.sock, server_side=True)

        Thread(target=self.listen).start()

    def listen(self) -> None:

        while 1:
            try:
                conn, _ = self.sock.accept()
                Thread(target=self.new_conn, args=(conn,)).start()

            except:
                continue

    def new_conn(self, conn: socket.socket) -> None:

        req = Request(conn)
        try:
            req.get()
            self.on_data(req)

        except BaseException as e:
            req.end(str(e), 400)

    def on_data(self, req: Request):

        return [req.method, req.body]


def test(address: str = "listrum.com", port: int = 2525, certfile: str = "listrum/keys/fullchain1.pem", keyfile: str = "listrum/keys/privkey1.pem"):

    serv = Server()
    serv.start_server(port, certfile, keyfile)

    url = "https://" + address + ":" + str(port)

    res = requests.get(url)
    assert(res.text == json.dumps(["", ""]))
    print("Https test 1 - passed")

    res = requests.get(url + "/new/" + json.dumps({"a": 1}))
    assert(res.text == json.dumps(["new", {"a": 1}]))
    print("Http test 2 - passed")
