import csv
import sys
import numpy
from scipy import stats

name_bact=dict()
with open('bacteria_def.csv') as bacteria_file:
    reader_b = csv.reader(bacteria_file)
    for row in reader_b:
        name_bact[row[0]] = row[1]

ast_sp=dict()
ast_gen=dict()
with open("atb_ana.csv") as atb_file:
    reader_atb = csv.reader(atb_file, delimiter=';')
    atb_list = next(reader_atb)[3:]
    atb_dict=dict()
    for x in atb_list:
        atb_dict[x]=atb_list.index(x)
    for row in reader_atb:
        if row[1] not in ast_gen:
            new_genus=dict()
            for y in atb_list:
                new_genus[y] = {"S":0,"R":0,"I":0,"T":0}
                ast_gen[row[1]] = new_genus
        if row[2] not in ast_sp:
            new_sp=dict()
            for y in atb_list:
                new_sp[y] = {"S":0,"R":0,"I":0,"T":0}
                ast_sp[row[2]] = new_sp
        for z in atb_dict:
            if row[3:][atb_dict[z]] != "":
                ast_gen[row[1]][z]["T"] += 1
                ast_sp[row[2]][z]["T"] += 1
                ast_gen[row[1]][z][row[3:][atb_dict[z]]] += 1
                ast_sp[row[2]][z][row[3:][atb_dict[z]]] += 1


ast_header=[]
for x in atb_list:
    ast_header.extend([str(x)+" S"])
    ast_header.extend([str(x)+" S (%)"])
    ast_header.extend([str(x)+" I"])
    ast_header.extend([str(x)+" I (%)"])
    ast_header.extend([str(x)+" R"])
    ast_header.extend([str(x)+" R (%)"])
    ast_header.extend([str(x)+" total"])
ast_header.insert(0,"name")
with open("ast_per_genus.csv", 'w', newline="") as atb_file:
    writer_atb = csv.writer(atb_file, delimiter=';')
    writer_atb.writerow(ast_header)
    for x in ast_gen:
        new_ast=[]
        new_ast.extend([x])
        for y in atb_list:
            num_ast=0
            for z in ("S","I","R"):
                new_ast.extend([ast_gen[x][y][z]])
                num_ast += ast_gen[x][y][z]
                try:
                    new_ast.extend([round(ast_gen[x][y][z]/ast_gen[x][y]["T"]*100,1)])
                except ZeroDivisionError:
                    new_ast.extend([0])
            new_ast.extend([num_ast])
        writer_atb.writerow(new_ast)
with open("ast_per_sp.csv", 'w', newline="") as atb_file:
    writer_atb = csv.writer(atb_file, delimiter=';')
    writer_atb.writerow(ast_header)
    for x in ast_sp:
        new_ast=[]
        new_ast.extend([str(name_bact[x])])
        for y in atb_list:
            num_ast=0
            for z in ("S","I","R"):
                new_ast.extend([ast_sp[x][y][z]])
                num_ast += ast_sp[x][y][z]
                try:
                    new_ast.extend([round(ast_sp[x][y][z]/ast_sp[x][y]["T"]*100,1)])
                except ZeroDivisionError:
                    new_ast.extend([0])
            new_ast.extend([num_ast])
        writer_atb.writerow(new_ast)
