import zmq

from client_client_connection.TicTakToe import Game

import os


port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)
clear = lambda: os.system('clear')

game = Game()
while True:
    clear()

    print(game.get_board())
    if game.winner:
        print('Вы проиграли')
        break
    if game.draw:
        print('Ничья')
        break

    print('Введите номер клетки, в которую вы хотите поставить крестик')
    move = int(input())
    game.player_move(1, move)
    clear()
    print(game.get_board())
    socket.send_pyobj(game)
    if game.winner:
        print('Вы выиграли')
        break
    if game.draw:
        print('Ничья')
        break
    game = socket.recv_pyobj()

