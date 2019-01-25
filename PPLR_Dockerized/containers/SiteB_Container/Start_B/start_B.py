import time
start_time = time.time()

import json
import requests
import shutil

import pandas as pd
import numpy as np

# Privacy-preserving Linear Regression
df = pd.read_csv("preprocessed_dataFile_B.csv", sep=',', low_memory=False)

# Salt must be 128 bytes in hex.
salt = 'a'.encode('UTF-8') * 128

# PI = ['encounter_id']
X_b = df[['diag_1', 'diag_2','diag_3']].iloc[0:1000] #.drop(PI, axis = 1)
B_divide_set = 10
print(len(X_b))

### At site B ###
#### Read file from Server #####
#read input file
with open('input_shared.json') as data_file:    
    inputJson_S = json.load(data_file)

url = 'http://dockerhost:5001/file/%s' % inputJson_S["C_matrix"]
response = requests.get(url, stream=True)
with open('/data/C_matrix.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

url = 'http://dockerhost:5001/file/%s' % inputJson_S["Sum_noises_A"]
response = requests.get(url, stream=True)
with open('/data/Sum_noises_A.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

# Get noised Sum from Site A #
C_matrix = np.load('/data/C_matrix.npy')
Sum_noises_A = np.load('/data/Sum_noises_A.npy')

len_B = len(X_b.columns)

Sum_coef_B = []
for i in range(0, len_B):
    Sum_noises_temp = []
    for j in range(0, len(Sum_noises_A)):
        Sum_noises_temp.append(np.dot(C_matrix[j].transpose(), X_b.iloc[:,i])) 
    Sum_coef_B.append(Sum_noises_temp)

B_random_set = []
for i in range(0, len(Sum_noises_A)):
    np.random.seed(3)
    B_random_set.append(np.random.randint(0,5, int(len(X_b.iloc[:,0])/B_divide_set))) 

Sum_noises_B = [] # which will be send to A
for n in range(0, len_B):
    B_noise = []
    for i in range(0, len(Sum_noises_A)):
        B_random_inter = []
        for j in range(0, len(B_random_set[i])): 
            for k in range(0, B_divide_set):
                B_random_inter.append(B_random_set[i][j])
        B_noise.append(Sum_coef_B[n][i] + B_random_inter)
    Sum_noises_B.append(B_noise)

# Add noises dataset A to the dataset B
Sum_noises_AB = []
for i in range(0, len_B):
    Sum_noises_temp = []
    for j in range(0, len(Sum_noises_A)):
        Sum_noises_temp.append(np.dot(Sum_noises_A[j], X_b.iloc[:,i])) 
    Sum_noises_AB.append(Sum_noises_temp)

### Only at B ###
np.save('B_random_set.npy', B_random_set)
np.save('Sum_noises_AB.npy', Sum_noises_AB)

#send file to TTP service
res_B_random_set = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('B_random_set.npy', 'rb')})
resultJson_0 = json.loads(res_B_random_set.text.encode("utf-8"))
#print output
print("(Only) B_random_set: UUID: %s" % resultJson_0["uuid"].encode("utf-8"))

res_Sum_noises_AB = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('Sum_noises_AB.npy', 'rb')})
resultJson_0 = json.loads(res_Sum_noises_AB.text.encode("utf-8"))
#print output
print("(Only) Sum_noises_AB: UUID: %s" % resultJson_0["uuid"].encode("utf-8"))

### shared with A ###
np.save('/data/Sum_noises_B.npy', Sum_noises_B)

#send file to TTP service
res_Sum_noises_B = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('/data/Sum_noises_B.npy', 'rb')})
resultJson_1 = json.loads(res_Sum_noises_B.text.encode("utf-8"))
#print output
print("Sum_noises_B: UUID: %s" % resultJson_1["uuid"].encode("utf-8"))

print "My program took", time.time() - start_time, "to run"