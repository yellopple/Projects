# -*- coding: utf-8 -*-
"""
FileIntro:Part3 Model Valuation

Created on Wed Jun 24 23:22:50 2020

Purpose:
    1. Classification Scores
    2. Predicted Long/ Long+Short return 

@author: Archer Zhu
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle # for ploting colors

from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score, accuracy_score, precision_score
# roc uses decision function or p value to construct
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn import linear_model
# multi class
from sklearn.multiclass import OneVsRestClassifier 
from scipy import interp


def ROCcal(y_test, y_score):
    '''
    calculate fpr, tpr and roc_auc for model
    input:
        y_test is y label
        y_score is classifier.decision_function(x_test), can be p value or Z value, after taking threshold, it should become y_pred
    output:
        fpr, tpr, roc_auc: all dict type, containing 
    '''
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    # Compute ROC curve and ROC area for each class
    n_classes = y_score.shape[1] # can be multi class
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    # First aggregate all false positive rates
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

    # input for macro
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])
    mean_tpr /= n_classes
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    return fpr, tpr, roc_auc

def ROC_plot( fpr, tpr, roc_auc, n_classes):
    '''
    plot ROC figure
    input:
        fpr: a dictionary containing false positive rate
        tpr: a dictionary containing true positive rate
        roc_auc: a dictionary containing auc for the model
    '''
    plt.figure()
    lw=2 # line width
    # plot micro
    plt.plot(fpr["micro"], tpr["micro"],
             label='micro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["micro"]),
             color='deeppink', linestyle=':', linewidth=4)
    
    # plot macro
    plt.plot(fpr["macro"], tpr["macro"],
             label='macro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["macro"]),
             color='navy', linestyle=':', linewidth=4)
    
    # plot each class
    colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                 ''.format(i, roc_auc[i]))
    # plot diagnal line
    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    # settings
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC AUC')
    plt.legend(loc="lower right")
    plt.show()

def ClassificationScoring(y_actual, classifier, x_test):
    '''
    calculate classificiation scores and plot roc curve
    '''
    y_predict = classifier.predict(x_test)
    y_score = classifier.decision_function(x_test) # prob of hitting obtaining each point
    # prediction scores
    validation_score = {
            'Accuracy':accuracy_score((y_actual), (y_predict)),
            'Precision':precision_score((y_actual), (y_predict)),
            'F1':f1_score((y_actual), (y_predict), average='weighted')
            }
    fpr, tpr, roc_auc = ROCcal(y_actual, y_score)
    validation_score['ROC AUC'] = roc_auc
    # plot
    n_classes = y_score.shape[1]
    ROC_plot( fpr, tpr, roc_auc, n_classes)
    return validation_score

def Profitability(holding_direction, sp500, trading_style='cc'):
    '''
    calculate actual return from holding suggestions
    
    input:
        holding_direction: Series, 1 is long, 0 is not long, -1 is short
        sp500_return: Series, relevant returns, can be open to close, or close to close, depending on model
    '''
    if trading_style == 'cc':
        sp500_return = sp500.close.pct_change()
    elif trading_style == 'oo':
        sp500_return = sp500.open.pct_change()
    elif trading_style == 'oc':
        sp500_return = sp500.close / sp500.close - 1
    else:
        sp500_return = sp500.close.pct_change()
    return (holding_direction * sp500_return + 1).cumproduct()







