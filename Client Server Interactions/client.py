import socket             
 
# Create a socket object 
s = socket.socket()

# Define the port on which you want to connect 
port = 12345               
 
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
while True:
    # receive data from the server and decoding to get the string.
    p=s.recv(1024).decode()
    print (p)
    #if p=="exit":
        #break
    x=input("Enter client message")
    s.send(x.encode())
    if x=="exit":
        break

# close the connection 
s.close()   
