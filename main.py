#!/usr/bin/env python3

import os
import time

def sort_tuple_list(tupl):
    return tupl[1]/tupl[0]

class State(object):
    def __init__(self, level, benefit, weight, token, data_sorted, max_wt):
        # token = list marking if a task is token. ex. [1, 0, 0] means
        # item0 token, item1 non-token, item2 non-token
        # available = list marking all tasks available, i.e. not explored yet
        self.level = level
        self.benefit = benefit
        self.weight = weight
        self.token = token
        self.ub = State.upperbound(self.token[:self.level]+[1]*(len(data_sorted)-level), data_sorted, max_wt)

    @staticmethod
    def upperbound(available, data_sorted, max_wt):  # define upperbound using fractional knaksack
        upperbound = 0  # initial upperbound
        # accumulated weight used to stop the upperbound summation
        remaining = max_wt
        for avail, (wei, val) in zip(available, data_sorted):
            wei2 =  wei * avail  # i could not find a better name
            if wei2 <= remaining:
                remaining -= wei2
                upperbound += val * avail
            else:
                upperbound += val * remaining / wei2
                break
        return upperbound

    def develop(self, data_sorted, max_wt):
        level = self.level + 1
        weight, value = data_sorted[self.level]
        left_weight = self.weight + weight
        if left_weight <= max_wt:  # if not overweighted, give left child
            left_benefit = self.benefit + value
            left_token = self.token[:self.level]+[1]+self.token[level:]
            left_child = State(level, left_benefit, left_weight, left_token, data_sorted, max_wt)
        else:
            left_child = None
        # anyway, give right child
        right_child = State(level, self.benefit, self.weight, self.token, data_sorted, max_wt)
        return ([] if left_child is None else [left_child]) + [right_child]


def doStuff(max_wt, wt_list, val_list):
    data_sorted = sorted(zip(wt_list, val_list), key=sort_tuple_list, reverse=True)

    Root = State(0, 0, 0, [0] * len(data_sorted), data_sorted, max_wt)  # start with nothing
    waiting_States = []  # list of States waiting to be explored
    current_state = Root
    while current_state.level < len(data_sorted):
        waiting_States.extend(current_state.develop(data_sorted, max_wt))
        # sort the waiting list based on their upperbound
        waiting_States.sort(key=lambda x: x.ub)
        # explore the one with largest upperbound
        current_state = waiting_States.pop()

    return current_state.benefit

def kp_bt(max_wt, wt_list, val_list, n_items): 
    # Caso quando a capacidade da mochila ou o peso total buscado são 0
    if n_items == 0 or max_wt == 0 :
        return 0
    
    # Caso o último item da lista exceda o valor total, ele é removido das opções válidas 
    if wt_list[n_items-1] > max_wt : 
        return kp_bt(max_wt, wt_list, val_list, n_items-1)
    else:
        # Peso atingido quando inclui-se item da lista
        wt_with_item = val_list[n_items-1] + kp_bt(max_wt-wt_list[n_items-1], wt_list, val_list, n_items-1)
        # Peso atingido quando item da lista não é incluído
        wt_without_item = kp_bt(max_wt, wt_list, val_list, n_items-1)

        return max(wt_with_item, wt_without_item) 

if __name__ == "__main__":
    student = "Francisco Bonome Andrade"
    reg = "2016006450"
    dirpath, _, filenames = next(os.walk("tests/"))

    csv = open("result.csv", "w+")
    csv.write("Arquivo;Aluno;Matricula;Algoritmo;Tempo(s);Resultado\n")
    for fname in filenames:
        with open(dirpath+fname) as f:
            items = f.read().splitlines()
        
        val, wt = [], []
        first_index = True
        aux_list = [i.split(" ") for i in items]
        for v,w in aux_list:
            if first_index:
                first_index = False
                total_items = int(v)
                bag_capacity = int(w)
                continue 

            val.append(float(v))
            wt.append(float(w))

        start_bt = time.time()
        bt_result = kp_bt(bag_capacity, wt, val, total_items)
        end_bt =  (time.time() - start_bt)

        csv.write(f"{fname};{student};{reg};backtracking;{end_bt};{bt_result}\n")

        if fname != "f8_l-d_kp_23_10000":
            start_bnb = time.time()
            bnb_result = doStuff(bag_capacity, wt, val)
            end_bnb =  (time.time() - start_bnb)
        else:
            start_bnb = 0.0
            bnb_result = 0.0
            end_bnb = 0.0
        csv.write(f"{fname};{student};{reg};branchandbound;{end_bnb};{bnb_result}\n")

    csv.close()