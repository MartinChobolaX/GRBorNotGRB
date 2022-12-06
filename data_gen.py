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
    if peak:
        return x, y, y_peak
    else:
        y_peak = np.zeros(N)
        return x, y, y_peak

def data_gen(N_data=100000,N_tu=256,x0=(64, 196),w=(5,20),A=(5,20),bkg=(5,15),a=(-0.03,0.03),norm=True):
    data, data_clean,data_slope,data_no_bkg = [],[],[],[]
    df = pd.DataFrame(columns=["x0", "w", "A", "bkg", "GRB", "a"], index=range(N_data))
    
    ## GENERATING RANDOM NUMBERS FOR CONSTANTS IN GIVEN RANGE
    for i in range(N_data):
        df["x0"].loc[i] = np.random.randint(x0[0],x0[1])
        df["w"].loc[i] = np.random.uniform(w[0],w[1])
        df["A"].loc[i] = np.random.uniform(A[0],A[1])
        df["bkg"].loc[i] = np.random.uniform(bkg[0],bkg[1])
        df["GRB"].loc[i] = [True,False][np.random.randint(2)]
        df["a"].loc[i] = np.random.uniform(a[0],a[1])
        
        
    ## GENERATING LIGHT CURVE
        x = gen_signal(N=N_tu, x0=df.x0.loc[i], w=df.w.loc[i], A=df.A.loc[i], bkg=df.bkg.loc[i], peak=df.GRB.loc[i])
    
    
    ## GENERATING LINEARLY CHANGING BACKGROUND
        x_slope = df.a.loc[i] * np.arange(N_tu)
        
        
    ## COMBINING LC WITH AND WITHOUT BKG
        combine = x[1]+x_slope
        combine_no_bkg = x[2]+x_slope
        
        
    ## NORMALIZING
        if norm:
            combine_norm = (combine-min(combine))/np.ptp(combine)
            combine_norm_no_bkg = (combine_no_bkg-min(combine_no_bkg))/np.ptp(combine_no_bkg)
            data.append(combine_norm)
            data_no_bkg.append(combine_norm_no_bkg)
            data_slope.append((x_slope-min(x_slope))/np.ptp(x_slope))
            if np.ptp(x[2]) == 0:
                data_clean.append(np.zeros_like(x[2]))
            else:
                data_clean.append((x[2]-min(x[2]))/np.ptp(x[2]))

        else:
            data.append(combine)
            data_clean.append(x[2])
            data_slope.append(x_slope)
            data_no_bkg.append(combine_norm_no_bkg)
    
    ## RESHAPING
    X = np.array(data).reshape(-1, len(data[0]))
    X_clean = np.array(data_clean).reshape(-1, len(data_clean[0]))
    X_slope = np.array(data_slope).reshape(-1, len(data_slope[0]))
    X_no_bkg = np.array(data_no_bkg).reshape(-1, len(data_no_bkg[0]))
    
    ## ENCODING (True = 1, False = 0)
    y = df.GRB
    le = LabelEncoder()
    le.fit(y) 
    y = le.transform(y) 

    return X, y, df, X_clean, X_slope, X_no_bkg

