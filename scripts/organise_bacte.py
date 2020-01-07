import csv
import sys
import pickle
from datetime import datetime, timedelta, time

# load list of bacteria with groups
list_bact=dict()
with open('bacteria_def.csv') as bacteria_file:
    reader_b = csv.reader(bacteria_file)
    for row in reader_b:
        list_bact[row[0]] = row[2]

# load true_bacteriemia.pickle
with open('true_bacteriemia.pickle', 'rb') as infile:
    dataset = pickle.load(infile)

# list bacteriemia per patient
bact=dict()
for row in dataset:
    if row[5] in bact:
        bact[row[5]].append({
            'bacteria':[row[0]],
            'first_isol':row[1],
            'last_isol':row[2],
            'service':row[4]
        })
    else:
        bact[row[5]] = [{
            'bacteria':[row[0]],
            'first_isol':row[1],
            'last_isol':row[2],
            'service':row[4]
        }]

# combined true_bacteriemia in episodes
def_bact=[]
for x in bact :
    if len(bact[x]) == 1 :
        def_bact.append([
            [bact[x][0]['bacteria']],
            bact[x][0]['first_isol'],
            bact[x][0]['last_isol'],
            bact[x][0]['service']
        ])
    else:
        temp_bact=[]
        for y in bact[x]:
            if temp_bact != []:
                for z in temp_bact:
                    if (z['first_isol'] <= y['first_isol'] <= z['last_isol'] + timedelta(5)
                        or z['first_isol'] <= y['last_isol'] <= z['last_isol'] + timedelta(5)):
                        if z['service'] == "ICM_NP":
                            serv_temp = y['service']
                        elif y['service'] == "ICM_NP":
                            serv_temp = z['service']
                        elif z['first_isol'] <= y['first_isol']:
                            serv_temp = z['service']
                        else:
                            serv_temp = y['service']
                        temp_bact[temp_bact.index(z)] = {
                            'bacteria':z['bacteria'] + y['bacteria'],
                            'first_isol':min(z['first_isol'],y['first_isol']),
                            'last_isol':max(z['last_isol'],y['last_isol']),
                            'service':serv_temp
                        }
                        break
                else:
                    temp_bact.append(y)
            else:
                temp_bact.append(y)
        for z in temp_bact:
            def_bact.append([
                [z['bacteria']],
                z['first_isol'],
                z['last_isol'],
                z['service']
            ])

# export bacteriemia
output_file = open('bacteriemia.pickle', 'wb')
pickle.dump(def_bact, output_file)
output_file.close()
