#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import auc, roc_curve, confusion_matrix
def predict_graph_info(y_test, y_pred_keras): 
    fig, (ax0, ax1) = plt.subplots(1,2, figsize=(10, 5))
    
    
    # ROC
    fpr_keras, tpr_keras, thresholds_keras = roc_curve(y_test, y_pred_keras)
    auc_keras = auc(fpr_keras, tpr_keras)
    ax0.plot(fpr_keras, tpr_keras)
    
    
    # histogram
    ax1.hist(y_pred_keras, bins=20)
    
    
    # confusion_matrix
    cm = confusion_matrix(y_test, y_pred_keras >= 0.5)
    print('True Negatives: ', cm[0][0])
    print('False Positives: ', cm[0][1])
    print('False Negatives: ', cm[1][0])
    print('True Positives: ', cm[1][1])
    print('Total: ', np.sum(cm))
    print('True / False','-', cm[0][0]+cm[1][1],'/', cm[1][0]+cm[0][1],'-', (cm[0][0]+cm[1][1])*100/np.sum(cm),'/', (cm[1][0]+cm[0][1])*100/np.sum(cm))
    
    
    fig.tight_layout()
    plt.show()

