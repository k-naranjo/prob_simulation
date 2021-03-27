# -*- coding: utf-8 -*-
"""
#Probabilistic simulator


"""


import pandas as pd
import numpy as np

#generate random floating point values 
from random import seed
from random import random
from numpy.random import default_rng

rng=default_rng()

#seed random number generator
seed(1)

pop=pd.read_csv("pop1.csv") #csv with age and sex info
race=pd.read_csv("race.csv") #csv race info
people=pd.DataFrame() #initialize the vector 

num_people=100

for _ in range(num_people):
    r=random()#random generator for sex and age
    
    aux=pop[pop.percentage>r].head(1) # get the row that corresponds to the given prob
    aux2=aux.iloc[0] #retrieve only the row, not the container
    age=rng.uniform(aux['age_min'],aux['age_max'],1)
    age=int(age)
    if aux2['sex']=="Female":
        sex='F'
    else:
        sex='M'
    
    r2=random() # race random generator 
     
    rac_row=race[(race['age_min']<=age) & (race['age_max']>=age) & (race['sex']==aux2['sex'])] #selecting rows based on condition 
     
    rac_row=rac_row.iloc[0]

    if rac_row['upper_threshold_white']>r2:
        race_v="w"
    elif rac_row['upper_threshold_black']>r2:
        race_v="b"
    elif rac_row['upper_threshold_aian']>r2:
        race_v="ai"
    elif rac_row['upper_threshold_asian']>r2:
        race_v="a"
    else:
        race_v="n"

    people=people.append({'sex':sex,
                          'age':age, 
                          'race':race_v,
                          'risk_factor':1,
                          'cluster':0,
                          'work':'u'
                          },
                          ignore_index=True)

for i, p in people.iterrows(): #assign a risk based on age 
    if p['age']<25:
        risk_m=0.1
    elif p['age']<45:
        risk_m=0.2
    elif p['age']<60:
        risk_m=0.7
    else:
        risk_m=1
    
    if p['race']!='b':
        risk_m=risk_m*0.5 #if there are people black, they have a higher isk to get the disease 
        

    print("the risk the multiplier is "+str(risk_m))
    people.at[i,'risk_factor']=p['risk_factor']*risk_m
    
    if p['age']<4:
        people.at[i,'work']='f' #family
    elif p['age']<18:
        people.at[i,'work']='s' #students
    elif p['age']<70:
        print("pending...")
    else:
        people.at[i,'work']='r' #retirees


    