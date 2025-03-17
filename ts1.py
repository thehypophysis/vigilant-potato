import threading
import time
import random

import socket

import sys

def get_flag(request):
    List = request.split()
    return List[len(List)-1]

def build_response(domain_name, IP, i, flag):
    return '1 ' + domain_name + " " + IP + " " + i + " " + flag

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    port = int(sys.argv[1])
    server_binding = ('', port)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    with open("ts1database.txt", "r") as rsdatabase:
        entries = rsdatabase.readlines()

    #print response in ts1responses.txt
    
    request = csockid.recv(200)
    request = request.decode('utf-8')
    
    split_request = request.split()

    # traverse the entries from the rsdatabase to see if any match the request
    is_found = 0
    for entry in entries:

        name = split_request[1]
        
        split_entry = entry.split()

        entry_name = split_entry[0]

        if name == entry_name:
            # build response
            IP = split_entry[1]
            i = split_request[2]
            response = build_response(entry_name, IP, i, 'aa')
            csockid.send(response.encode('utf-8'))
            is_found = 1
            break
        
        else:
            # check if it's ts1 or ts2
            split_name = name.split(".")
            last_part = split_name[len(split_name)-1]
            
            if last_part == entry_name:
                # get request flag and check if it is rd or it
                is_found = 1
                flag = split_request[3]

                if flag == 'rd':
                    # recursive, send request to ts1 or ts2
                    print("")

                elif flag == "it":
                    # iterative, send response to client
                    print("")
            else:
                print("")
    
    if is_found == 0:
        # this means there was nothing associated to request found in rsdatabase
        IP = split_entry[1]
        i = split_request[2]
        response = build_response(entry_name, '0.0.0.0', i, 'rx')
        csockid.send(response.encode('utf-8'))

    # Close the server socket
    # ss.close()
    # exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()
