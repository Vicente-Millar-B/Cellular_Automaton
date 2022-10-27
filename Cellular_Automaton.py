import matplotlib.pyplot as plt, numpy as np, time, os
from tqdm import tqdm

plt.style.use('dark_background')

class Cellular_Automaton(object):
    '''Example:

    >> from "path" import Cellular_Automaton
    >> import numpy as np
    >> 
    >> n = 50
    >>
    >> init_cond = np.zeros(2*n+1, dtype=int)
    >> init_cond[n] = 1
    >>
    >> CA = Cellular_Automaton(init_cond, 30, n)
    >>
    >> CA.Show()
    '''
    default_size = 1
    def __init__(self, init_cond, rule, steps, show_progress=False, coup_bord=True):
        self.DE = coup_bord
        if not isinstance(rule, int):
            msg = 'Rule type must be "int"'
            raise TypeError(msg)
        if rule > 255:
            msg = 'Rule value must be less than 256'
            raise ValueError(msg)
        self.rule = np.binary_repr(rule, width=8)
        self.it = steps
        self.matrix = [init_cond]
        if show_progress:
            for i in tqdm(range(steps-1)):
                a = self.Next_Row(init_cond, rule)
                self.matrix.append(a)
                init_cond = a
            time.sleep(1)
            print('-'*52)
        elif not show_progress:
            for i in range(steps-1):
                a = self.Next_Row(init_cond, self.rule)
                self.matrix.append(a)
                init_cond = a
    def Next_Row(self, row, rule):
        next_row = []
        for i in range(len(row)):
            this_dig = row[i]
            if i == 0:
                if self.DE: prev_dig = row[-1]
                else: prev_dig = 0
            else: prev_dig = row[i-1]
            if i == len(row)-1:
                if self.DE: next_dig = row[0]
                else: next_dig = 0
            else: next_dig = row[i+1]
            if prev_dig and this_dig and next_dig:
                next_row.append(int(rule[0]))
            if prev_dig and this_dig and not next_dig:
                next_row.append(int(rule[1]))
            if prev_dig and not this_dig and next_dig:
                next_row.append(int(rule[2]))
            if prev_dig and not this_dig and not next_dig:
                next_row.append(int(rule[3]))
            if not prev_dig and this_dig and next_dig:
                next_row.append(int(rule[4]))
            if not prev_dig and this_dig and not next_dig:
                next_row.append(int(rule[5]))
            if not prev_dig and not this_dig and next_dig:
                next_row.append(int(rule[6]))
            if not prev_dig and not this_dig and not next_dig:
                next_row.append(int(rule[7]))
        return np.array(next_row)
    def Show(self, cmap='gray'):
        size = Cellular_Automaton.default_size*5
        plt.rcParams["figure.figsize"] = (size, size)
        plt.axis('off')
        plt.imshow(self.matrix, cmap=cmap)
        plt.show()
