from socket import *
from threading import *
s = socket(AF_INET , SOCK_STREAM)

def respond(s):
    while True:    
        a = s.recv(2028)
        print("server : " ,a.decode())

host = "127.0.0.1"
port = 8000

s.connect((host , port))
Thread(target= respond , args= (s , )).start()

while True:
    s.send(input().encode())
   