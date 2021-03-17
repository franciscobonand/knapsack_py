#!/usr/bin/env python3
import os
import time

def kp_bt(max_wt, wt_list, val_list, n_items): 
    table = [[0 for x in range(max_wt + 1)] for x in range(n_items + 1)]
    print(table)
    print("nxt")
    # Build table table[][] in bottom up manner 
    for i in range(n_items + 1): 
        for w in range(max_wt + 1): 
            if i == 0 or w == 0: 
                table[i][w] = 0
            elif wt_list[i-1] <= w: 
                table[i][w] = max(val_list[i-1] + table[i-1][w-wt_list[i-1]],  table[i-1][w]) 
            else: 
                table[i][w] = table[i-1][w]
        print(table)
        print("nxt")
  
    return table[n_items][max_wt] 

if __name__ == "__main__":
    student = "Francisco Bonome Andrade"
    dirpath, _, filenames = next(os.walk("tests/"))
    
    csv = open("result.csv", "w+")
    for fname in filenames[3:4]:
        total_items = int(fname.split("_")[3])
        bag_capacity = int(fname.split("_")[4])
        with open(dirpath+fname) as f:
            items = f.read().splitlines()
        
        val, wt = [], []
        aux_list = [i.split(" ") for i in items]
        for v,w in aux_list:
            if "." in v or "." in w:
                val.append(float(v))
                wt.append(float(w))
            else:
                val.append(int(v))
                wt.append(int(w))

        start_time = time.time()
        bt_result = kp_bt(bag_capacity, wt, val, total_items)
        end_time =  (time.time() - start_time)
        
        csv.write(f"{fname};{student};{end_time};{bt_result}\n")

    csv.close()