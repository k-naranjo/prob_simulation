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

pop=pd.read_csv("pop1.csv")
race=pd.read_csv("race.csv")
people=pd.DataFrame() #initialize the vector 

for _ in range(5):
    r=random()
    
    aux=pop[pop.percentage>r].head(1)
    aux2=aux.iloc[0]
    age=rng.uniform(aux['age_min'],aux['age_max'],1)
    age=int(age)
    if aux2['sex']=="Female":
        sex='F'
    else:
        sex='M'
        
    r2=random()
    rac_row=race[  (race["age_min"]<=age) & (race["age_max"]>=age)  & (race["sex"]==aux2['sex'])  ]
    # if rac_row.iloc[[0],[2]]>10:
    #     print(rac_row['age_min'])
    rac_row=rac_row.iloc[0]

    c1=rac_row['upper_threshold_white']
    c2=rac_row['upper_threshold_black']
    # c3=rac_row['upper_threshold_aian']
    c4=rac_row['upper_threshold_asian']
    
    
    # if c>0.05:
    #     print(c)
    
    print(rac_row['upper_threshold_white'])
    #print(rac_row)
    # if rac_row['upper_threshold_white']>r2:
    #     race="w"
    # elif rac_row['upper_threshold_black']>r2:
    #     race="b"
    # elif rac_row['upper_threshold_aian']>r2:
    #     race="ai"
    # elif rac_row['upper_threshold_asian']>r2:
    #     race="a"
    # else:
    #     race="n"
    
    # if c1>r2:
    #     race="w"
    # elif c2>r2:
    #     race="b"
    # elif c3>r2:
    #     race="ai"
    # elif c4>r2:
    #     race="a"
    # else:
    #     race="n"
    
    
    # if rac_row.iloc[[0],[3]]>r2:
    #     race="w"
    # elif rac_row.iloc[[0],[4]]>r2:
    #     race="b"
    # elif rac_row.iloc[[0],[5]]>r2:
    #     race="ai"
    # elif rac_row.iloc[[0],[6]]>r2:
    #     race="a"
    # else:
    #     race="n"
    
        

    #rac_row=rac_row[rac_row.columns[3:7]]
    #rac2=rac_row.pivot(columns="d", values=rac_row.columns[3:7])
    #print(rac_row.iloc[0])

    people=people.append({'sex':sex,'age':age, 'race':race},ignore_index=True)


#print(pop[['sex', 'percentage']])





#may=people[(people['age']>28) & (people['age']<40)]

#may=race[  (race["age_min"]>=35) & (race["age_max"]<=39)  & (race["sex"]=="Male")   ]
#print(may)
#print(may["Upper threshold AIAN"])


#for _ in range(100):
#    r=random()
    
    

