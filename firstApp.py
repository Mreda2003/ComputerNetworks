try:
    file = open("text.txt" , "r")
    file.write("Hi there")
except IOError:
    print("can't do it")
else:
    print("added successfuly")
    file.close()