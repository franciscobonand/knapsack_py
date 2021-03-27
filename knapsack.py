#!/usr/bin/env python3

def backtracking(max_wt, wt_list, val_list, n_items): 
    # Caso quando a capacidade da mochila ou o peso total buscado são 0
    if n_items == 0 or max_wt == 0 :
        return 0
    # Caso o último item da lista exceda o valor total, ele é removido das opções válidas 
    if wt_list[n_items-1] > max_wt : 
        return backtracking(max_wt, wt_list, val_list, n_items-1)
    else:
        # Peso atingido quando inclui-se item da lista
        wt_with_item = val_list[n_items-1] + backtracking(max_wt-wt_list[n_items-1], wt_list, val_list, n_items-1)
        # Peso atingido quando item da lista não é incluído
        wt_without_item = backtracking(max_wt, wt_list, val_list, n_items-1)

        return max(wt_with_item, wt_without_item)


def branch_n_bound(max_wt, wt_list, val_list):
    val_wts = sorted(zip(wt_list, val_list), key=sort_tuple_list, reverse=True)
    # inicia árvore vazia e lista de nós a serem explorados
    root = Node(0, 0, 0, [0] * len(val_wts), val_wts, max_wt)
    current_state = root
    states_to_explore = []

    while current_state.level < len(val_wts):
        # pega nós a serem explorados a partir do nó atual
        states_to_explore.extend(current_state.search_next(val_wts, max_wt))
        # ordena a lista de nós a serem explorados de acordo com a upperbound
        states_to_explore.sort(key=lambda x: x.up)
        # explora nó de maior upperbound e remove-o da lista de nós a serem explorados
        current_state = states_to_explore.pop()

    return current_state.total_value

class Node(object):
    def __init__(self, level, total_value, weight, done, val_wts, max_wt):
        self.level = level
        self.total_value = total_value
        self.weight = weight
        # done representa a lista de nós que foram/não foram incluídos pelo 
        # caminho até o nó atual
        self.done = done
        self.up = Node.upperbound(self.done[:self.level]+[1]*(len(val_wts)-level), val_wts, max_wt)

    @staticmethod
    # calcula a upperbound dos nós a fim de definir qual será o próximo a ser 
    # explorado pelo algoritmo branch and bound
    def upperbound(available, val_wts, max_wt):
        upperbound = 0
        capacity = max_wt
        for av, (wt, val) in zip(available, val_wts):
            tmp_wt =  wt * av
            if tmp_wt <= capacity:
                capacity -= tmp_wt
                upperbound += val * av
            else:
                upperbound += val * capacity / tmp_wt
                break
        return upperbound

    
    def search_next(self, val_wts, max_wt):
        level = self.level + 1
        weight, value = val_wts[self.level]
        left_weight = self.weight + weight
        if left_weight <= max_wt:  # if not overweighted, give left child
            left_total_value = self.total_value + value
            left_done = self.done[:self.level]+[1]+self.done[level:]
            left_child = Node(level, left_total_value, left_weight, left_done, val_wts, max_wt)
        else:
            left_child = None
        # anyway, give right child
        right_child = Node(level, self.total_value, self.weight, self.done, val_wts, max_wt)
        return ([] if left_child is None else [left_child]) + [right_child]


def sort_tuple_list(tupl):
    return tupl[1]/tupl[0]

def number_size_order(numbr):
    return len(str(numbr).split(".")[0])