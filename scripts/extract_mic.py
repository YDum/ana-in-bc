import csv
import sys
import pickle
import numpy as np
from datetime import datetime, timedelta

list_bact=dict()
list_bact_name=dict()
list_genus=dict()

with open('bacteria_def.csv') as bacteria_file:
    reader_b = csv.reader(bacteria_file)
    for row in reader_b:
        list_bact[row[0]] = row[2]
        list_bact_name[row[0]] = row[1]
        list_genus[row[0]] = row[1].split(" ")[0]

list_genus_inv=set()
for x in list_genus:
    list_genus_inv.add(list_genus[x])

with open('true_bacteriemia.pickle', 'rb') as datafile:
    bact = pickle.load(datafile)

list_atb=[]
with open('mensuel_CHU_22_12_2018.csv', newline='', encoding='iso-8859-1') as chu_atb_file:
    chu_atb_data = csv.reader(chu_atb_file, delimiter=';')
    next(chu_atb_data)
    for row in chu_atb_data:
        list_atb.append(row)

atb_ana=[]
for x in bact:
    if list_bact[x[0]] in ("3","4"): # selects anaerobic bacteria
        for y in list_atb:
            if x[-1] == y[2] and x[0] == y[7]: # checks if identification and analyse number is the same
                new_atb=[]
                new_atb.extend([y[2],list_genus[y[7]],y[7]])
                new_atb.append(y[9]) #AMC
                new_atb.append(y[12]) #MTR
                if y[15] != "": # choose between cefoxitins
                    new_atb.append(y[15])
                else:
                    new_atb.append(y[16])
                new_atb.append(y[21])
                for v, w in enumerate(new_atb): # remove the last "NL"
                    if w == "NL":
                        new_atb[v] = ""
                for v, w in enumerate(new_atb): #transform str in flt
                    if new_atb.index(w) in (0,1,2):
                        next
                    elif (type(w) == str and w != ""):
                        if ">" in w or "<" in w:
                            new_atb[v] = w.replace(" ","").replace(",",".")
                        else:
                            new_atb[v] = float(w.replace(" ","").replace(",","."))
                atb_ana.append(new_atb)

# input a table with all the MIC
with open("mic_ana.csv", 'w', newline="") as atb_file:
    writer_atb = csv.writer(atb_file, delimiter=';')
    writer_atb.writerow(["IPP","genus","bacteria","AMC","MTR","FOX","TYG"])
    for row in atb_ana:
        writer_atb.writerow(row)

# creates statistics (MIC50, MIC90, min, max)
def stat_mic(mic_array):
    j=[]
    if len(mic_array) != 0:
        j.append(np.percentile(mic_array,50))
        j.append(np.percentile(mic_array,90))
        j.append(np.amin(mic_array))
        j.append(np.amax(mic_array))
    else :
        j.append("NA")
        j.append("NA")
        j.append("NA")
        j.append("NA")
    return j

# format MIC to avoid unusable characters
def mic_append(a):
    if isinstance(a,str) :
        c = a.replace(" ","").replace(",",".")
        if "<" in c:
            print(c)
            mic_val = float(0)
        elif ">" in c:
            print(c)
            d = c.replace(">","")
            mic_val = float(d)
            mic_val += 1
    else:
        mic_val = float(a)
    return(mic_val)

# for each genus and antibiotic, calculates MIC50, MIC90 and min/max
list_mic_gen=dict()
with open("mic_per_gen.csv", "w", newline='') as mic_file:
    writer_atb = csv.writer(mic_file, delimiter=';')
    writer_atb.writerow(["genus",
                         "AMC CMI50","AMC CMI90","AMC MIN","AMC MAX",
                         "MTR CMI50","MTR CMI90","MTR MIN","MTR MAX",
                         "FOX CMI50","FOX CMI90","FOX MIN","FOX MAX",
                         "TYG CMI50","TYG CMI90","TYG MIN","TYG MAX"])
    for x in list_genus_inv:
        amc_array = np.array([])
        mtr_array = np.array([])
        fox_array = np.array([])
        tyg_array = np.array([])
        for y in atb_ana:
            if list_bact[y[2]] in ("3","4"):
                if y[1] == x :
                    if y[3] != "": amc_array = np.append(mic_append(y[3]),amc_array)
                    if y[4] != "": mtr_array = np.append(mic_append(y[4]),mtr_array)
                    if y[5] != "": fox_array = np.append(mic_append(y[5]),fox_array)
                    if y[6] != "": tyg_array = np.append(mic_append(y[6]),tyg_array)
        stats_bundle = list([x]
                            + stat_mic(amc_array)
                            + stat_mic(mtr_array)
                            + stat_mic(fox_array)
                            + stat_mic(tyg_array))
        if stats_bundle[1:] != list(["NA"] * 16):
            writer_atb.writerow(stats_bundle)
        list_mic_gen[x] = {'AMC': amc_array, 'MTR': mtr_array, 'FOX': fox_array, 'TYG': tyg_array}

with open('list_mic_gen.pickle', 'wb') as datafile:
    pickle.dump(list_mic_gen,datafile)

# for each species and antibiotic, calculates MIC50, MIC90 and min/max
list_mic_sp=dict()
with open("mic_per_sp.csv", "w", newline='') as mic_file:
    writer_atb = csv.writer(mic_file, delimiter=';')
    writer_atb.writerow(["species",
                         "AMC CMI50","AMC CMI90","AMC MIN","AMC MAX",
                         "MTR CMI50","MTR CMI90","MTR MIN","MTR MAX",
                         "FOX CMI50","FOX CMI90","FOX MIN","FOX MAX",
                         "TYG CMI50","TYG CMI90","TYG MIN","TYG MAX"])
    for x in list_bact:
        amc_array = np.array([])
        mtr_array = np.array([])
        fox_array = np.array([])
        tyg_array = np.array([])
        for y in atb_ana:
            if list_bact[y[2]] in ("3","4"):
                if y[2] == x :
                    if y[3] != "": amc_array = np.append(mic_append(y[3]),amc_array)
                    if y[4] != "": mtr_array = np.append(mic_append(y[4]),mtr_array)
                    if y[5] != "": fox_array = np.append(mic_append(y[5]),fox_array)
                    if y[6] != "": tyg_array = np.append(mic_append(y[6]),tyg_array)
        stats_bundle = list([list_bact_name[x]]
                            + stat_mic(amc_array)
                            + stat_mic(mtr_array)
                            + stat_mic(fox_array)
                            + stat_mic(tyg_array))
        if stats_bundle[1:] != list(["NA"] * 16):
            writer_atb.writerow(stats_bundle)
        list_mic_sp[x] = {'AMC': amc_array, 'MTR': mtr_array, 'FOX': fox_array, 'TYG': tyg_array}

with open('list_mic_sp.pickle', 'wb') as datafile:
    pickle.dump(list_mic_sp,datafile)
