import time
import pandas as pd
import numpy as np
import requests
import json
from numpy.linalg import inv

### Start at A ###
def start_at_A(df, Divide_set, C_seed, C_min, C_max): # df: import data in DataFrame Format
    start_time = time.time()
    
    X_a = df #.drop(PI, axis = 1)
    B_divide_set = Divide_set

    # Add one columns with all values of 1 to dataset which uses to calculate b0
    b0 = np.ones((1, len(X_a))).tolist()[0]
    X_a.insert(loc=0, column='b0', value=b0)

    len_A = len(X_a.columns)

    # Generate random numbers and add to data at Data Site A
    A_randoms = []
    for i in range(0, len_A):
        # np.random.seed(1)
        A_randoms.append(np.random.randint(0,5, len(X_a.iloc[:,i])))
        
    C_matrix = [] # C_noises is shared between A and B 
    for i in range(0, len_A):
        np.random.seed(C_seed)
        C_matrix.append(np.random.randint(C_min,C_max, (len(X_a.iloc[:,i]), len(X_a.iloc[:,i]))))

    Sum_noises_A = [] # which will be sent to B
    for i in range(0, len_A):
        Sum_noises_A.append(np.add(X_a.iloc[:,i], np.dot(C_matrix[i], A_randoms[i])))

    ### To Byte ###
    A_randoms_byte = np.array(A_randoms).tolist() ### Local file: Only A ###
    C_matrix_byte = np.array(C_matrix).tolist() ### Shared file with B ###
    Sum_noises_A_byte = np.array(Sum_noises_A).tolist() ### Shared file with B ###

    # print("Start A took " + (time.time() - start_time) + " to run")

    return {
        "randomBytes": A_randoms_byte,
        "sumNoiseBytes": Sum_noises_A_byte
    }


################################################################
################################################################
### At site B ###
def start_at_B(df , C_seed, C_min, C_max, Sum_noises_A, Divide_set): # df: import data in DataFrame Format
    start_time = time.time()
    
    Sum_noises_A = np.array(Sum_noises_A)
    C_matrix = [] # seeds, range of C_noises is shared between A and B 
    for i in range(0, len(Sum_noises_A)):
        np.random.seed(C_seed)
        C_matrix.append(np.random.randint(C_min ,C_max , (len(Sum_noises_A[i,:]), len(Sum_noises_A[i,:]))))
    
    X_b = df 
    B_divide_set = Divide_set

    len_B = len(X_b.columns)

    Sum_coef_B = []
    for i in range(0, len_B):
        Sum_noises_temp = []
        for j in range(0, len(Sum_noises_A)):
            Sum_noises_temp.append(np.dot(C_matrix[j].transpose(), X_b.iloc[:,i])) 
        Sum_coef_B.append(Sum_noises_temp)

    B_random_set = []
    for i in range(0, len(Sum_noises_A)):
        # np.random.seed(3)
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

    ### To Byte ###
    B_random_set_byte = np.array(B_random_set).tolist() ### Only at B ###
    Sum_noises_AB_byte = np.array(Sum_noises_AB).tolist() ### Only at B ###
    Sum_noises_B_byte = np.array(Sum_noises_B).tolist() ### shared with A ###

    return {
        "randomBytes": B_random_set_byte,
        "sumNoisesAB": Sum_noises_AB_byte,
        "sumNoisesB": Sum_noises_B_byte
    }


################################################################
################################################################

def communication_at_A(df, A_randoms, Sum_noises_AB, Sum_noises_B, Divide_set):
    start_time = time.time()
    
    A_randoms = np.array(A_randoms)
    Sum_noises_B = np.array(Sum_noises_B)
    Sum_noises_AB = np.array(Sum_noises_AB)

    X_a = df
    B_divide_set = Divide_set
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
            temp.append(np.subtract(Sum_noises_AB[n][i], np.dot(A_randoms[i],Sum_noises_B[n][i])))
        Sum_noises_B_Arand.append(temp)

    # Calculate X_a.T * X_a locally at data site A 
    XaTXa = np.matrix(X_a).T * np.matrix(X_a)

    ### To Byte ###
    A_randoms_Sumset_byte = np.array(A_randoms_Sumset).tolist()
    Sum_noises_B_Arand_byte = np.array(Sum_noises_B_Arand).tolist()
    XaTXa_byte = np.array(XaTXa).tolist()
    
    return {
        "randomsSumSet": A_randoms_Sumset_byte,
        "sumNoisesBARand": Sum_noises_B_Arand_byte,
        "XaTXa": XaTXa_byte
    }


################################################################
################################################################

def Final_at_B(df, A_randoms_Sumset, Sum_noises_B_Arand, XaTXa, B_random_set, Divide_set):
    start_time = time.time()
    
    A_randoms_Sumset = np.array(A_randoms_Sumset)
    Sum_noises_B_Arand = np.array(Sum_noises_B_Arand)
    XaTXa = np.array(XaTXa)

    X_b = df
    B_divide_set = Divide_set
    len_A = len(A_randoms_Sumset)
    len_B = len(Sum_noises_B_Arand)

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
            out.append(Sum_noises_B_Arand[n][i] + rand_sums[i]) 
        outcomes.append(out)

    ### Compute b0, b1 ###
    XbTXb = np.matrix(X_b).T * np.matrix(X_b)

    XaTXb = np.matrix(outcomes)[:-1]
    XbTXa = XaTXb.T

    XaTY = np.matrix(outcomes)[-1]
    XbTXb_exclY = XbTXb[:-1].T[:-1]
    XbTY = np.delete(XbTXb[-1], -1)

    print("XaTXa: " + str(len(XaTXa)) + " - " + str(len(XaTXa[0])))
    print("XbTXa: " + str(len(XbTXa)) + " - " + str(len(XbTXa[0])))
    print("XaTXb: " + str(len(XaTXb)) + " - " + str(len(XaTXb[0])))
    print("XbTXb: " + str(len(XbTXb)) + " - " + str(len(XbTXb[0])))
    print("XbTXb_exclY: " + str(len(XbTXb_exclY)) + " - " + str(len(XbTXb_exclY[0])))
    
    pp_XTX = np.concatenate((np.concatenate((XaTXa, XbTXa), axis=1), np.concatenate((XaTXb, XbTXb_exclY), axis=1)),axis=0) 
    pp_XTY = np.concatenate((XaTY, XbTY),axis=1).T

    pp_out = np.linalg.inv(pp_XTX) * pp_XTY

    b1 = pp_out[1:]
    b0 = pp_out.item(0)
    print('Coefficients: \n',  b1)
    print('Intercept: ', b0)
    
    return {
        "coefficients": b1.tolist(),
        "intercept": b0
    }
