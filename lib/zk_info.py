from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None



from functools import partial

zk_command = ("conf","cons","dump","envi","reqs","ruok","stat","wchs","wchc","wchp")

for item  in zk_command:
    conn = LazyConnection(('10.46.162.118', 2181))
    with conn as s:
    	s.send(item)
    	resp = b''.join(iter(partial(s.recv, 8192), b''))
	print resp
