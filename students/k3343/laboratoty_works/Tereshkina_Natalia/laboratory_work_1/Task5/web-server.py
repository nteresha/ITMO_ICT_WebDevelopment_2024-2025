import socket
import threading


grades = {}


def generate_html():
    response = """
    <html>
    <head>
        <title>Disciplines grades</title>
        <style>
            body {
                font-family: 'Verdana', sans-serif;
                margin: 40px;
                background-color: #eef2f3;
            }
            table {
                width: 60%;
                border-collapse: collapse;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            table, th, td {
                border: 1px solid #ccc;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #4a90e2;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #4CAF50;
            }
            form {
                margin-top: 20px;
                background: #fff;
                padding: 20px;
                border-radius: 8px; 
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }
            input[type="text"] {
                margin: 5px 0;
                padding: 10px;
                width: 100%;
                border: 1px solid #bbb;
                border-radius: 5px;
                box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            input[type="submit"] {
                padding: 5px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <h1>Disciplines grades</h1>
        <table>
            <tr>
                <th>Discipline</th>
                <th>Grade</th>
            </tr>
    """
    for subject, grade_list in grades.items():
        grades_str = ', '.join(grade_list)
        response += f"<tr><td>{subject}</td><td>{grades_str}</td></tr>"

    response += """
        </table>
        <h2>Add new grade</h2>
        <form method="POST">
            Discipline: <input type="text" name="subject"><br>
            Grade: <input type="text" name="grade"><br>
            <input type="submit" value="Add">
        </form>
    </body>
    </html>
    """
    return response


def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    headers = request.split('\r\n')
    if len(headers) > 0:
        request_line = headers[0]
        method, path, _ = request_line.split()

        if method == 'GET':
            response_body = generate_html()
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            client_socket.sendall((response_headers + response_body).encode())

        elif method == 'POST':
            body = request.split('\r\n\r\n')[1]
            params = dict(param.split('=') for param in body.split('&'))
            subject = params.get('subject', '').replace('+', ' ')
            grade = params.get('grade', '')
            if subject and grade:
                if subject in grades:
                    grades[subject].append(grade)
                else:
                    grades[subject] = [grade]

            response_headers = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
            client_socket.sendall(response_headers.encode())

    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen()
print("Server started")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()