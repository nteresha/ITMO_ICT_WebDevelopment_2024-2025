import socket


def quadratic_equation(a, b, c):
    discr = b ** 2 - 4 * a * c
    if discr > 0:
        x1 = (-b + discr ** 0.5) / (2 * a)
        x2 = (-b - discr ** 0.5) / (2 * a)
        return str(x1)+str(' ')+ str(x2)
    elif discr == 0:
        x = -b / (2 * a)
        return str(x)
    else:
        return "No solution"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", 1234))
    server_socket.listen()
    print("Server started")
    client_connection, client_address = server_socket.accept()
    with client_connection:
        client_message = client_connection.recv(1024).decode()
        a, b, c = client_message.split(',')
        client_connection.sendall(str(quadratic_equation(float(a), float(b), float(c))).encode())
        print("Client got the result")