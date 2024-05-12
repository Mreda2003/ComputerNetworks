from socket import *
from threading import *
host = "127.0.0.1"
port = 8000

s = socket(AF_INET , SOCK_STREAM) # ipv4 AF_INET -- SOCK_STREAM TCP
s.bind((host , port))

x = []

def get(c):
    while True:
     x = c.recv(2048)
     print( "client :"  , x.decode())
def send(c):
    while True:
        p = input().encode()
        for i in c:
            i.send(p)


while True:
    s.listen()
    c , addr = s.accept()
    print("connected to" , addr)
    x.append(c)
    Thread(target= get , args=(c , )).start()
    Thread(target= send , args=(x , )).start()    
