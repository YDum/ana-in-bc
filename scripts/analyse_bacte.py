import csv
import sys
import pickle
from datetime import datetime, timedelta
from statistics import mean, median
import numpy
from scipy import stats


with open('bacteriemia.pickle', 'rb') as datafile:
    bact = pickle.load(datafile)

list_bact=dict()
list_genus=dict()
name_bact=dict()
with open('bacteria_def.csv') as bacteria_file:
    reader_b = csv.reader(bacteria_file)
    for row in reader_b:
        list_bact[row[0]] = row[2]
        name_bact[row[0]] = row[1]
        list_genus[row[0]] = row[1].split(" ")[0]

service_list=set()
for x in bact:
    service_list.add(x[3])

bact_per_service=[]
bact_ana=[]
for w in service_list:
    num=0
    num_ana=0
    bact_sp=dict()
    for x in bact:
        if x[3] == w:
            num += 1
            for y in x[0][0]:
                if (list_bact[y] == '3' or list_bact[y] == '4'):
                    if str(x[0][0]) in bact_sp:
                        bact_sp[str(x[0][0])] += 1
                    else:
                        bact_sp[str(x[0][0])] = 1
                    num_ana += 1
                    bact_ana.append(x)
                    break
    bact_per_service.append([w,num,num_ana,bact_sp])

# share of plurimicrobial episodes
count_bact = 0
total_bact = 0
len_bact=dict()
for x in bact:
    try:
        len_bact[len(x[0][0])] += 1
    except KeyError:
        len_bact[len(x[0][0])] = 1
    if len(x[0][0]) > 1:
        count_bact += 1
    total_bact += 1
moy_bact=0
denom_bact=0
for x in len_bact:
    if x != 1:
        moy_bact += x*len_bact[x]
        denom_bact += len_bact[x]
print("mean number of species per polymicrobial episode : " + str(moy_bact/denom_bact))
print("repartition of the numbers of species per episode : " + str(len_bact))
print("number of plurimicrobial bacteriemia : " + str(count_bact))
print("total number of episodes : "+ str(total_bact))
print("frequence of plurimicrobial episodes within all episodes : " + str(count_bact/total_bact) + "\n")
count_bact_pluri = count_bact
total_bact_pluri = total_bact


# share of plurimicrobial episodes within BIAB
count_bact = 0
total_bact = 0
len_bact=dict()
for x in bact_ana:
    try:
        len_bact[len(x[0][0])] += 1
    except KeyError:
        len_bact[len(x[0][0])] = 1
    if len(x[0][0]) > 1:
        count_bact += 1
    total_bact += 1
moy_bact=0
denom_bact=0
for x in len_bact:
    if x != 1:
        moy_bact += x*len_bact[x]
        denom_bact += len_bact[x]
print("mean number of species per BIAB episodes : " + str(moy_bact/denom_bact))
print("repartition of the numbers of species per episode : " + str(len_bact))
print("number of plurimicrobial bacteriemia within BIAB : " + str(count_bact))
print("total number of BIAB episodes : "+ str(total_bact))
print("frequence of plurimicrobial episodes within BIAB episodes : " + str(count_bact/total_bact))
obs=numpy.array([[count_bact,total_bact-count_bact],[count_bact_pluri,total_bact_pluri-count_bact_pluri]])
print("p-value " + str(stats.chi2_contingency(obs)[1]) + ".")
print("\n")

# number of BIAB with only AB
only_ana=0
only_multiana=0
for x in bact_ana:
    for y in x[0][0]:
        if list_bact[y] in ("3","4"):
            continue
        else:
            break
    else:
        only_ana += 1
        if len(x[0][0]) > 1:
            only_multiana += 1
print("number of BIAB with only AB : " + str(only_ana))
print("number of polymicrobial BIAB episodes with only AB : " + str(only_multiana) + "\n")

# number of episodes, of BIAB episodes, per service, plus description of episodes
print('all data')
for x in bact_per_service:
    print(x)
print("\n")

# frequencies of BIAB within all episodes, in ICM, for each service
freq_bactana=[]
freq_bactana_serv=dict()
print("frequencies of BIAB within all episodes, in ICM, for each service")
for x in bact_per_service:
    if x[1] > 10 and x[0][:3] == 'ICM':
        print(x)
        print(str(x[2]/x[1]))
        freq_bactana.append(x[2]/x[1])
        freq_bactana_serv[x[0]] = x[2]/x[1]
