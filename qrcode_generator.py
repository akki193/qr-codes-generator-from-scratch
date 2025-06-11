#!/usr/bin/env python3
#qr code generator from scratch

import numpy as np
import matplotlib.pyplot as plt

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
    
    def plot_qr_structure(self, binary_seq, returns=False):
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
                    arr[14:20, i] = 1

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

        plt.imshow(arr, cmap="Greys")
        plt.show()
        if returns: return arr

    



            

        


    
x = QRgen()
text = "Hello, world"
bseq = x.binary_encoding(text)
x.plot_qr_structure(bseq)
