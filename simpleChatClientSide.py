from socket import *
from time import *
from _thread import*
try:
    s = socket(AF_INET , SOCK_STREAM)
    host = "127.0.0.1"
    port = 7002
    s.connect((host , port))
    while True:
        s.send(input("client :").encode("utf-8"))
        y = s.recv(2048)
        print("server" , y.decode("utf-8") , ctime(time()))
    s.close()
except error as e:
    print(e)
except KeyboardInterrupt:
    print("Chat is terminated")