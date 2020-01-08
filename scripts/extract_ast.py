import csv
import sys
import pickle
from datetime import datetime, timedelta

# limits results to S, I, R or ""
def extd_atb(a):
    if a in ("S","R","I"):
        new_atb.extend(a)
    else:
        new_atb.extend([""])


list_bact=dict()
list_genus=dict()
with open('bacteria_def.csv') as bacteria_file:
    reader_b = csv.reader(bacteria_file)
    for row in reader_b:
        list_bact[row[0]] = row[2]
        list_genus[row[0]] = row[1].split(" ")[0]

with open('true_bacteriemia.pickle', 'rb') as datafile:
    bact = pickle.load(datafile)

list_atb=[]
with open('SIR_AST_results', newline='', encoding='iso-8859-1') as atb_file:
    atb_data = csv.reader(atb_file, delimiter=';')
    next(atb_data)
    next(atb_data)
    for row in atb_data:
        list_atb.append(row)

# extract AST results
atb_ana=[]
for x in bact:
    if list_bact[x[0]] in ("3","4"):
        for y in list_atb:
            if x[-1] == y[2] and x[0] == y[7]:
                new_atb=[]
                new_atb.extend([y[2],list_genus[y[7]],y[7]])
                if y[10] in ("S","R","I"): # choix entre penicilline
                    extd_atb(y[10])
                elif y[10] == "NL":
                    if y[9] in ("S","R","I"):
                        extd_atb(y[9])
                    else:
                        extd_atb([""])
                else:
                    extd_atb([""])
                extd_atb(y[13]) # choix entre ampicilline
                if y[29] in ("S","R","I"): # choix entre AMX
                    extd_atb(y[29])
                elif y[30] in ("S","R","I"):
                    extd_atb(y[30])
                else:
                    extd_atb([""])
                extd_atb(y[17]) # choix entre AMC
                extd_atb(y[31]) # choix entre PIP
                extd_atb(y[18]) # choix entre PIT
                if y[11] in ("S","R","I"): # choix entre cefotaxime
                    extd_atb(y[11])
                elif y[12] in ("S","R","I"):
                    extd_atb(y[12])
                else:
                    extd_atb([""])
                if y[25] == "NL": # choix entre FOX
                    extd_atb(y[24])
                else:
                    extd_atb(y[25])
                extd_atb(y[19]) # choix entre IMP
                extd_atb(y[16]) # choix entre NAL
                extd_atb(y[15]) # choix entre CIP
                extd_atb(y[34]) # choix entre MOX
                extd_atb(y[14]) # choix entre SXT
                extd_atb(y[32]) # choix entre TET
                if y[28] in ("S","R","I"): # choix entre RIF
                    extd_atb(y[28])
                elif y[27] in ("S","R","I"):
                    extd_atb(y[27])
                else:
                    extd_atb([""])
                extd_atb(y[27]) # choix entre ERY
                if y[21] in ("S","R","I"): # choix entre clinda
                    extd_atb(y[21])
                elif y[21] == "NL" :
                    extd_atb(y[23])
                else:
                    extd_atb(y[22])
                extd_atb(y[20]) # choix entre MTZ
                extd_atb(y[33]) # choix entre VA
                extd_atb(y[35]) # choix entre TIG
                for v, w in enumerate(new_atb): # remove the last "NL"
                    if w == "NL":
                        new_atb[v] = ""
                atb_ana.append(new_atb)
                list_atb.remove(y)

# output AST results
with open("atb_ana.csv", 'w', newline="") as atb_file:
    writer_atb = csv.writer(atb_file, delimiter=';')
    # create a header
    writer_atb.writerow(
                        ["IPP",
                         "genus",
                         "bacteria",
                         "PEN",
                         "AMPI",
                         "AMX",
                         "AMC",
                         "PIP",
                         "PIT",
                         "CTX",
                         "FOX",
                         "IMP",
                         "NAL",
                         "CIP",
                         "MOX",
                         "SXT",
                         "TET",
                         "RIF",
                         "ERY",
                         "CLI",
                         "MTZ",
                         "VA",
                         "TIG"]
                        )
    for row in atb_ana:
        writer_atb.writerow(row)
