# client reads from hostnames.txt
# local database is read from ts1database.txt, ts2database.txt, and rsdatabase.txt
# print responses in rsresponses.txt, ts1responses.txt, ts2responses.txt, resolved.txt


# FLAGS: aa = authoritative, arrived directly from authoritative name server/local database
#        ra = response was constructed through recursive resolution by RS
#        ns = DNS response did not fully resolve, directing client to TLD for iterative
#        nx = non-existent, IP Address returned should be 0.0.0.0

import threading
import time
import socket
import sys

def get_flag(request):
    List = request.split()
    return List[len(List)-1]

def build_response(domain_name, IP, i, flag):
    i = i+1
    return '1 ' + domain_name + " " + IP + " " + i + " " + flag

def ts2():
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
    print("[TS2]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS2]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[TS2]: Got a connection request from a client/server at {}".format(addr))

    #read in local database
    with open("ts2database.txt", "r") as ts2_file:
        entries = ts2_file.readlines()
    #print response in ts2responses.txt
    
    # princeton.com 192.1.1.7
    # www.google.com 9.7.5.6
    # test input
    #request = "www.google.com 9.7.5.6 1 it"

    request = csockid.recv(200)
    request = request.decode('utf-8')

    # incoming request from client/server: 1 DomainName IPAddress identification flags
    # split request into variables
    split_request = request.split()
    name = split_request[1]     #DomainName
    i = split_request[2]        #request IP
    #flag = split_request[len(split_request)-1]

    # traverse the entries from the ts2database.txt to see if any match the request
    is_found = 0        #internal flag for name found in entries, if 0 then will sends nx
    for entry in entries:
        # entries will read: princeton.com 192.1.1.7        DomainName IPAddress
        # incoming request from client/server: 1 DomainName IPAddress identification flags
        split_entry = entry.split()
        entry_name = split_entry[0]     #entry DomainName
        IP = split_entry[1]             #entry IP

        # if request matches any entries, sends aa
        if name == entry_name:
            # build response
            response = build_response(entry_name, IP, i, 'aa')
            csockid.send(response.encode('utf-8'))
            testresponse = response.decode('utf-8')
            #out_file.write(response + "\n")
            print("if AA " +testresponse + "\n")
            is_found = 1
    # if request not found in TS entries, send back 0.0.0.0 with nx
    if is_found == 0:
        testresponse = response.decode('utf-8')
        #out_file.write(response + "\n")
        print("if NX " +testresponse + "\n")
        response = build_response(name, '0.0.0.0', i, 'nx')
        csockid.send(response.encode('utf-8'))
    #Close the server socket
    #ss.close()
    #exit()

if __name__ == "__main__":
    t2 = threading.Thread(name='ts2', target=ts2)
    t2.start()
