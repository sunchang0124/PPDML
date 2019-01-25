import time
start_time = time.time()

import json
import shutil
import requests
import pandas as pd
import numpy as np
from numpy.linalg import inv

# Privacy-preserving Linear Regression
# From A: Get   #
#read input file
with open('input_shared.json') as data_file:    
    inputJson_S = json.load(data_file)

url = 'http://dockerhost:5001/file/%s' % inputJson_S["A_randoms_Sumset"]
response = requests.get(url, stream=True)
with open('/data/A_randoms_Sumset.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

url = 'http://dockerhost:5001/file/%s' % inputJson_S["Sum_noises_B_Arand"]
response = requests.get(url, stream=True)
with open('/data/Sum_noises_B_Arand.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

url = 'http://dockerhost:5001/file/%s' % inputJson_S["XaTXa"]
response = requests.get(url, stream=True)
with open('/data/XaTXa.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

A_randoms_Sumset = np.load('/data/A_randoms_Sumset.npy')
Sum_noises_B_Arand = np.load('/data/Sum_noises_B_Arand.npy')


# Have to read data again...
df = pd.read_csv("preprocessed_dataFile_B.csv", low_memory=False)

with open('input_internal.json') as data_file:    
    inputJson_I = json.load(data_file)

url = 'http://dockerhost:5001/file/%s' % inputJson_I["Sum_noises_AB"]
response = requests.get(url, stream=True)
with open('Sum_noises_AB.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

url = 'http://dockerhost:5001/file/%s' % inputJson_I["B_random_set"]
response = requests.get(url, stream=True)
with open('B_random_set.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
B_random_set = np.load('B_random_set.npy')
Sum_noises_AB = np.load('Sum_noises_AB.npy')


X_b = df[['diag_1', 'diag_2','diag_3']].iloc[0:1000] 
B_divide_set = 10
len_A = len(A_randoms_Sumset)
len_B = len(Sum_noises_AB)

### At site B ###
rand_sums = []
for i in range(0, len_A):
    r_sum = 0
    for j in range(0, len(B_random_set[0])):
        r_sum = r_sum + A_randoms_Sumset[i][j] * B_random_set[i][j]
    rand_sums.append(r_sum)
 
outcomes = []
for n in range(0, len_B):
    out = []
    for i in range(0, len_A):
        out.append(Sum_noises_AB[n][i] - Sum_noises_B_Arand[n][i] + rand_sums[i]) 
    outcomes.append(out)


### Compute b0, b1 ###
XaTXa = np.load('/data/XaTXa.npy')
XbTXb = np.matrix(X_b).T * np.matrix(X_b)

XaTXb = np.matrix(outcomes)[:-1]
XbTXa = XaTXb.T

XaTY = np.matrix(outcomes)[-1]
XbTXb_exclY = XbTXb[:-1].T[:-1]
XbTY = np.delete(XbTXb[-1], -1)

pp_XTX = np.concatenate((np.concatenate((XaTXa, XbTXa), axis=1), np.concatenate((XaTXb, XbTXb_exclY), axis=1)),axis=0) 
pp_XTY = np.concatenate((XaTY, XbTY),axis=1).T

pp_out = np.linalg.inv(pp_XTX) * pp_XTY

b1 = pp_out[1:]
b0 = pp_out.item(0)
print('Coefficients: \n' ,b1)
print('Intercept: ', b0)

print "My program took", time.time() - start_time, "to run"