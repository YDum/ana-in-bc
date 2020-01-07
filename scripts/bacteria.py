#!/usr/bin/python3

import pickle
import csv
import sys

dataset_file = open('dataset.pickle', 'rb')
dataset = pickle.load(dataset_file)
dataset_file.close()

bacteria=set()

# extract bacteria species from the dataset
for x in dataset :
    for y in x['prelevements']:
        for z in y['germe']:
            bacteria.add(z[0])

# write bacteria in bacteria.csv
with open('bacteria.csv', 'w') as bacteria_file:
    writer_b = csv.writer(bacteria_file)
    for row in bacteria:
        writer_b.writerow([row,"",""])
