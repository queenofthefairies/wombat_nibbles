#import matplotlib.pyplot as plt
import numpy as np
import math
import cmath      
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit



####################################################################
# GET THE DATA
############################'########################################

sample_no = 1
#### first sample
if sample_no == 1:
     sample_name = '10pZn0pTe'
     big_dat_df = pd.read_csv('10pZn0pTe_MvsH_4K-10K.dat', sep=',', #skiprows=29,
                              encoding='cp1252', header = 30)#, #header=30)
     MvsH_start = 2269-30
     MvsH_end = 3990-30

#### second sample
if sample_no == 2:
     sample_name = '10pZn10pTe'
     big_dat_df = pd.read_csv('10pZn10pTe_MvsH_4K-10K.dat', sep=',', #skiprows=29,
                              encoding='cp1252', header = 30)#, #header=30)
     MvsH_start = 2272-30
     MvsH_end = 3079-30

     big_dat_df2 = pd.read_csv('10pZn10pTe_MvsH_44p5K-60K.dat', sep=',', #skiprows=29,
                               encoding='cp1252', header = 30)#, #header=30)
     MvsH_end2 = 942-30


MvsT_df = big_dat_df.loc[range(0,MvsH_start)] 
MvsT_df.to_csv('{0}_MvsT_0Oe.dat'.format(sample_name), index = False)
print('done MvsT')

if sample_no == 1:
     sat_mag_df = big_dat_df.loc[range(MvsH_end,len(big_dat_df))] 
if sample_no == 2:
     sat_mag_df = big_dat_df2.loc[range(941-30,1727-30)] 
sat_mag_df.to_csv('{0}_sat_mag.dat'.format(sample_name), index =False)
print('done sat mag')
#MvsT_df = big_dat_df[big_dat_df["Magnetic Field (Oe)"] == -0.0212818123400211]

temperatures_list = [4, 10, 15, 25, 30, 35]
for i in np.arange(40, 51, 0.5):
    temperatures_list.append(i)
for i in np.arange(51, 56, 1):
     temperatures_list.append(i)
temperatures_list.append(60.0)

MvsH_df = big_dat_df.loc[range(MvsH_start,MvsH_end)]

if sample_no == 1:
     pass
elif sample_no == 2:
     temperatures_list = temperatures_list[0:15]
for temperature in temperatures_list:
     temperature_df = MvsH_df[(MvsH_df['Temperature (K)'] < temperature+0.25) & (MvsH_df['Temperature (K)'] > temperature-0.25)]
     temperature_df.to_csv('{0}_MvsH_{1:.1f}K.dat'.format(sample_name, temperature), index=False)
     print('done MvsH {0:.1f} K data'.format(temperature))

if sample_no == 2:
     temperatures_list2 = []
     for i in np.arange(44.5, 52.5, 0.5):
          temperatures_list2.append(i)
     for i in [53, 54, 55, 60]:
          temperatures_list2.append(i)
     MvsH_df = big_dat_df2.loc[range(0,MvsH_end2)] 
     for temperature in temperatures_list2:
          temperature_df = MvsH_df[(MvsH_df['Temperature (K)'] < temperature+0.25) & (MvsH_df['Temperature (K)'] > temperature-0.25)]
          temperature_df.to_csv('{0}_MvsH_{1:.1f}K.dat'.format(sample_name, temperature), index=False)
          print('done MvsH {0:.1f} K data'.format(temperature))

     extra_temperatures_list = [56,57]
     MvsH_df = big_dat_df2.loc[range(1727-30,len(big_dat_df2))]
     for temperature in extra_temperatures_list:
          temperature_df = MvsH_df[(MvsH_df['Temperature (K)'] < temperature+0.25) & (MvsH_df['Temperature (K)'] > temperature-0.25)]
          temperature_df.to_csv('{0}_MvsH_{1:.1f}K.dat'.format(sample_name, temperature), index = False)
          print('done MvsH {0:.1f} K data'.format(temperature))

