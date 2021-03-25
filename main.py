#!/usr/bin/env python3

# TODO: Adicionar contador do valor atual de cada nó
# Problema -> Nós com o mesmo custo, mas se um exceder
# o peso total quando somar seu filho deve-se optar pelo outro

import os
import time

def sort_tuple_list(tupl):
    return tupl[0]/tupl[1]

def sort_by_ratio(values, weights):
    val_wts = list(zip(values, weights))
    val_wts.sort(reverse=True, key=sort_tuple_list)
    return val_wts

def minimum_node(tupl):
    return tupl[0].cost

class Node:
    def __init__(self, index=-2, cost=1, included=False, valid=False):
        self.index = index
        self.cost = cost
        self.included = included
        self.childs = []
        self.valid = valid

    def add_node(self, child_node):
        self.childs.append(child_node)

    def find_lowest_cost(self, upper):
        if self.valid:
            if self.cost > upper:
                self.valid = False
                return 0
            elif len(self.childs) == 0:
                return self.cost
            else:
                return min(self.childs[0].find_lowest_cost(upper),
                            self.childs[1].find_lowest_cost(upper))
        return 0

    def get_lowest_cost_node(self, cost, excluded):
        if self.valid:
            if self.cost == cost and self.index != -1 and len(self.childs) == 0:
                return self, excluded
            elif len(self.childs) > 0:
                if not self.included:
                    excluded.append(self.index)
                return min(self.childs[0].get_lowest_cost_node(cost, excluded),
                            self.childs[1].get_lowest_cost_node(cost, excluded)
                            , key=minimum_node)
        return Node(), []

# get_cost_and_upper returns the cost and upper bound of the list of elements
# excluding those elements that are listed in 'ignore'
def get_cost_and_upper(ignore, max_wt, val_wts):
    curr_wt, cost, up = 0, 0, 0
    for i in range(0, len(val_wts)) :
        if i not in ignore:
            curr_wt += val_wts[i][1] # val_wts[i][1] são os pesos de cada tupla

            if curr_wt > max_wt:
                curr_wt -= val_wts[i][1]
                cost = up + (max_wt - curr_wt) * (val_wts[i][0] / val_wts[i][1])
                up = -up
                cost = -cost
                break
            else:
                up += val_wts[i][0]

            if curr_wt == max_wt:
                up = -up
                cost = up
                break
    
    return up, cost
    
def get_child_nodes(max_wt, val_wts, item_idx, min_upper, ignore):
    node_in, node_out = Node(), Node()
    ignored_plus_actual = ignore + [item_idx]
    up_wout, cost_wout = get_cost_and_upper(ignored_plus_actual, max_wt, val_wts)
    up_with, cost_with = get_cost_and_upper(ignore, max_wt, val_wts)

    loc_min_upper = min(up_wout, up_with)
    min_upper = min(min_upper, loc_min_upper)

    if cost_wout <= min_upper:
        node_out.index = item_idx
        node_out.cost = cost_wout
        node_out.included = False
        node_out.valid = True

    if cost_with <= min_upper:
        node_in.index = item_idx
        node_in.cost = cost_with
        node_in.included = True
        node_in.valid = True

    return node_in, node_out, min_upper

def bnb_recursive(min_upper, root, val_wts, max_wt, curr_node):
    lwst_cost = root.find_lowest_cost(min_upper)
    nxt_node, excl = root.get_lowest_cost_node(lwst_cost, [])
    
    if nxt_node.cost == curr_node.cost and  nxt_node.index == curr_node.index:
        return curr_node.cost
    elif nxt_node.index != -2 and nxt_node.index+1 < len(val_wts):
        node_in, node_out, min_upper = get_child_nodes(max_wt, val_wts, nxt_node.index+1, min_upper, excl)
        nxt_node.add_node(node_in)
        nxt_node.add_node(node_out)
        bnb_recursive(min_upper, root, val_wts, max_wt, nxt_node)
    return 

def kp_bnb(max_wt, wt_list, val_list, n_items):
    # Caso quando a capacidade da mochila ou o peso total buscado são 0
    if n_items == 0 or max_wt == 0 :
        return 0

    val_wts = sort_by_ratio(val_list, wt_list)
    min_upper = 0
    node_in, node_out, min_upper = get_child_nodes(max_wt, val_wts, 0, min_upper, list())
    root = Node(-1, node_in.cost, True, True)
    root.add_node(node_in)
    root.add_node(node_out)

    return bnb_recursive(min_upper, root, val_wts, max_wt, root)


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
    dirpath, _, filenames = next(os.walk("tests/"))

    # csv = open("result.csv", "w+")
    # csv.write("Arquivo;Aluno;Tempo(s);Resultado\n")
    for fname in filenames[3:4]:
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

        start_time = time.time()
        # bt_result = kp_bt(bag_capacity, wt, val, total_items)
        end_time =  (time.time() - start_time)

        kp_bnb(bag_capacity, wt, val, total_items)

    #     csv.write(f"{fname};{student};{end_time};{bt_result}\n")

    # csv.close()