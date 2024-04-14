from threading import *
from time import *

def printNow(s, t):
    for i in range(4):
        print(s, "--------", ctime())
        sleep(t)  # Add a delay between prints

try:
    thread1 = Thread(target=printNow, args=("first", 1))
    thread2 = Thread(target=printNow, args=("second", 2))

    thread1.start()
    thread2.start()

except:
    print("error")
