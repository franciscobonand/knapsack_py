#!/usr/bin/env python3
import os
import time

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
    
    csv = open("result.csv", "w+")
    csv.write("Arquivo;Aluno;Tempo(s);Resultado\n")
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

        start_time = time.time()
        bt_result = kp_bt(bag_capacity, wt, val, total_items)
        end_time =  (time.time() - start_time)

        csv.write(f"{fname};{student};{end_time};{bt_result}\n")

    csv.close()