from socket import *
from threading import *

s = socket(AF_INET , SOCK_STREAM)
ip = "127.0.0.1"
port = 9000

def request(k):
    while True:
        k.send(input().encode())

def response(k):
    while True:
        x = k.recv(20000).decode()
        print(x)

s.connect((ip , port))
Thread(target=request , args=(s,)).start()
Thread(target=response , args=(s,)).start()
