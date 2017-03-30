#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 22:18:29 2016

@author: xueyan
"""

import pandas as pd
import numpy as np
import os
from sklearn import preprocessing
import re

from sklearn.model_selection import KFold     # this one is only available in Python 3.6
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


os.chdir('/Users/xueyan/Documents/French_Case')


FR_Raw_Data = pd.read_csv('Fr_New_ModelData_v1.csv')
print(FR_Raw_Data.shape)

#for QC
R_log_dummy_varlist = pd.read_csv('log_dummy_var_list.csv')
R_varlist = pd.read_csv('vars_list.csv')

feature_names_list = list(FR_Raw_Data.columns)

vars_for_log_trans = ["INSEE_Total_Pst_actifs", 
                       "INSEE_Pst_act_industrie",
                       "INSEE_Pst_act_construction",
                       "INSEE_Pst_act_commerceServices",
                       "INSEE_Pst_act_adm_publique",
                       "New_OK_CountManager",
                       "New_CountManager"]

vars_for_dum_trans = ["SituationStation",
                       "SituationBorder",
                       "SituationCoastal"]
                       
vars_with_boolean =  ["IsCC_Address","IsZA_Address",
                      "IsPharmacyInsurance", "IsPharmacyFOT", "IsZoneTownCenter",
                      "IsZoneTownRisky", "IsZoneTownSuburb", "IsZoneRural",
                      "IsZoneTownRural", "IsZoneTouristic", "IsHighlyFrequented"]               
                      
#vars_with_boolean_renamed = ["dummy_" + old_name for old_name in vars_with_boolean]                   

for i, var_name in enumerate(feature_names_list):
    
    if i == 0:
        
        new_var_names = []

    if var_name in vars_with_boolean:
        
        var_name = "dummy_" + var_name
        
    new_var_names.append(var_name)

    
print(new_var_names)

FR_Raw_Data.columns = new_var_names  #rename column names of the raw data; can try .rename() method later
print(list(FR_Raw_Data.columns))    
               

def log_transform(data, vars_list):
    
    data2 = data.copy()
    
    for col_name in data.columns:
        
        if col_name in vars_list:
            
            new_col_name = 'log_' + col_name
            
            data2[new_col_name] = np.log(data[col_name] + 1)
           
    return data2


data3 = log_transform(FR_Raw_Data, vars_for_log_trans)  # log tranform

temp_data_for_boolean = FR_Raw_Data[vars_for_dum_trans]  #select variables and transform to boolean variables

enc = preprocessing.OneHotEncoder(sparse=False)  #no sparse data
enc_tool = enc.fit(temp_data_for_boolean)
boolean_tranformed_data =enc_tool.transform(temp_data_for_boolean)


for col in vars_for_dum_trans:
    
    print(temp_data_for_boolean[col].value_counts())  #check the frequency


col_names = ["SituationStation.1","SituationStation.2","SituationStation.3",
             "SituationBorder.0", "SituationBorder.1", "SituationBorder.2", "SituationBorder.3",
             "SituationCoastal.0", "SituationCoastal.1"]      #convert back to data frame, will try to automate the naming process    
col_names = ["dummy_" + obj for obj in col_names]

boolean_tranformed_df = pd.DataFrame(boolean_tranformed_data, columns = col_names)

data4 = data3.drop(vars_for_dum_trans,axis=1)
#QC
[obj for obj in list(data4.columns) if re.search(r"^Situation", obj)]

data_merged = pd.merge(data4, boolean_tranformed_df, left_index=True, right_index=True, how='inner')  #merge data4 and boolean_tranformed_df by index since this is not re-ordering the data


lowercase_colnames = [x.lower() for x in list(data_merged.columns)]  #convert original columns to lower case 
data_merged.columns = lowercase_colnames
print(list(data_merged.columns) )#end of this covertion.

'''
use normal expression to extract variables for log-log model or 
'''

dropVars = ["code_onekey", "panel"]

#vars for normal model
vars = set(lowercase_colnames) - set(dropVars) - set([obj for obj in lowercase_colnames if re.search(r'^log', obj)]) - set([obj2 for obj2 in lowercase_colnames if re.search(r"^panel_", obj2)])
vars = list(vars)
print(len(vars))
#QC
[v for v in vars if v not in list(R_varlist['vars'])]
[s for s in list(R_varlist['vars']) if s not in vars]


#vars for log model
log_vars = set([obj for obj in lowercase_colnames if re.search(r'^log_|^lg|^dummy', obj)]) - set([obj2 for obj2 in lowercase_colnames if re.search(r'^log_panel_', obj2)])
log_vars = list(log_vars)
print(len(log_vars))
#QC
[v for v in log_vars if v not in list(R_log_dummy_varlist['log_dummy'])]
[s for s in list(R_log_dummy_varlist['log_dummy']) if s not in log_vars]

#response
response = [obj2 for obj2 in lowercase_colnames if re.search(r"^panel_", obj2)]

#log response
log_response = [obj2 for obj2 in lowercase_colnames if re.search(r'^log_panel_', obj2)]

#panel data and non-panel data
panel_data = data_merged[ np.isnan(data_merged.panel_catt_daily) == False] # there should be a better way, find out later

nonpanel_data = data_merged[np.isnan(data_merged.panel_catt_daily)]
#check panel data
var_std = panel_data.std(axis = 1)
np.sum(np.isnan(var_std))
cleaned = panel_data.dropna()
print(panel_data.shape)
print(cleaned.shape)

'''
test support vector regression 
'''
#Global Parameters --

STANDARDIZED =True
MODEL_FORM = 'original' #alternative is 'log-log'

#step 1 -- standardize x and y

def pre_process_data(input_data, model_form, standardized, nfold = 3):
    #1. select columns according to model_form
    if model_form == 'original':
        #
        x = input_data[vars]

        multiple_ys = input_data[response]

        print(x.head(3))
        
        print(multiple_ys.head(3))
        
    elif model_form == 'log-log':
        #
        x = input_data[log_vars]

        multiple_ys = input_data[log_response]

        print(x.head(3))
        
        print(multiple_ys.head(3))

    #record row index in case the data will be re-shuffled when being splitted into k folds

    row_indexes = list(x.index)

    #2. split the input data into nfold parts -- create indexes
    print('initialize nfolds...\n')
    kf = KFold(n_splits=nfold, random_state=123, shuffle=False)    
    
    #3. standardize selected data

    #initalized empty list --
    print('initialized an empty list to store final outcome... \n')
    outcome = []

    for train_index, test_index in kf.split(x):

        print('check training index and testing index...\n')

        print(train_index)
        print('\n')
        print(test_index)
        print('\n')


        print('split input data into training part and testing part... \n')
        train_x = x.iloc[train_index, : ]
        train_ys = multiple_ys.iloc[train_index, : ]
        print(train_x.head(5))
        print(train_ys.head(5))

        test_x =  x.iloc[test_index, : ]
        test_ys =  multiple_ys.iloc[test_index, : ]
        print(test_x.head(5))
        print(test_ys.head(5))
        
        if standardized:
            print('Standardize training and testing data...\n')
            # form transformers
            print('Form transformers for standardization ... \n')

            scaler_x = preprocessing.StandardScaler().fit(train_x)

            scaler_ys = preprocessing.StandardScaler().fit(train_ys)

            print('End of forming transformers\n')

            # transform...
            print('Start to standardize train_x and test_x... \n')

            train_x_scaled = scaler_x.transform(train_x)
            test_x_scaled =  scaler_x.transform(test_x)

            print('Start to standardize train_ys and test_ys... \n')
            train_ys_scaled = scaler_ys.transform(train_ys)
            test_ys_scaled = scaler_ys.transform(test_ys)
            print('End of standardization...\n')

            #convert back to DataFrame and keep same row indexes and column names
            train_x_scaled = pd.DataFrame(train_x_scaled, columns = list(train_x.columns), index = list(train_x.index))
            test_x_scaled = pd.DataFrame(test_x_scaled, columns = list(test_x.columns), index = list(test_x.index))

            train_ys_scaled = pd.DataFrame(train_ys_scaled, columns = list(train_ys.columns), index = list(train_ys.index))
            test_ys_scaled = pd.DataFrame(test_ys_scaled, columns = list(test_ys.columns), index = list(test_ys.index))


            print('Append standardized data... \n')
            outcome.append([ train_x_scaled, test_x_scaled, train_ys_scaled, test_ys_scaled])
            print('End of appending data... \n')

        else:

            print('Just append original training and testing data...\n')

            #just append original sampled data
            outcome.append([train_x, test_x, train_ys, test_ys])

            print('End of appending data')

    return outcome


#execute the function
test1 = pre_process_data(panel_data, MODEL_FORM, True)

test2 = pre_process_data(panel_data, MODEL_FORM, False)


#step 2 -- test one single SVR
COST = 1
MarketName =  'cahm'
Indexx = 0

if MODEL_FORM == 'original':
    y_name = [obj for obj in response if re.search(MarketName, obj)]
else:
    y_name = [obj for obj in log_response if re.search(MarketName, obj)]
#initialize estimators
#1
svr_lin = SVR(kernel='linear', C= COST)
#2
svr_rbf = SVR(kernel='rbf', C= COST, gamma = 0.1)
#3
svr_poly = SVR(kernel='poly', C= COST, degree = 2)

train_x = test1[Indexx][0]
test_x = test1[Indexx][1]

train_y = test1[Indexx][2][y_name]
test_y = test1[Indexx][3][y_name]
train_y2 = np.array(train_y).reshape(train_x.shape[0], )
test_y2 = np.array(test_y).reshape(test_x.shape[0], )

svr_rbf_model = svr_rbf.fit(train_x, train_y2)
svr_lin_model = svr_lin.fit(train_x, train_y2)
svr_poly_model = svr_poly.fit(train_x, train_y2)

lin_train_y_pred = svr_lin_model.predict(train_x)
lin_test_y_pred = svr_lin_model.predict(test_x)

lin_train_rsquare = r2_score(train_y2, lin_train_y_pred)
lin_test_rsquare = r2_score(test_y2, lin_test_y_pred)
print("Training Rsquare ", lin_train_rsquare)
print("Testing Rsquare ", lin_test_rsquare)


#step 3 -- do grid search: define a function





'''
print(test1.__len__())
print(test1[0][0].shape)
print(test1[0][1].shape)
print(test1[0][2].shape)
print(test1[0][3].shape)
print(test1[0][0].index)
print(test1[0][1].index)

print(test1[0][2].index)
print(test1[0][3].index)
print(test1[1][2].index)
print(test1[1][3].index)
print(test1[2][2].index)
print(test1[2][3].index)


kf = KFold(n_splits=3, random_state=123, shuffle=False)

for train_index, test_index in kf.split(panel_data):
    #print("TRAIN:", train_index,'\n')
    #print("TEST:", test_index, '\n')
    print(panel_data.iloc[train_index, : ].index)
    print(panel_data.iloc[test_index, :].index)
    print(panel_data.iloc[train_index, : ].head(3))
#end of testing KFold().
'''
