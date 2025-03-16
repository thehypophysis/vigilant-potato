import threading
import time

import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    #receive message from client and send back
    number=csockid.recv(8)
    number = int.from_bytes(number,'big')
    
    outfile = open( 'out-proj.txt','w')
    for i in range(number):
        return_msg = csockid.recv(200)
        return_msg = return_msg.decode('utf-8')
        reversed_msg = return_msg[::-1].swapcase()
        csockid.send(reversed_msg.encode('utf-8'))
        #write to outfile
        outfile.write(reversed_msg)

    # Close the server socket
    ss.close()
    exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()

    time.sleep(20)
    print("Done.")
