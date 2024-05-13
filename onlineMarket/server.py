from socket import *
from threading import *
from time import *
s = socket(AF_INET , SOCK_STREAM)
ip = "127.0.0.1"

host = 9000
s.bind((ip , host))
# Initialize server's port

products_list = [ "product 1" , "product 2" , "product 3", "product 4", "product 5", "product 6", "product 7"]
products_quantity = [100 , 10 , 5 ,6 , 5 ,3 ,1]
products_price = [2 , 50 , 53 , 200 , 500, 300 , 2000]
available = 7

def get_respond_from_client(session):
    client_type = "a"
    while client_type == 'a':
        client_type =  session.recv(2000).decode()
    return(client_type)


def new_client(session):
    global products_list
    global products_quantity
    global products_price
    products_count = len(products_list) # Number of all products on system 
    global available # Number of available products
    
    # Get client's info
    session.send("Please enter your name".encode())
    client_name = get_respond_from_client(session)
    session.send("Please enter your address".encode())
    client_address = get_respond_from_client(session)

    session.send(("Welcome to our store " + client_name).encode())
    session.send(("Would you like to place an order ? y/n").encode())
    ans =  get_respond_from_client(session)
    
    if(ans != "y"): # Client did not find the item he want or just want to end 
        session.send(("Thank you for visiting us " + client_name).encode())
        return
    
    if(available == 0): # if all products are sold out
        session.send("Sorry all our products are sold out".encode())
        session.send(("Thank you for visiting us " + client_name).encode())
        
    
    session.send("These are our available products :".encode())
    for i in range(products_count):
        if(products_quantity[i] != 0):
            session.send((str(i+1) + "- " + products_list[i] + "\n" ).encode())
            session.send(("Price  " + str(products_price[i]) + "\n").encode())
            session.send((str(products_quantity[i]) + "  available" + "\n").encode())
            session.send(("-------------------------------"+ "\n").encode())
    wanted = [0 for i in range(products_count)]
    while True:    
        session.send("Number of product you want to buy :".encode())
        want = int(get_respond_from_client(session))
        want -= 1
        session.send("How many do you want ? :".encode())
        wanted_quantity = int(get_respond_from_client(session))
        wanted[want] += wanted_quantity
        if(products_quantity[want] < wanted[want]):
            session.send("Sorry we do not have this quantity".encode())
            wanted[want] -= wanted_quantity
        session.send("Would you like to add another item y/n".encode())
        if(get_respond_from_client(session) == 'n'):
            break
    session.send(("This is your order :" + '\n').encode())
    total = 0
    for i in range(products_count):
        if(wanted[i] != 0):
            session.send((str(wanted[i]) + " of " + products_list[i] + "   price : " + str(products_price[i] * wanted[i]) + ' EGP\n').encode())
            total += (products_price[i] * wanted[i])
    session.send(("Total bill is : " + str(total) + " EGP \n").encode())
    session.send("Would you like to checkout ? y/n".encode())
    ans =  get_respond_from_client(session)
    if(ans != 'y'):
        session.send(("Thank you for visiting us " + client_name).encode())
        return
    ok = True
    for i in range(products_count):
        if(products_quantity[i] < wanted[i]):
            ok = False
    
    if ok:
        for i in range(products_count):
            if(wanted[i] != 0):
                products_quantity[i] -= wanted[i]
                if products_quantity[i] == 0:
                    available -=1
        session.send(("Your order will arrive to "+ client_address + " in 3 working days.\n thank you for using our service" + client_name).encode())
    else:
        session.send(("Sorry " + client_name +  " another client took this item , see you soon").encode())
    
    sleep(60)
    session.send("".encode())
    session.close()
    
clients = 0
s.listen()
while True:
    session , addres = s.accept()
    clients +=1
    Thread(target= new_client , args=(session ,)).start()