import threading
import time

import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    #read from file
    with open('in-proj.txt', 'r') as infile:
        numOfLines = len(infile.readlines())
        cs.send(numOfLines.to_bytes(8, 'big'))

    with open('in-proj.txt', 'r') as infile:
        for line in infile:
            #remove newline characters message =line.strip()
            message = line
            #print line
            print(f"[C] Read: {message.strip()}")
            #send
            cs.send(message.encode('utf-8'))
            data_from_server=cs.recv(200)
            print("[C] Received: {}".format(data_from_server.decode('utf-8').strip()))

    if 'infile' in locals():
        infile.close()

    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='client', target=client)
    t1.start()

    time.sleep(5)
    print("Done.")
