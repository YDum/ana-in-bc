import csv
import sys
import pickle
from datetime import datetime, timedelta

# load dataset
dataset_file = open('dataset.pickle', 'rb')
dataset = pickle.load(dataset_file)
dataset_file.close()

true_bact=[]
discard_bact=[]
ptt_bact=[]

# load definitive bacteria list
list_bact=dict()
with open('bacteria_def.csv') as bacteria_file:
    reader_b = csv.reader(bacteria_file)
    for row in reader_b:
        list_bact[row[0]] = row[2]

# format episodes
def episod_appd(b,c):
    c.append([
        b,
        episode[b]['first_isol'],
        episode[b]['last_isol'],
        episode[b]['nber_isol'],
        episode[b]['service'],
        episode[b]['ipp_num']
        ])
    del episode[b]

# check whether conditions are met to assert a true episodes
def verif_episode(a):
    if list_bact[a] == '1':
        episod_appd(a,true_bact)
    elif (list_bact[a] == '2'
          and episode[a]['nber_OUI'] >= 1):
        episod_appd(a,true_bact)
    elif list_bact[a] == '3':
        episod_appd(a,true_bact)
    elif (list_bact[a] == '4'
          and episode[a]['nber_isol'] >= 2):
        episod_appd(a,true_bact)
    elif list_bact[a] == '0':
        del episode[a]
    else:
        episod_appd(a,discard_bact)

# go through the dataset to create epidodes, and then check them
for x in dataset:
    episode=dict()
    for y in x['prelevements']:
        for z in y['germe']:
            if z[0] in episode:
                if (y['date_plvt'] - episode[z[0]]['last_isol']) < timedelta(5): #timedelta fixed to 5 days
                    episode[z[0]]['last_isol'] = y['date_plvt']
                    episode[z[0]]['nber_isol'] += 1
                    if z[-1] == 'OUI': episode[z[0]]['nber_OUI'] += 1
                    if z[-1] == 'NON': episode[z[0]]['nber_NON'] += 1
                    if z[-1] == 'INC': episode[z[0]]['nber_INC'] += 1
                else:
                    verif_episode(z[0])
            else:
                episode[z[0]] = {'first_isol': y['date_plvt'],
                                 'last_isol': y['date_plvt'],
                                 'service': y['service'],
                                 'nber_isol': 1,
                                 'nber_OUI': 1 if z[-1] == 'OUI' else 0,
                                 'nber_NON': 1 if z[-1] == 'NON' else 0,
                                 'nber_INC': 1 if z[-1] == 'INC' else 0,
                                 'ipp_num': x['ipp_num']
                                 }
    remain_episode = list(episode.keys())
    for w in remain_episode: #verify conditions for each bacteria
        verif_episode(w)


with open('true_bacteriemia.pickle', 'wb') as outfile:
    pickle.dump(true_bact,outfile)

with open('false_bacteriemia.pickle', 'wb') as outfile:
    pickle.dump(discard_bact,outfile)
