import socket

s = socket.socket()         
print ("Socket successfully created")
port = 12345              
s.bind(('', port))
print ("socket bound to %s" %port)
s.listen(5)     
print ("socket is listening")   
c, addr = s.accept()  
        
while True: 
  x=input("Enter Server Message")  # send a thankyou message to the client. encoding to send byte type.
  c.send(x.encode())
  #if c=="exit":
    #break
  p=c.recv(1024).decode()
  print(p)
  if p=="exit":
    break
   
c.close()
   
  

