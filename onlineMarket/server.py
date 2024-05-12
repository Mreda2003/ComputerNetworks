from socket import *
from threading import *
from time import *
s = socket(AF_INET , SOCK_STREAM)
ip = "127.0.0.1"

host = 9000
s.bind((ip , host))
# Initialize server's port

products = [ "product 1" , "product 2" , "product 3", "product 4", "product 5", "product 6", "product 7"]
products_quantity = [100 , 10 , 5 ,6 , 5 ,3 ,1]
products_price = [2 , 50 , 53 , 200 , 500, 300 , 2000]
available = 7

responses = []
def get(session , id):
    one = Thread(target= handle_input , args= (session , id))
    one.start()
    one.join()
    return(responses[id])

def handle_input(session , id):
        client_type = "a"
        while client_type == 'a':
         client_type =  session.recv(2000).decode()
        responses[id] = client_type
        return
    

def new_client(session , id):
    responses.append("")
    global products
    global products_quantity
    global products_price
    items = len(products) # Number of all items on system 
    global available # Number of available items
    
    session.send("Please enter your name".encode())
    
    clientName = get(session , id)
    
    session.send(("Welcome to our store " + clientName).encode())
    session.send(("Would you like to place an order ? y/n").encode())
    ans =  get(session , id)
    
    if(ans != "y"): # Client did not find the item he want or just want to end 
        session.send(("Thank you for visiting us " + clientName).encode())
        return
    
    if(available == 0): # if all products are sold out
        session.send("Sorry all our products are sold out".encode())
        session.send(("Thank you for visiting us " + clientName).encode())
        
    
    session.send("These are our available products :".encode())
    for i in range(items):
        if(products_quantity[i] != 0):
            session.send((str(i+1) + "- " + products[i] + "\n" ).encode())
            session.send(("Price  " + str(products_price[i]) + "\n").encode())
            session.send((str(products_quantity[i]) + "  available" + "\n").encode())
            session.send(("-------------------------------"+ "\n").encode())
    wanted = [0 for i in range(items)]
    while True:    
        session.send("Number of product you want to buy :".encode())
        want = int(get(session , id))
        want -= 1
        session.send("How many do you want ? :".encode())
        wanted_quantity = int(get(session , id))
        wanted[want] += wanted_quantity
        if(products_quantity[want] < wanted[want]):
            session.send("Sorry we do not have this quantity".encode())
            wanted[want] -= wanted_quantity
        session.send("Would you like to add another item y/n".encode())
        if(get(session , id) == 'n'):
            break
    session.send(("This is your order :" + '\n').encode())
    total = 0
    for i in range(items):
        if(wanted[i] != 0):
            session.send((str(wanted[i]) + " of " + products[i] + "   price : " + str(products_price[i] * wanted[i]) + ' EGP\n').encode())
            total += (products_price[i] * wanted[i])
    session.send(("Total bill is : " + str(total) + " EGP \n").encode())
    session.send("Would you like to checkout ? y/n".encode())
    ans =  get(session , id)
    if(ans != 'y'):
        session.send(("Thank you for visiting us " + clientName).encode())
        return
    ok = True
    for i in range(items):
        if(products_quantity[i] < wanted[i]):
            ok = False
    
    if ok:
        for i in range(items):
            if(wanted[i] != 0):
                products_quantity[i] -= wanted[i]
                if products_quantity[i] == 0:
                    available -=1
        session.send(("All done have a nice day " + clientName).encode())
    else:
        session.send(("Sorry " + clientName +  " another client took this item , see you soon").encode())
    
    sleep(60)
    session.send("".encode())
    session.close()
    
clients = 0
s.listen()
while True:
    session , addres = s.accept()
    clients +=1
    Thread(target= new_client , args=(session , clients-1)).start()