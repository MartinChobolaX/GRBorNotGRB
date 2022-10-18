#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def gen_signal(N, x0, w, A, bkg, peak=False):
    x = np.arange(N)
    y = np.ones(N) * bkg
    
    if peak:
        y_peak = np.exp(-(x-x0)/w) * A
        y_peak[:x0] = 0
        y += y_peak
        
    y = np.random.poisson(y)

    return x, y

def data_gen(N_data=100000,N_tu=256,x0=(64, 196),w=(5,20),A=(5,25),bkg=(5,15)):
    data = []
    df = pd.DataFrame(columns=["x0", "w", "A", "bkg", "GRB"], index=range(N_data))
    for i in range(N_data):
        df["x0"].loc[i] = np.random.randint(x0[0],x0[1])
        df["w"].loc[i] = np.random.uniform(w[0],w[1])
        df["A"].loc[i] = np.random.uniform(A[0],A[1])
        df["bkg"].loc[i] = np.random.uniform(bkg[0],bkg[1])
        df["GRB"].loc[i] = [True,False][np.random.randint(2)]
        data.append(gen_signal(N=N_tu, 
                               x0=df.x0.loc[i], 
                               w=df.w.loc[i], 
                               A=df.A.loc[i], 
                               bkg=df.bkg.loc[i],
                               peak=df.GRB.loc[i])[1])
    X = np.array(data).reshape(-1, len(data[0]))
    y = df.GRB
    le = LabelEncoder() #encode target labels with value between 0 and n_classes-1
    le.fit(y) #fit label encoder
    y = le.transform(y) #transform labels to normalized encoding (True = 1, False = 0)

    return X, y, df

