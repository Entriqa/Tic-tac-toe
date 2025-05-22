import zmq
import os
from main import game

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)
clear = lambda: os.system('clear')

print(game.get_board())
while True:
    game = socket.recv_pyobj()
    if game.winner:
        print('Вы проиграли')
        break
    if game.draw:
        print('Ничья')
        break
    clear()

    print(game.get_board())
    print('Введите номер клетки, в которую вы хотите поставить нолик')
    move = int(input())
    game.player_move(0, move)
    clear()
    print(game.get_board())
    if game.winner:
        print('Вы выиграли')
        socket.send_pyobj(game)
        break
    if game.draw:
        print('Ничья')
        break

    socket.send_pyobj(game)

