import socket

a = input("Enter the coef_a: ")
b = input("Enter the coef_b: ")
c = input("Enter the coef_c: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(("localhost", 1234))
    client_socket.sendall(f"{a}, {b}, {c}".encode())
    server_message = client_socket.recv(1024)

print(f"The solution of quadratic equation: {server_message.decode()}")