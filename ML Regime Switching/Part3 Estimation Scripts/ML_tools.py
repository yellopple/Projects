# -*- coding: utf-8 -*-
"""
FileIntro: ML tools

Created on Thu Jun 25 02:41:05 2020

@author: Archer Zhu
"""

# train test split
from sklearn import model_selection
x_train, x_test, y_train, y_test = model_selection.train_test_split(x_dummy, y, test_size = test_size, random_state = 624)

# one hot encoding
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(handle_unknown='ignore') 
X = [['Male', 1], ['Female', 3], ['Female', 2]]
enc.fit(X)
enc.categories_ # feature order check
enc.transform([['Female', 1], ['Male', 4]]).toarray() 
enc.inverse_transform([[0, 1, 1, 0, 0], [0, 0, 0, 1, 0]])
enc.get_feature_names(['gender', 'group'])# set feature names

# grid search

