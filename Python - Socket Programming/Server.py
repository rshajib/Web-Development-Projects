import socket
import threading

SYN = 'SYN'
ACK = 'ACK'
ACK_SYN = 'ACK+SYN'
FIN = 'FIN'
ACK_FIN = 'ACK+FIN'


def each_connection(c, addr):
    is_finishing = False
    print(str(addr) + 'Connected')
    while True:
        msg_recv = c.recv(2048).decode()
        if msg_recv == SYN:
            print(str(addr) + 'Recieved: ' + msg_recv)
            msg_send = ACK_SYN
            c.send(msg_send.encode())
            print(str(addr) + 'Server sent', msg_send)
        elif msg_recv.startswith(ACK) and not is_finishing:
            print(str(addr) + 'Recieved: ', msg_recv)
            file_name = msg_recv[3:]
            if len(file_name) > 0:
                print('got ', file_name)
                f = open('server_files/' + file_name, 'r')
                file_content = f.read()
                f.close()
                print(str(addr) + 'File contents read')
                c.send(file_content.encode())
                print(str(addr) + 'Sending: ' + file_content)
        elif msg_recv == FIN:
            print(str(addr) + 'Recieved: ' + msg_recv)
            msg_send = ACK_FIN
            c.send(msg_send.encode())
            print(str(addr) + 'Server sent', msg_send)
            is_finishing= True
        elif msg_recv == ACK and is_finishing:
            break
        else:
            break
    c.close()
    print(str(addr) + 'Connection closed')


def prepare_html():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Page Title</title>
    </head>
    <body>
    <h1>This is a Heading</h1>
    <p>This is a paragraph.</p>
    </body>
    </html>'''
    return html


# next create a socket object
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our case it is 12345 but it can be anything
port = 12344

# Next bind to the port. we have not typed any ip in the ip field
# instead we have inputted an empty string this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)
print("socket is listening")

while True:
    c, addr = s.accept()
    threading.Thread(target=each_connection, args=(c, addr)).start()

    print('Got connection from', addr)
