import socket
import threading
from TicTakToe import Game, PlayerType

HOST = '127.0.0.1'
PORT = 1234

games = []
game_lock = threading.Lock()


def handle_player_connection(player_socket, game, player_type, turn_lock):
    try:
        while True:
            with turn_lock:
                # Ждем своей очереди
                while game.current_turn != player_type:
                    turn_lock.wait()
                if game.winner is not None:
                    player_socket.sendall(f"Player {game.winner.name} wins!".encode())
                    break
                if game.draw:
                    player_socket.sendall(f"Nobody wins!".encode())
                    break
                player_socket.sendall((game.get_board() + 'no').encode())


                data = player_socket.recv(1024).decode()
                if not data:
                    break

                cage_number = int(data)
                move_success = game.player_move(player_type, cage_number)

                if move_success:
                    # Обновляем текущего игрока
                    game.current_turn = PlayerType.noughts if game.current_turn == PlayerType.crosses else PlayerType.crosses
                    turn_lock.notify_all()
                    player_socket.sendall((game.get_board() + '  ').encode())
                    if game.winner is not None:
                        player_socket.sendall(f"Player {game.winner.name} wins!".encode())
                        break
                    if game.draw:
                        player_socket.sendall(f"Nobody wins!".encode())
                        break




    finally:
        player_socket.close()


def start_game(player_sockets):
    game = Game()
    games.append(game)
    turn_lock = threading.Condition()

    threading.Thread(target=handle_player_connection,
                     args=(player_sockets[0], game, PlayerType.crosses, turn_lock)).start()
    threading.Thread(target=handle_player_connection,
                     args=(player_sockets[1], game, PlayerType.noughts, turn_lock)).start()


def main_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        player_sockets = []

        for _ in range(2):
            player_socket, player_address = server_socket.accept()
            print(f"Player connected from {player_address}")

            player_sockets.append(player_socket)

        start_game(player_sockets)


if __name__ == "__main__":
    main_server()