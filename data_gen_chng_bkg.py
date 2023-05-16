import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from scipy.stats import loguniform

def gen_signal(N, x0, w, w_rat, A, nu, bkg, peak=False):
    x = np.arange(N)
    y = np.ones(N) * bkg
    w_d = w_rat * w
    w_r = w
    
    # np.where()
    
    if peak==True:
        y_peak = np.exp(-((x-x0)/w_d)**nu) * A
        y_peak[:x0] = 0
        y += y_peak
        
        y_rise = np.exp(-(abs(x0-x)/w_r)**nu) * A
        y_rise[x0:] = 0
        y += y_rise

    y = np.random.poisson(y)
    if peak==True:
        return x, y, y_peak+y_rise
    else:
        y_peak = np.zeros(N)
        return x, y, y_peak+y_rise

def data_gen_chng_bkg(N_data=100000,N_tu=256,x0=(64, 196),w=(5,20),w_rat=(0.1,2.5),SNR=(1,200),nu=(1,5),bkg=(5,15),a=(-0.03,0.03),norm=True,all_peak=False):
    data, data_clean,data_slope = [],[],[]
    df = pd.DataFrame(columns=["x0", 'w_rat', "w_r", 'w_d', "A", 'SNR', 'nu', "bkg", "GRB", "a"], index=range(N_data))
    
    if all_peak == True:
        peak = [True,True]
    else:
        peak = [True,False]
    
    df["x0"] = np.random.randint(x0[0],x0[1],N_data)
    df['w_rat'] = np.random.uniform(w_rat[0],w_rat[1],N_data)
    df['w_d'] = np.random.uniform(w[0],w[1],N_data)
    df['w_r'] = df['w_rat'] * df['w_d']
    df['SNR'] = loguniform(SNR[0],SNR[1]).rvs(N_data)
    df["bkg"] = np.random.uniform(bkg[0],bkg[1],N_data)
    df['A'] = df['SNR'] * df['bkg']
    df['nu'] = np.random.uniform(nu[0],nu[1],N_data)
    #df["GRB"].loc[i] = peak[np.random.randint(2),N_data]
    df["GRB"] = np.random.choice(peak,size=N_data)
    df["a"] = np.random.uniform(a[0],a[1],N_data)
        
    for i in range(N_data):
    #    df["x0"].loc[i] = np.random.randint(x0[0],x0[1],N_data)
    #    df['w_rat'].loc[i] = np.random.uniform(w_rat[0],w_rat[1],N_data)
    #    df['w_d'].loc[i] = np.random.uniform(w[0],w[1],N_data)
    #    df['w_r'].loc[i] = df['w_rat'][i] * df['w_d'][i]
    #    df['SNR'].log[i] = np.random.uniform(SNR[0],SNR[1],N_data)
    #    df["bkg"].loc[i] = np.random.uniform(bkg[0],bkg[1],N_data)
    #    df['A'].loc[i] = SNR * df['bkg'].loc[i]
    #    df['nu'].loc[i] = np.random.uniform(nu[0],nu[1],N_data)
    #    df["GRB"].loc[i] = peak[np.random.randint(2),N_data]
    #    df["a"].loc[i] = np.random.uniform(a[0],a[1],N_data)
        
        if norm:
            x = gen_signal(N=N_tu, x0=df.x0.loc[i], w=df.w_d.loc[i],w_rat=df.w_rat.loc[i], A=df.A.loc[i], nu=df.nu.loc[i], bkg=df.bkg.loc[i], peak=df.GRB.loc[i])
            x_slope = df.a.loc[i] * np.arange(N_tu)
            combine = x[1]+x_slope
            combine_norm = (combine-min(combine))/np.ptp(combine)
            data.append(combine_norm)
            data_slope.append((x_slope-min(x_slope))/np.ptp(x_slope))
            if np.ptp(x[2]) == 0:
                data_clean.append(np.zeros_like(x[2]))
            else:
                data_clean.append((x[2]-min(x[2]))/np.ptp(x[2]))

        else:
            x = gen_signal(N=N_tu, x0=df.x0.loc[i], w=df.w_d.loc[i],w_rat=df.w_rat.loc[i], A=df.A.loc[i], nu=df.nu.loc[i], bkg=df.bkg.loc[i], peak=df.GRB.loc[i])
            x_slope = df.a.loc[i] * np.arange(N_tu)
            data.append(x[1]+x_slope)
            data_clean.append(x[2])
            data_slope.append(x_slope)
        
    X = np.array(data).reshape(-1, len(data[0]))
    X_clean = np.array(data_clean).reshape(-1, len(data_clean[0]))
    X_slope = np.array(data_slope).reshape(-1, len(data_slope[0]))
    y = df.GRB
    le = LabelEncoder() #encode target labels with value between 0 and n_classes-1
    le.fit(y) #fit label encoder
    y = le.transform(y) #transform labels to normalized encoding (True = 1, False = 0)

    return X, y, df, X_clean, X_slope