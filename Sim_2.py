# -*- coding: utf-8 -*-
"""
#Probabilistic simulator


"""


import pandas as pd
import numpy as np
#import scipy as sci
#import scipy.stats

#generate random floating point values 
from random import seed
from random import random
from numpy.random import default_rng
#from scipy.stats import *


rng=default_rng() #random generator

#seed random number generator
seed(1)

pop=pd.read_csv("pop1.csv") #csv with age and sex info
race=pd.read_csv("race.csv") #csv race info
people=pd.DataFrame() #initialize the vector 

num_people=1000

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
                          'cluster':-1,
                          'work':'u'
                          },
                          ignore_index=True)
    

for i, p in people.iterrows(): 
    #assign a risk based on age 
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
        

    #print("the risk the multiplier is "+str(risk_m))
    people.at[i,'risk_factor']=p['risk_factor']*risk_m
    
    # assing a work profile
    if p['age']<4:
        people.at[i,'work']='f' #family
    elif p['age']<18:
        people.at[i,'work']='s' #students
    elif p['age']<70:
        #print("pending...")
        r=random()
        if r<0.25:
            people.at[i,'work']='h'
        elif r<0.4:
            people.at[i,'work']='e'
        else:
            people.at[i, 'work']='w'
    else:
        people.at[i,'work']='r' #retirees
    

#assign clusters

#elderly
eld=people[people['age']>75]
num_nh=round(0.03*len(eld))
prob_nh=0.5 #prob that the person lives in a nursing home
#print(len(eld))
print("this town has "+str(num_nh) + " nursing homes")
if num_nh!=0:
    for i, p in eld.iterrows():
        r=random() # roll a dice. It give us a random variable
        if r<prob_nh:
            rd=rng.integers(1,num_nh,1)
            people.at[i, 'cluster']=rd
    #        print("person assigned to nursing home # "+str(rd))

current_cluster=num_nh

# households
prob_alone=0.07
prob_ssp=0.1 # same sex partner
eligible_p=people[(people['cluster']==-1)& (people['age']>22)]
for i, p in eligible_p.iterrows():
    if p['cluster']==-1: # if someone hasn't been assigned to a cluster
        match_found=False
        if random()>prob_alone:# look for partner only if p doesn't live alone
            if random()<prob_ssp:
                possible_partners=people[(people['sex']==p['sex']) & (people['cluster']==-1)]
            else:
                possible_partners=people[(people['sex']!=p['sex']) & (people['cluster']==-1)]
            #find partner's age
            age_p=max(16,round(rng.normal(p['age'],4))) 
            match=possible_partners.iloc[(possible_partners['age']-age_p).abs().argsort()[:1]] #find the closest one to the desirable age
            
            #print("closest match is "+str(match))
            
            for j, m in match.iterrows():
                if m['age']>=16:
                    possible=True
                    age_diff=abs(m['age']-p['age']) #abs absolute value of the age difference., We do not care about who is older 
                    if age_diff>15 and random()<0.9: # age is different than 15 years, do a prob very small (roll a dice)
                        possible=False                        
                    if possible:
                        people.at[j,'cluster']=current_cluster
                        #print("j is " + str(j))
                        match_found=True
            
            #people.at[match.iloc[0].index,'cluster']=current_cluster
            if match_found:
                people.at[i,'cluster']=current_cluster
                #print("i is "+str(i))
                #print("we found a match! - "+str(current_cluster))
                current_cluster+=1
            
        else: #people who live alone
            people.at[i, 'cluster']=current_cluster
            current_cluster+=1
            print("current cluster is "+ str(current_cluster))
#assign clusters to children
eligible_children=people[(people ['cluster']==-1)& (people['age']<=18)]
for i, p in eligible_children.iterrows():
    if random()>0.95:#male parent
        eligible_parents=people[(people['sex']=='M')& (people['age']>p['age']+13)]
    else:
        eligible_parents=people[(people['sex']=='F')& (people['age']>p['age']+13)]
        
    #age_parent=round(rng.normal(p['age']+25,5)) 
    age_parent=round( max( rng.normal(p['age']+25,5),13 )    )
    
    match=eligible_parents.iloc[(eligible_parents['age']-age_parent).abs().argsort()[:1]]
    
    for j, m in match.iterrows():
        people.at[i,'cluster']=m['cluster']
        
    

#k=round(abs(rng.normal(25,4)))
#print("value is: "+str(k))
