#!/usr/bin/python3

import csv
import sys
import pickle
import secrets
from datetime import datetime, timedelta

# load ICM services data, since service number needed a separate extraction
listservicm={}
with open('hemoc_ICM.csv', newline='', encoding='iso-8859-1') as icmfile:
    icmdata = csv.reader(icmfile, delimiter=",")
    next(icmdata) #skip first line
    for row in icmdata:
        if row[1] == "":
            listservicm[row[3]] = "ICM_NP"
        else:
            listservicm[row[3]] = row[1]


# Load ATB data
list_atb=[]
with open('HAA_CHU_ATB.csv', newline='', encoding='iso-8859-1') as chu_atb_file:
    chu_atb_data = csv.reader(chu_atb_file, delimiter=',')
    next(chu_atb_data)
    for row in chu_atb_data:
        list_atb.append([row[5][-8:],row[7],int(row[6]),row[8][:3]])
with open('HAA_ICM_ATB.csv', newline='', encoding='iso-8859-1') as icm_atb_file:
    icm_atb_data = csv.reader(icm_atb_file, delimiter=',')
    next(icm_atb_data)
    next(icm_atb_data)
    for row in icm_atb_data:
        list_atb.append([row[5][-8:],row[7],int(row[6]),row[8][:3]])

def icmserv(): #replace ICM generic service by real services or ICM_NL
    if row[9] == '9993':
        try:
            return(listservicm[row[8]])
        except IndexError:
            print('ICM_NL')
    else:
        return(row[9])


def newhemoc(a): # add a new prelevement to a patient from the dataset
    germe=[]
    germe_type=list()
    germe_num=list()
    for x in row[12:-1]:
        if x == "" or x == "N/A" : # eliminate "null" values
            continue
        elif x[0:7] == "Identif": # append identification numbers in germe_num
            germe_num.append(int(x[-1]))
        elif x == 'ENTCLO': # unify E. cloacae complex
            germe_type.append('ENTCLX')
        elif x == 'ENTFRE': # unify E. freundii complex
            germe_type.append('ENTFRX')
        elif x == 'STRB': # rename S. agalactiae
            germe_type.append('STRAGA')
        elif x == 'STRA': # rename S. pyogenes
            germe_type.append('STRPYO')
        elif x == 'BACDIS': # rename P. distasonis
            germe_type.append('PARDIS')
        else : # append germ number to germe_type
            germe_type.append(x)
    germe_type_len = len(germe_type)
    for x in range(germe_type_len): #associate germ type and number
        germe.append([germe_type[x],germe_num[x]])
    for x in germe: #associate AST with corresponding isolate
        for y in list_atb:
            if (str(row[8])[-8:] == y[0] and x == y[1:3]):
                x.append(y[3][:4])
                list_atb.remove(y)
                break
        else:
            x.append('INC')
    a.append({
        'date_plvt':datetime.strptime(row[0], "%d/%m/%Y %H:%M:%S"),
        'travail_num':str(row[8])[-8:],
        'service':icmserv(),
        'germe':germe})


# create the dataset
dataset=list()
with open('Somme.csv', newline='', encoding='iso-8859-1') as csvfile:
  hemocdata = csv.reader(csvfile, delimiter=";")
  for row in hemocdata:
    if row[4] == 'IPP': # skip first line
      continue
    if row[12] == "N/A" : # eliminate negative pairs of blood culture
      continue
    if row[4] == '': # eliminate forensic analyses
      continue
    if ((datetime(2015,6,1)) - datetime.strptime(row[6], "%d/%m/%Y") < timedelta(16,0,0)): # eliminates patients < 16 years
      continue
    for x in dataset:
      if x['ipp_num'] == row[4]: # verify if IPP exist in dataset, if so add a new prelevement
        patient=dataset.index(x)
        newhemoc(dataset[patient]['prelevements'])
        break
    else: #create new patient and add a new prelevement
      new_prlvt={}
      new_prlvt['ipp_num'] = row[4]
      new_prlvt['info_patient'] = {
        'ddn_patient':datetime.strptime(row[6], "%d/%m/%Y"),
        'sexe_patient':row[7]
        }
      new_prlvt['prelevements']=[]
      newhemoc(new_prlvt['prelevements'])
      dataset.append(new_prlvt)

# anonymise ipp
anon_ipp = set()
dataset_anon = []
for x in dataset:
    while True:
        new_ipp = secrets.randbelow(10000)
        if new_ipp not in anon_ipp:
            break
    anon_ipp.add(new_ipp)
    anon_patient = x
    anon_patient["ipp_num"] = new_ipp
    dataset_anon.append(anon_patient)

# Output dataset in pickle
output_file = open('dataset.pickle', 'wb')
pickle.dump(dataset_anon, output_file)
output_file.close()
