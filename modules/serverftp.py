# ftp_server.py
import argparse
import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS
from io import BytesIO
from pyftpdlib.log import config_logging

class InMemoryFS(AbstractedFS):
    def __init__(self, root, cmd_channel):
        super().__init__(root, cmd_channel)
        self.files = {}

    def open(self, filename, mode):
        if 'r' in mode and filename not in self.files:
            raise FileNotFoundError(f"No such file or directory: '{filename}'")
        if 'w' in mode:
            self.files[filename] = BytesIO()
        fileobj = self.files[filename]
        return fileobj

    def remove(self, filename):
        del self.files[filename]

    def listdir(self, path):
        return list(self.files.keys())

    def isfile(self, path):
        return path in self.files

    def isdir(self, path):
        return False

    def stat(self, path):
        fileobj = self.files[path]
        size = fileobj.getbuffer().nbytes
        return {'st_size': size}

def main(args):
    config_logging(level=args.loglevel)
    
    authorizer = DummyAuthorizer()
    authorizer.add_user(args.username, args.password, "/", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.abstracted_fs = InMemoryFS
    handler.banner = "Welcome to the in-memory FTP server."

    address = (args.host, args.port)
    server = FTPServer(address, handler)
    server.max_cons = args.max_cons
    server.max_cons_per_ip = args.max_cons_per_ip

    logging.info(f"Starting FTP server on {args.host}:{args.port}")
    server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an in-memory FTP server.")
    parser.add_argument('--host', default='0.0.0.0', help='Hostname to listen on')
    parser.add_argument('--port', type=int, default=2121, help='Port to listen on')
    parser.add_argument('--username', default='user', help='Username for FTP login')
    parser.add_argument('--password', default='12345', help='Password for FTP login')
    parser.add_argument('--max_cons', type=int, default=256, help='Maximum number of connections')
    parser.add_argument('--max_cons_per_ip', type=int, default=5, help='Maximum number of connections per IP')
    parser.add_argument('--loglevel', default='INFO', help='Logging level')

    args = parser.parse_args()
    main(args)
