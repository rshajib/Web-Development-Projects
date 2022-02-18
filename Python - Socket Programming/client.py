import socket
import sys

SYN = 'SYN'
ACK = 'ACK'
ACK_SYN = 'ACK+SYN'
FIN = 'FIN'
ACK_FIN = 'ACK+FIN'



def connect_to_google_server():
    # An example script to connect to Google using socket programming in Python

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    # default port for socket
    port = 80

    try:
        host_ip = socket.gethostbyname('www.google.com')
        print(host_ip)
    except socket.gaierror:

        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()

    # connecting to the server
    s.connect((host_ip, port))

    print("the socket has successfully connected to google")


#connect_to_google_server()


# def connect_to_our_server():
#     # Create a socket object
#     s = socket.socket()
#
#
def connect_to_QOTD_server():
    # An example script to connect to Google using socket programming in Python

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    # default port for socket
    port = 17

    try:
        host_ip = socket.gethostbyname('djxmmx.net')
    except socket.gaierror:

        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()

    # connecting to the server
    s.connect((host_ip, port))
    quote = s.recv(2048).decode()
    print("the quote is ", quote)


def connect_to_our_file_server(filenum):
    s = socket.socket()
    port = 12344
    s.connect(('127.0.0.1', port))

    msg_SYN = SYN
    s.send(msg_SYN.encode())
    msg_recv = s.recv(2048).decode()
    if msg_recv != ACK_SYN:
        print(ACK_SYN, 'not received! Received', msg_recv)
        s.close()
        return

    file_msg = 'file' + str(filenum) + ".txt"
    s.send((ACK + file_msg).encode())
    msg_recv = s.recv(2048).decode()
    print('client recieved', msg_recv)
    path = "C:/Users/Pc/Desktop"
    f = open(path + file_msg, "w")
    f.write(msg_recv)  # write file content that we recieved from server
    f.close()


    # s.send((FIN + file_msg).encode())
    # msg_recv = s.recv(2048).decode()
    # print(msg_recv)


    s.send(FIN.encode())
    print('Sending: ' + FIN)
    msg_recv = s.recv(2048).decode()
    print('Received:', msg_recv)
    s.close()
    if msg_recv == ACK_FIN:
        s.close()

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)

# connect_to_QOTD_server()
# connect_to_our_server(1)
connect_to_our_file_server(3)