print(freq_bactana_serv)
with open('freq_bact_per_serv_icm.csv','w', newline='') as outputfile:
    writer = csv.writer(outputfile)
    writer.writerow(['service','frequence'])
    for key,value in freq_bactana_serv.items():
        writer.writerow([key,value])
print("minimal frequency ICM >=10 : " + str(min(freq_bactana)))
print("maximal frequency ICM >=10 : " + str(max(freq_bactana)))
print("mean of frequency ICM >=10 : " + str(mean(freq_bactana)))
print("median of frequency ICM >=10 : " + str(median(freq_bactana)) + "\n")

# frequencies of BIAB within all episodes, in CHU, for each service
freq_bactana=[]
freq_bactana_serv=dict()
print("frequencies of BIAB within all episodes, in ICM, for each service")
for x in bact_per_service:
    if x[1] > 10 and x[0][:3] != 'ICM':
        print(x)
        print(str(x[2]/x[1]))
        freq_bactana.append(x[2]/x[1])
        freq_bactana_serv[x[0]] = x[2]/x[1]
with open('freq_bact_per_serv_chu.csv','w', newline='') as outputfile:
    writer = csv.writer(outputfile)
    writer.writerow(['service','frequence'])
    for key,value in freq_bactana_serv.items():
        writer.writerow([key,value])
print("minimal frequency CHUM >=10 : " + str(min(freq_bactana)))
print("maximal frequency CHUM >=10 : " + str(max(freq_bactana)))
print("mean of frequency CHUM >=10 : " + str(mean(freq_bactana)))
print("median of frequency CHUM >=10 : " + str(median(freq_bactana)) + "\n")

# Statistics between CHU and ICM
bact_icm=0
bactana_icm=0
bact_chu=0
bactana_chu=0
for x in bact_per_service:
    if x[0][:3] == 'ICM':
        bact_icm += x[1]
        bactana_icm += x[2]
    else:
        bact_chu += x[1]
        bactana_chu += x[2]
print('chu: '
      + str(bactana_chu)
      + ' bacteriemies ana sur '
      + str(bact_chu) + ' bacteriemie soit '
      + str(bactana_chu/bact_chu*100)
      + '%')
print('ICM: '
      + str(bactana_icm)
      + ' bacteriemies ana sur '
      + str(bact_icm)
      + ' bacteriemie soit '
      + str(bactana_icm/bact_icm*100)
      + '%')
obs=numpy.array([[bactana_chu,bactana_icm],[bact_chu-bactana_chu,bact_icm-bactana_icm]])
print("p-value " + str(stats.chi2_contingency(obs)[1]) + ".")
print("\n")

# frequency of species isolation in BIAB
occur=dict()
for x in list_bact:
    if (list_bact[x] == '3' or list_bact[x] == '4'):
        occur[x] = 0
        for y in bact_per_service:
            for z in y[3]:
                if x in z:
                    occur[x] += y[3][z]
print("frequency of species isolation")
for x in occur:
    print(str(x) + ' : ' + str(occur[x]))
with open("occur_spp.csv", 'w', newline="") as occur_file:
    writer_file = csv.writer(occur_file, delimiter=';')
    writer_file.writerow(["species","name","occurence"])
    for row in occur:
        writer_file.writerow([str(row),str(name_bact[row]),str(occur[row])])
print("\n")

# frequency of genus isolation in BIAB
occur_gen=dict()
for x in list_bact :
    if (list_genus[x] not in occur_gen and (list_bact[x] == '3' or list_bact[x] == '4')): # pas besoin de relancer list_genus[x] si déjà fait
        for y in bact_per_service:
            for z in y[3]:
                for w in z.split(","):
                    if list_genus[x] == list_genus[w[2:8]] and (list_bact[w[2:8]] == '3' or list_bact[w[2:8]] == '4'):
                        try:
                            occur_gen[list_genus[x]] += y[3][z]
                        except KeyError:
                            occur_gen[list_genus[x]] = y[3][z]
                        break
print("frequency of genus isolation :")
for x in occur_gen:
    print(str(x) + ' : ' + str(occur_gen[x]))
with open("occur_gen.csv", 'w', newline="") as occur_file:
    writer_file = csv.writer(occur_file, delimiter=';')
    for row in occur_gen:
        writer_file.writerow([str(row),str(occur_gen[row])])

# frequency of BFG isolation in BIAB
occur_frag_grp=0
for y in bact_per_service:
    for z in y[3]:
        for w in z.split(","):
            if list_genus[w[2:8]] in ('Bacteroides','Parabacteroides'):
                occur_frag_grp += y[3][z]
                break
print("\n" + "Number of episodes with BFG : " + str(occur_frag_grp) + "\n")
