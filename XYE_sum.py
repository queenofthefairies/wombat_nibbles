# little script for adding GSAS-II xye files together

import pandas as pd

filename_list = ['WBT0102676_Y2SiO5_massive_single_xtal_small.xye',
                 'WBT0102677_Y2SiO5_massive_single_xtal_small.xye',
                 'WBT0102678_Y2SiO5_massive_single_xtal_small.xye']

dataframe_list = []
for file in filename_list:
    df = pd.read_csv(file,sep='\s+',skiprows = 2, header =None, names = ['X','Y','E'])
    dataframe_list.append(df)

#print(dataframe_list[0])

summed_XYE_df =  pd.DataFrame(data=None, columns = ['X','Y','E'])

init_df = dataframe_list[0]
summed_XYE_df['X'] = init_df['X'] 
summed_XYE_df['Y'] = init_df['Y']
summed_XYE_df['E'] = init_df['E']

for i in range(1,len(filename_list)):
    i_df = dataframe_list[i]
    summed_XYE_df['Y'] = summed_XYE_df['Y'] + i_df['Y'] 
    summed_XYE_df['E'] = summed_XYE_df['E'] + i_df['E'] 

print(summed_XYE_df)

summed_XYE_df.to_csv('summed_XYE.xye', sep=' ', header= False, index = False, float_format = '%.4f')
    
