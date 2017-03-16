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

#from sklearn.model_selection import KFold  # this one is only available in Python 3.6
#from sklearn.cross_validation import KFold 
from sklearn import cross_validation

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
    elif model_form == 'log-log':
        
        #
    
    #2. split the input data into nfold parts
        
    #3. standardize selected data
    if standardized:
        
        #
        
    else:

  

    #end
    
#test KFold()    
kf = cross_validation.KFold(12, n_folds=3, shuffle= True, random_state = 123)
len(kf)
for train_index, test_index in kf:    
    print("TRAIN:", train_index, "TEST:", test_index)    
#end of testing KFold().


#step 2 -- test one single SVR


#step 3 -- do grid search



''' ----old code---
#the first way to get corresponding var list
def search_log_or_dum(col_list, str_pattern):
    
    colnames_stored =[]
    
    if str_pattern == 'log':
        
        for i, obj in enumerate(col_list):
            
            temp_searched = re.search(r'^log', obj)
            
            if temp_searched:
                
                colnames_stored.append(obj)
                
    elif str_pattern == 'dummy':
        
        for i, obj in enumerate(col_list):
            
            temp_searched = re.search(r'^dummy', obj)
            
            if temp_searched:
                
                colnames_stored.append(obj)
                
    
    return colnames_stored
    
log_vars = search_log_or_dum(lowercase_colnames, 'log')
dum_vars = search_log_or_dum(lowercase_colnames, 'dummy')


# the second, i.e the much simpler way to get var list
log_vars2 = [obj for obj in lowercase_colnames if re.search(r'^log', obj)]  
dum_vars2 = [obj for obj in lowercase_colnames if re.search(r'^dummy', obj)]

all_other_vars = [obj for obj in lowercase_colnames if obj not in log_vars2 + dum_vars2]

log_vars2.__add__(dum_vars2)  ==  log_vars2 + dum_vars2  # this gives the answer True

#1
response_var_list =  [obj for obj in all_other_vars if re.search(r'^panel', obj)]
print(response_var_list) #note: there is a variable called "panel" which should be removed later
response_var_list = list(set(response_var_list) - set(['panel']))

#2
none_log_indep = list(set(all_other_vars) - set(response_var_list + ['code_onekey', 'panel'] ))
print(len(none_log_indep))

#3
log_response_var_list = [obj for obj in log_vars2 if re.search(r'^log_panel', obj)]
print(log_response_var_list)

#4
log_indep = list(set(log_vars2) - set(log_response_var_list))
print(log_indep)
print(len(log_indep))

[obj for obj in lowercase_colnames if re.search(r'log|lg|dummy', obj)]
'''

