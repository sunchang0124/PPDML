import time
start_time = time.time()
import json
import requests
import shutil
import pandas as pd
import numpy as np

# Privacy-preserving Linear Regression
# From B: Get noised Sum  #
with open('input_shared.json') as data_file:    
    inputJson_S = json.load(data_file)

url = 'http://dockerhost:5001/file/%s' % inputJson_S["Sum_noises_B"]
response = requests.get(url, stream=True)
with open('/data/Sum_noises_B.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
Sum_noises_B = np.load('/data/Sum_noises_B.npy')

# Have to read data again...
df = pd.read_csv("preprocessed_dataFile_A.csv", low_memory=False)

with open('input_internal.json') as data_file:    
    inputJson_I = json.load(data_file)

url = 'http://dockerhost:5001/file/%s' % inputJson_I["A_randoms"]
response = requests.get(url, stream=True)
with open('A_randoms.npy', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
A_randoms = np.load('A_randoms.npy')

# PI = ['encounter_id']
X_a = df[['num_lab_procedures','num_medications']].iloc[0:1000]
b0 = np.ones((1, len(X_a))).tolist()[0]
X_a.insert(loc=0, column='b0', value=b0)
B_divide_set = 10
len_A = len(X_a.columns)

### At site A ###
A_randoms_Sumset = []
for i in range(0, len_A):
    sum_temp = []
    for j in range(0, int(len(X_a)/B_divide_set)):
        temp = 0
        for k in range(0, B_divide_set):
            temp = temp + A_randoms[i][B_divide_set*j + k]
        sum_temp.append(temp)
        
    A_randoms_Sumset.append(sum_temp)
 
    
Sum_noises_B_Arand = []
for n in range(0, len(Sum_noises_B)):
    temp = []
    for i in range(0, len_A):
        temp.append(np.dot(A_randoms[i],Sum_noises_B[n][i]))
    Sum_noises_B_Arand.append(temp)

# Calculate X_a.T * X_a locally at data site A 
XaTXa = np.matrix(X_a).T * np.matrix(X_a)

### share with B ###
np.save('/data/A_randoms_Sumset.npy', A_randoms_Sumset)
np.save('/data/Sum_noises_B_Arand.npy', Sum_noises_B_Arand)
np.save('/data/XaTXa.npy', XaTXa)

#send file to TTP service
res_A_randoms_Sumset = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('/data/A_randoms_Sumset.npy', 'rb')})
resultJson_1 = json.loads(res_A_randoms_Sumset.text.encode("utf-8"))
#print output
print("A_randoms_Sumset: UUID: %s" % resultJson_1["uuid"].encode("utf-8"))


res_Sum_noises_B_Arand = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('/data/Sum_noises_B_Arand.npy', 'rb')})
resultJson_2 = json.loads(res_Sum_noises_B_Arand.text.encode("utf-8"))
#print output
print("Sum_noises_B_Arand: UUID: %s" % resultJson_2["uuid"].encode("utf-8"))


res_XaTXa = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('/data/XaTXa.npy', 'rb')})
resultJson_3 = json.loads(res_XaTXa.text.encode("utf-8"))
#print output
print("XaTXa: UUID: %s" % resultJson_3["uuid"].encode("utf-8"))

print "My program took", time.time() - start_time, "to run"