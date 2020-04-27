import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 5002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


def process_csv_ip_request(request: bytes):
    parsed = request.decode('ASCII').split(',')

    username, password, asd_id, message = parsed

    print(username)
    print(password)
    print(asd_id)
    print(message)

    print('message:')

    message_format = message[0:2]

    if message_format != '18':
        print('Message format not supported, need 18, got {}'.format(message_format))
        return

    # 1 = new event or opening, 3 = new restore or closing, 6 = previous event
    event_qualifier = message[2]

    # 3 hex digits
    event_code = message[3:6]

    # 2 hex digits, can be 0 for no info (then only one digit)
    group_number = message[6:9]

    # 3 hex digits, can be 0 for no info (then only one digit)
    device_or_sensor_number = message[9:13]

    print(message_format)
    print(event_qualifier)
    print(event_code)
    print(group_number)
    print(device_or_sensor_number)


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print('Received {}'.format(request))
    process_csv_ip_request(request)
    client_socket.send(b'ACK!')
    client_socket.close()


while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        args=(client_sock,)
    )
    client_handler.start()
