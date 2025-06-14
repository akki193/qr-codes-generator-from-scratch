#!/usr/bin/env python3
#qr code generator from scratch

import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

class QRgen():
    """
    qr size: 21x21
    ???error correction: Level Q(~25%)???
    mask formula: ((i*j)%3+i+j)%2==0
    data encoding type: bytes
    """

    def __init__(self):
        pass

    def binary_encoding(self, text):
        ascii_seq = np.frombuffer(text.encode("ascii"), dtype='uint8')
        binary_seq = np.array(list("".join(map(lambda x: "{:08b}".format(x), ascii_seq))), dtype='uint8')

        return binary_seq
    
    def binary_decoding(self, binary_seq):
        ascii_seq = np.packbits(binary_seq)
        text = ascii_seq.tobytes().decode('ascii')

        return text
    
    def plot_qr_structure(self, binary_seq, grey_markup=False):
        arr = np.zeros((21, 21))
        for i in range(21):
            if 0<=i<=6 or 14<=i<=20:
                arr[0, i] = 1
                arr[6, i] = 1
                if 0<=i<=6:
                    arr[14, i] = 1
                    arr[20, i] = 1

            if i % 2 == 0:
                arr[6, i] = 1
                arr[i, 6] = 1
            if i in [0, 6, 14, 20]:
                arr[0:6, i] = 1
                if i in [0, 6]:
                    arr[14:20, i] = 1#6,8

            if i in [2, 3, 4, 16, 17, 18]:
                arr[2:5, i] = 1
                if i in [2, 3, 4]:
                    arr[16:19, i] = 1

            if arr[8, i] == 0 and not i in [9, 10, 11, 12]: 
                arr[8, i] = 0.5
            if arr[i, 8] == 0 and not i in [9, 10, 11, 12]:
                arr[i, 8] = 0.5
        arr[13, 8] = 1
        arr[-1, -2] = 1

        if grey_markup:
            arr = np.where(arr == 1, 0.5, arr)

        return arr

    def plot_data(self, arr, bseq, moves_):
        colored_blocks = []
        move_history = []
        row, col = 18, 20

        for move_name, dir in moves_:
            move_history.append(move_name)

            try:
                if move_history[-2] == 'u' and move_history[-1] == 'l':
                    row -= 1
                elif move_history[-2] == 'l' and move_history[-1] == 'd':
                    row += 2
                    col += 2
                elif move_history[-2] == 'd' and move_history[-1] == 'l':
                    row += 0
                    col += 0
                elif move_history[-2] == 'l' and move_history[-1] == 'u':
                    row -= 1
                    col += 2
            except: pass

            for bit, move in zip(bseq, dir):
                arr[row, col] = bit
                colored_blocks.append((row, col))
                print(f"colored: {row};{col}")

                if move[2] > move[3]:
                    row -= 1
                elif move[2] < move[3]: 
                    row += 1
                if move[0] > move[1]:
                    col -= 1
                elif move[0] < move[1]:
                    col += 1


                    




        print(f"double colored blocks: {len(colored_blocks) != len(set(colored_blocks))}")






    



            
x = QRgen()
text = "Hello, world"
#bseq = x.binary_encoding(text)
bseq = np.array([i/8 for i in range(32)])
bytes_amount = bseq.size//8
   
#left, right, up, down
byte_move_up = ('u', [(1, 0, 0, 0), (0, 1, 1, 0)]*4)
byte_move_left = ('l', [(0, 0, 0, 1), (1, 0, 1, 0)]*4)
byte_move_down = ('d', [(1, 0, 0, 0), (0, 1, 0, 1)]*4)
moves= [byte_move_up, byte_move_up, byte_move_left, byte_move_down, byte_move_down, byte_move_left, byte_move_up, byte_move_up, byte_move_left, byte_move_down, byte_move_down, byte_move_left, byte_move_up, byte_move_up, byte_move_up]
moves = moves[:bytes_amount*8]



print(bseq)
print(bytes_amount)
print(moves)

arr = x.plot_qr_structure(bseq, grey_markup=True)
x.plot_data(arr, bseq, moves)
plt.imshow(arr, cmap="Greys")
plt.show()


