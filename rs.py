# HARDCODED PORTS
# updated 12:06 by Nami

import threading
import time
import random

import socket

import sys

def build_request(host_name, i, flag):
    return '0 ' + host_name + " " + str(i) + " " + flag

def get_flag(request):
    List = request.split(" ")
    return List[-1]

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

    with open("rsdatabase.txt", "r") as rsdatabase:
        entries = rsdatabase.readlines()

    request = csockid.recv(200)
    request = request.decode('utf-8')
    
    split_request = request.split()

    # traverse the entries from the rsdatabase to see if any match the request
    # entry is from the rsdatabase
    # name is from the request received by rs
    is_found = 0
    for entry in entries:

        name = split_request[1]
        
        split_entry = entry.split()

        entry_name = split_entry[0]

        IP = split_entry[1]
        i = split_request[2]

        #checkpoint reached
        if name == entry_name:
            # build response
            response = build_response(entry_name, IP, i, 'aa')
            csockid.send(response.encode('utf-8'))
            is_found = 1
            testresponse = response.decode('utf-8')
            #out_file.write(response + "\n")
            print("if name == entry_name " +testresponse + "\n")
            break
        
        else:
            # check if it's ts1 or ts2
            split_name = name.split(".")
            last_part = split_name[-1]
            
            if last_part == entry_name:
                # get request flag and check if it is rd or it
                is_found = 1
                flag = split_request[3]
                if last_part == 'com':
                    port = 47000 #ts1
                else:
                    port = 48000 #ts2

                if flag == 'rd':
                    print ("checkpoint start")
                    # recursive, send request to ts1/ts2
                    request = build_request(name, i, 'rd')
                    #ts_addr = socket.gethostbyname(split_entry[1])               UNDO
                    binding = ('popsicle.cs.rutgers.edu', 47000)
                    ss.connect(binding)
                    ss.send(request.encode('utf-8'))
                    print ("A checkpoint")

                    # send to the client the response received
                    # we don't have to encode response before sending because the ts already encoded it for us
                    response = ss.recv(200)
                    csockid.send(response)
                    
                    testresponse = response.decode('utf-8')
                    #out_file.write(response + "\n")
                    print("if rd " +testresponse + "\n")

                elif flag == "it":
                    # iterative, send response to client
                    response = build_response(entry_name, IP, i, 'ns')
                    csockid.send(response.encode('utf-8'))
                    testresponse = response.decode('utf-8')
                    #out_file.write(response + "\n")
                    print("if it " +testresponse + "\n")
                    break
            else:
                print("else for last_part == entry_name")
            print ("X checkpoint END")      # not being reached
    
    if is_found == 0:
        # this means there was nothing associated to request found in rsdatabase
        IP = split_entry[1]
        i = split_request[2]
        testresponse = response.decode('utf-8')
        #out_file.write(response + "\n")
        print("if is_found ==0 " +testresponse + "\n")
        response = build_response(entry_name, '0.0.0.0', i, 'nx')
        csockid.send(response.encode('utf-8'))

    # Close the server socket
    # ss.close()
    # exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()
