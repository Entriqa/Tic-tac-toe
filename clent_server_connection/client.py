import os
import socket
from server import games

clear = lambda: os.system('clear')


def connect_to_game_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            board = client_socket.recv(1024).decode()
            if board.endswith('  '):
                clear()
                print(board[:-2])
            else:
                if "wins" in board:
                    print(board)
                    break
                clear()
                print(board[:-2])

                move = input("Enter your move (cage number): ")
                client_socket.sendall(move.encode())
    finally:
        client_socket.close()


if __name__ == "__main__":
    server_host = '127.0.0.1'
    server_port = 1234
    connect_to_game_server(server_host, server_port)