import threading
import time
import random

import socket

import sys

def get_flag(request):
    List = request.split()
    return List[len(List)-1]

def build_request(host_name, i, flag):
    return '0 ' + host_name + " " + str(i) + " " + flag

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    RS_addr = socket.gethostbyname(sys.argv[1])
    port = int(sys.argv[2])

    # connect to the root server
    server_binding = (RS_addr, port)
    cs.connect(server_binding)

    # creates a list of requests
    with open('hostnames.txt', 'r') as in_file:
        requests = in_file.readlines()

    in_file.close()

    with open('resolved.txt', 'w') as out_file:

        # starts DNS resolution for each request
        i = 1
        for request in requests:
            flag = get_flag(request)
            request_list = request.split()
            host_name = request_list[0]
            
            # recursive DNS
            if flag == 'rd':

                # ideally, the DNS servers are configured correctly and client only gets one response to print
                request = build_request(host_name, i, flag)
                cs.send(request.encode('utf-8'))
                response = cs.recv(200)
                response = response.decode('utf-8')
                print(response + "\n")
                i = i + 1

            # iterative DNS
            elif flag == 'it':

                # the while loop condition checks if the flag is nx or aa
                # nx or aa means that the iterative DNS has ended
                # if nx and aa aren't the flag of the response, continue DNS
                # else, just print the response
                while flag != 'nx' and flag != 'aa':
                    request = build_request(host_name, i, 'it')
                    cs.send(request.encode('utf-8'))
                    response = cs.recv(200)
                    response = response.decode('utf-8')
                    flag = get_flag(response)
                    out_file.write(response + "\n")
                    List = response.split()
                    # ts_domain = List[2]
                    ts_addr = List[3]
                    cs.connect(ts_addr, port)
                    i = i + 1
                else:
                    out_file.write(response + "\n")
                    i = i + 1

            # this shouldn't happen    
            else:
                print('Bruh')
                quit()

    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":

    # time.sleep(random.random() * 5)
    c1 = threading.Thread(name='client', target=client)
    c1.start()

    # time.sleep(5)
    print("Done.")
