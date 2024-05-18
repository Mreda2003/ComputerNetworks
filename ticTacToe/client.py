from tkinter import *
from socket import *
from tkinter import messagebox
from functools import partial
session = socket(AF_INET , SOCK_STREAM)
from threading import *
session.connect(("127.0.0.1" ,8000 ))
myTurn = 1
count = 0
btns = []
def check():
    global page
    winner = -1
    for i in range(3):
        if btns[i*3]['text'] == btns[i*3+1]['text'] and btns[i*3]['text'] == btns[i*3+2]['text'] and btns[i*3]['text'] != " ":
            if btns[i*3]['text'] == "X":
                messagebox.showinfo(title="Game over " , message="Player 1")
                winner = 1
            else:
                winner = 2
                messagebox.showinfo(title="Game over " , message="Player 2")
    for i in range(3):
        if btns[i+3]['text'] == btns[i+6]['text'] and btns[i]['text'] == btns[i+3]['text'] and btns[i+3]['text'] != " ":
            if btns[i+3]['text'] == "X":
                winner = 1
            else:
                winner = 2
    if(btns[4]['text'] == " "):
        pass
    else:
        if btns[0]['text'] == btns[4]['text'] and btns[8]['text'] == btns[0]['text'] and btns[4]['text'] != " ":
            if btns[0]['text'] == "X":
                winner = 1
            else:
                winner = 2

        if btns[6]['text'] == btns[2]['text'] and btns[2]['text'] == btns[4]['text'] and btns[4]['text'] != " ":
            if btns[0]['text'] == "X":
                winner = 1
            else:
                winner = 2
    if winner != -1:
        messagebox.showinfo(title="Game over " , message="Player " + str(winner)+" won")                
        page.destroy()
    if count == 9:
        messagebox.showinfo(title="Game over " , message="tie")                
        page.destroy()
    
def fromServer():
    global session
    global myTurn
    x = " "
    while x == " ":
        x = session.recv(2000).decode()
    myTurn = 1
    i = int(x[0])
    j = int(x[1])
    btns[i*3+j]['text'] = "X"
    check()


def onclick(i , j):
    global myTurn
    global btns
    global count
    global session
    if(myTurn == 1 and btns[i*3+j]['text'] == " "):
        myTurn = 0
        count += 1
        session.send((str(i) + str(j)).encode())
        btns[i*3+j]['text'] = "O"
        check()
        Thread(target=fromServer).start()
    
page = Tk()
page.title("Player O")
page.geometry("230x200")
l1 = Label(page , text="Player 2" , font=14)
l1.grid(row= 0 , column= 0)
l2 = Label(page , text="plays O" , font= 15)
l2.grid(row = 0 , column = 1)

for i in range(3):
    for j in range(3):
        b = Button(page , width= 6 , height= 2 , bg= "black" , fg= "white" , text=" " , font=15 , command=lambda:onclick(i , j))
        b.config(command=partial(onclick , i , j))
        b.grid(row=i+1 , column= j)
        btns.append(b)
Thread(target=fromServer).start()
mainloop()
