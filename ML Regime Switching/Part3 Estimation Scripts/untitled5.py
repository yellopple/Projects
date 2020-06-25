# -*- coding: utf-8 -*-
"""
FileIntro: Decision tree + random forest

Created on Thu Jun 25 18:17:47 2020

@author: Archer Zhu
"""

from sklearn import linear_model, tree, model_selection

parameters = [
    {'criterion': ['gini', 'entropy'], 'splitter': ['best', 'random'], 'max_depth': [2, 3, 4, 5], 'min_samples_split': [5]},
    {'criterion': ['gini', 'entropy'], 'splitter': ['best', 'random'], 'max_depth': [3], 'min_samples_split': [3, 5, 7, 9]}]

clf = model_selection.GridSearchCV(tree.DecisionTreeClassifier(), parameters, cv = model_selection.StratifiedKFold(n_splits = 10, shuffle = True, random_state = 2020))
clf.fit(x, y)
print('best score:', clf.best_score_)
print('best parameters: ', clf.best_params_)

d = 5 # tree depth
tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = d)

