from socket import *
from threading import *
from time import *

# Initialize server's port
s = socket(AF_INET , SOCK_STREAM)
ip = "127.0.0.1"
host = 9000
s.bind((ip , host))

# Set products data 
products_list = [ "product 1" , "product 2" , "product 3", "product 4", "product 5", "product 6", "product 7"]
products_quantity = [100 , 10 , 5 ,6 , 5 ,3 ,1]
products_price = [2 , 50 , 53 , 200 , 500, 300 , 2000]
available = len(products_list)
lock = Lock()
def get_data_from_client(session):
    client_type = "a"
    while client_type == 'a':
        client_type =  session.recv(2000).decode()
    return(client_type)

def send_data_to_client(session , data):
    session.send(data.encode())


def new_client(session):
    global products_list
    global products_quantity
    global products_price
    global lock
    global available # Number of available products
    products_count = len(products_list) # Number of all products on system 
    try:    
        # Get client's info
        send_data_to_client(session , "Please enter your name")
        client_name = get_data_from_client(session)
        send_data_to_client(session , "Please enter your address")
        client_address = get_data_from_client(session)

        # Welcome message
        send_data_to_client(session , ("Welcome to our store " + client_name))
        send_data_to_client(session , ("Would you like to place an order ? y/n"))
        ans =  get_data_from_client(session)
        
        # Client did not find the item he wanted or just want to end 
        if(ans != "y"):
            send_data_to_client(session , ("Thank you for visiting us " + client_name))
            return
        
        # If all products are sold out
        if(available == 0): 
            send_data_to_client(session , "Sorry all our products are out of stock")
            send_data_to_client(session , ("Thank you for visiting us " + client_name))
            return
            
        # Showing available products price and stock
        send_data_to_client(session , "These are our available products :")
        for i in range(products_count):
            if(products_quantity[i] != 0):
                send_data_to_client(session , (str(i+1) + "- " + products_list[i] + "\n" ))
                send_data_to_client(session , ("Price  " + str(products_price[i]) + "\n"))
                send_data_to_client(session , (str(products_quantity[i]) + "  available" + "\n"))
                send_data_to_client(session , ("-------------------------------"+ "\n"))
                
        # Getting order from client , insure that he can not order more than in stock
        wanted = [0 for i in range(products_count)] 
        while True:
            send_data_to_client(session , "Number of product you want to buy :")
            want = int(get_data_from_client(session))
            if(want > len(products_list)):
                print("sorry we don't have this item")
                continue
            want -= 1
            send_data_to_client(session , "How many do you want ? :")
            wanted_quantity = int(get_data_from_client(session))
            wanted[want] += wanted_quantity
            if(products_quantity[want]):
                send_data_to_client(session , "Sorry we do not have this quantity")
                wanted[want] -= wanted_quantity
            send_data_to_client(session , "Would you like to add another item y/n")
            if(get_data_from_client(session) == 'n'):
                break

        # Revise the order and get confirmation
        send_data_to_client(session , ("This is your order :" + '\n'))
        total = 0
        for i in range(products_count):
            if(wanted[i] != 0):
                send_data_to_client(session , (str(wanted[i]) + " of " + products_list[i] + "   price : " + str(products_price[i] * wanted[i]) + ' EGP\n'))
                total += (products_price[i] * wanted[i])
        send_data_to_client(session , ("Total bill is : " + str(total) + " EGP \n"))
        send_data_to_client(session , "Would you like to checkout ? y/n")
        ans =  get_data_from_client(session)
        if(ans != 'y'):
            send_data_to_client(session , ("Thank you for visiting us " + client_name))
            return
        # Check if no other client bought the items before confirmation , as a critical section
        with lock:
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
                send_data_to_client(session , ("Your order will arrive to "+ client_address + " in 3 working days.\n thank you for using our service " + client_name))
            else:
                send_data_to_client(session , ("Sorry " + client_name +  " another client took this item , see you soon"))
    except:
        send_data_to_client(session , "A problem occured please try again later")
    finally:
        sleep(60)
        send_data_to_client(session , "")
        session.close()

clients = 0
s.listen()
while True:
    session , addres = s.accept()
    clients +=1
    Thread(target= new_client , args=(session ,)).start()