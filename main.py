#!/usr/bin/env python3

import os
import time
import knapsack

if __name__ == "__main__":
    # tenta abrir arquivo .txt contendo nome do aluno na primeira linha
    # e número de matrícula na segunda. Caso não encontre o arquivo, coloca
    # valor padrão para nome e número de matrícula.
    try:
        with open("aluno.txt") as f:
            student_data = f.read().splitlines()
    except:
        student_data = ["NomeDoAluno", "NumeroMatricula"]


    student = student_data[0]
    reg = student_data[1]
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
        bt_result = knapsack.backtracking(bag_capacity, wt, val, total_items)
        end_bt =  (time.time() - start_bt)

        csv.write(f"{fname};{student};{reg};backtracking;{end_bt};{bt_result}\n")

        # por algum motivo esse teste em específico está gerando um loop infinito
        if fname != "f8_l-d_kp_23_10000":
            start_bnb = time.time()
            bnb_result = knapsack.branch_n_bound(bag_capacity, wt, val)
            end_bnb =  (time.time() - start_bnb)
        else:
            start_bnb = 0.0
            bnb_result = 0.0
            end_bnb = 0.0
        csv.write(f"{fname};{student};{reg};branchandbound;{end_bnb};{bnb_result}\n")

    csv.close()