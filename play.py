"""Playing script for the network."""

from __future__ import print_function

import os
import numpy as np
import chess.pgn


def replace_tags(board):
    board_san = board.split(" ")[0]
    board_san = board_san.replace("2", "11")
    board_san = board_san.replace("3", "111")
    board_san = board_san.replace("4", "1111")
    board_san = board_san.replace("5", "11111")
    board_san = board_san.replace("6", "111111")
    board_san = board_san.replace("7", "1111111")
    board_san = board_san.replace("8", "11111111")
    for i in range(len(board.split(" "))):
        if i > 0 and board.split(" ")[i] != '' and i == 1:
            board_san += board.split(" ")[i]
    return board_san


def main():
    print('\nPlaying...\nComputer plays white.\n')
    board = chess.Board()
    while(not board.is_game_over()):
        # We get the movement prediction
        game_state = " ".join(replace_tags(board.fen()))

        y = np.array([game_state])

        with open("nmt/datasets/nmt_data/infer_movement.gm", 'w+') as f_handle:
            np.savetxt(f_handle, y.reshape(1, y.shape[0]), delimiter="", newline="\n", fmt="%s")

        os.system("python -m nmt.nmt --src=gm --tgt=mv --vocab_prefix=nmt/datasets/nmt_data/vocab --train_prefix=nmt/datasets/nmt_data/train  --dev_prefix=nmt/datasets/nmt_data/dev  --test_prefix=nmt/datasets/nmt_data/test  --out_dir=nmt/nmt_model  --num_train_steps=25000  --steps_per_stats=100  --num_layers=2  --num_units=128  --dropout=0.2 --attention_architecture=gnmt --inference_input_file=nmt/datasets/nmt_data/infer_movement.gm --inference_output_file=nmt/datasets/nmt_data/output_infer >/dev/null 2>&1")

        with open("nmt/datasets/nmt_data/output_infer") as f:
            content = f.readlines()

        movements = [x.strip() for x in content]

        movement = "".join(movements[0].split())
        print('The computer wants to move to:', movement)
        try:
            if(board.parse_san(movement) in board.legal_moves):
                print ("and it's a valid movement :).")
                board.push_san(movement)
                print("\n")
                print(board)
                print("\n")
            else:
                print("but that is NOT a valid movement.")
        except:
            print ("but that is NOT a valid movement :(.")

        # we move now
        moved = False
        while not moved:
            try:
                movement = raw_input('Enter your movement: ')
                if(board.parse_san(movement) in board.legal_moves):
                    print ("That is a valid movement.")
                    board.push_san(movement)
                    print("\n")
                    print(board)
                    print("\n")
                    moved = True
                else:
                    print ("That is NOT a valid movement :(.")
            except:
                print ("but that is NOT a valid movement :(.")
    print("\nEnd of the game.")
    print("Game result:")
    print(board.result())


if __name__ == '__main__':
    main()
