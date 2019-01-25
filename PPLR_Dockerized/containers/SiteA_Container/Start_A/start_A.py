import time
start_time = time.time()

import pandas as pd
import numpy as np
import requests
import json

# Privacy-preserving Linear Regression
df = pd.read_csv("preprocessed_dataFile_A.csv", low_memory=False)

# Salt must be 128 bytes in hex.
salt = 'a'.encode('UTF-8') * 128

# PI = ['encounter_id']
X_a = df[['num_lab_procedures','num_medications']].iloc[0:1000] #.drop(PI, axis = 1)
B_divide_set = 10


# Add one columns with all values of 1 to dataset which uses to calculate b0
b0 = np.ones((1, len(X_a))).tolist()[0]
X_a.insert(loc=0, column='b0', value=b0)

len_A = len(X_a.columns)

# Generate random numbers and add to data at Data Site A
A_randoms = []
for i in range(0, len_A):
    np.random.seed(1)
    A_randoms.append(np.random.randint(0,5, len(X_a.iloc[:,i])))
    
C_matrix = [] # C_noises is shared between A and B 
for i in range(0, len_A):
    np.random.seed(2)
    C_matrix.append(np.random.randint(0,5, (len(X_a.iloc[:,i]), len(X_a.iloc[:,i]))))

Sum_noises_A = [] # which will be sent to B
for i in range(0, len_A):
    Sum_noises_A.append(np.add(X_a.iloc[:,i], np.dot(C_matrix[i], A_randoms[i])))

### Only A ###
np.save('A_randoms.npy', A_randoms)

#send file to TTP service
res_A_randoms = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('A_randoms.npy', 'rb')})
resultJson_0 = json.loads(res_A_randoms.text.encode("utf-8"))
#print output
print("(Only) A_randoms: UUID: %s" % resultJson_0["uuid"].encode("utf-8"))

### Share with B ###
np.save('/data/C_matrix.npy', C_matrix)
np.save('/data/Sum_noises_A.npy', Sum_noises_A)

#send file to TTP service
res_C_matrix = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('/data/C_matrix.npy', 'rb')})
resultJson_1 = json.loads(res_C_matrix.text.encode("utf-8"))
#print output
print("C_matrix: UUID: %s" % resultJson_1["uuid"].encode("utf-8"))


res_Sum_noises_A = requests.post(url='http://dockerhost:5001/addFile',
    files={"fileObj": open('/data/Sum_noises_A.npy', 'rb')})
resultJson_2 = json.loads(res_Sum_noises_A.text.encode("utf-8"))
#print output
print("Sum_noises_A: UUID: %s" % resultJson_2["uuid"].encode("utf-8"))

# pse_df.to_csv("/data/cbs.csv", sep=',', encoding='utf-8') # pse_df

print("Site A took", time.time() - start_time, "to finish Step 1")