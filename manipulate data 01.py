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

os.chdir('/Users/xueyan/Documents/French_Case')

FR_Raw_Data = pd.read_csv('Fr_New_ModelData_v1.csv')
FR_Raw_Data.shape

feature_names  = FR_Raw_Data.columns
print(feature_names)

#'Code_Onekey' in feature_names

feature_names_list = list(feature_names)

#new variables 
#feature_names_list2 = map(lambda x:x.lower(), feature_names_list)
#print(feature_names_list2)
#type(feature_names_list2)

feature_names_list3 = [x.lower() for x in feature_names_list]
#print(feature_names_list3)

vars_for_log_trans = ["INSEE_Total_Pst_actifs", 
                       "INSEE_Pst_act_industrie",
                       "INSEE_Pst_act_construction",
                       "INSEE_Pst_act_commerceServices",
                       "INSEE_Pst_act_adm_publique",
                       "New_OK_CountManager",
                       "New_CountManager"]

#len(vars_for_log_trans)

vars_for_dum_trans = ["SituationStation",
                       "SituationBorder",
                       "SituationCoastal"]

###

def log_transform(data, vars_list):
    
    data2 = data.copy()
    data3 = data.copy()
    
    for col_name in data.columns:
        if col_name in vars_list:
            
            print(col_name)
            data2[col_name] = np.log(data[col_name] + 1)
            
            print(data[col_name].head())
            print(data2[col_name].head())
            
            
            new_col_name = 'log_' + col_name
            print(new_col_name)
            data3[new_col_name] = np.log(data[col_name] + 1)
            print(data3[new_col_name].head())           
            
    return data3

#1
data3 = log_transform(FR_Raw_Data, vars_for_log_trans)
data3.shape
print(data3.columns)

#convert to boolean variables
temp_data_for_boolean = FR_Raw_Data[vars_for_dum_trans]
#check
#temp_data_for_boolean.head(20)
#temp_data_for_boolean.columns

enc = preprocessing.OneHotEncoder(sparse=False)  #no sparse data
enc_tool = enc.fit(temp_data_for_boolean)
boolean_tranformed_data =enc_tool.transform(temp_data_for_boolean)
boolean_tranformed_data
#print(boolean_tranformed_data.shape)
#print(boolean_tranformed_data[:10,])
#print(temp_data_for_boolean.head(10))

#convert back to data frame

for col in vars_for_dum_trans:
    
    print(temp_data_for_boolean[col].value_counts())
    
#will try to automate the naming process    
col_names = ["SituationStation_1","SituationStation_2","SituationStation_3",
             "SituationBorder_0", "SituationBorder_1", "SituationBorder_2", "SituationBorder_3",
             "SituationCoastal_0", "SituationCoastal_1"]    
boolean_tranformed_df = pd.DataFrame(boolean_tranformed_data, columns = col_names)
#boolean_tranformed_df.head(10)
#boolean_tranformed_df.index
#drop unwanted data columns contained in list vars_for_dum_trans
data4 = data3.drop(vars_for_dum_trans,axis=1)
#data4.shape
#data4.index

#merge data4 and boolean_tranformed_df by index since this is not re-ordering the data
data_merged = pd.merge(data4, boolean_tranformed_df, left_index=True, right_index=True, how='inner')
#data_merged.shape
#data_merged.head(3)

FR_Raw_Data.head(3)

'''
use normal expression to extract variables for log-log model or 
'''

