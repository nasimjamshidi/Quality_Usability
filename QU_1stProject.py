import os,json
import numpy as np
import pandas as pd
from numpy import mean,append,average
from pandas import ExcelWriter
from numpy import savetxt

path_to_json = 'C:/Users/Nasim/Desktop/QU_1st/'
# Access to all .json files in the folder
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

pFrame_avg_concat=pd.DataFrame()
iFrame_avg_concat=pd.DataFrame()
pFrame_std_concat=pd.DataFrame()

for k in range(len(json_files)):
    with open(json_files[k]) as myfile:
         data = json.load(myfile)
    
    Frames_Access=data['I13']['segments'][0]['frames']

    Frames_Size = []
    Frames_Type = []


# Seperate the Frames_Access into  Frames_Size and Frames_Type
    for i in range(len(Frames_Access)):
        Frames_Size.append(Frames_Access[i]['frameSize'])
        Frames_Type.append(Frames_Access[i]['frameType'])

# Change the values of Frames_Type, from I/Non-I to 1/0
    for j in range(len(Frames_Type)):
        if Frames_Type[j]=='Non-I':
            Frames_Type[j]=0
        else:
            Frames_Type[j]=1
            
            
# Convert the values type from string to int            
    Frames_Size = list(map(int, Frames_Size))
    Frames_Type = list(map(int, Frames_Type))

# Convert the type from list to array
    Frames_Size = np.asarray(Frames_Size)
    Frames_Type = np.asarray(Frames_Type)


    All = np.concatenate((Frames_Size, Frames_Type))
    All2 = All.reshape((2,902));




    pFrame_avg =  []
    pFrame_std = []
    iFrame_avg =  []
    iFrame_std = []
    Mean_Frame_avg =  []
    Mean_Frame_std = []

# Create pFrame Avg and Std arrays including the average and Std values over Non-I Frame_type values   
    for i in range(0,np.shape(All2)[1],30):
        temp = All2[:,i:i+30]
        temp2 = np.delete(temp[0,:], np.where(temp[1,:] == 1)[0])
        pFrame_avg.append(average(temp2[:,]))
        pFrame_std.append (np.std(temp2[:,]))
   
# Create iFrame arrays including the average values over I Frame_type values   
    
    for i in range(0,np.shape(All2)[1],30):
        temp3 = All2[:,i:i+30]
        temp4 = np.delete(temp3[0,:], np.where(temp3[1,:] == 0)[0])
        iFrame_avg.append(average(temp4[:,]))
     
    

    pFrame_avg=pd.DataFrame(pFrame_avg, columns = [json_files[k]])
    pFrame_avg_concat = pd.concat([pFrame_avg_concat,pFrame_avg], axis=1)
    
    
    iFrame_avg=pd.DataFrame(iFrame_avg, columns = [json_files[k]])
    iFrame_avg_concat = pd.concat([iFrame_avg_concat,iFrame_avg], axis=1)
    # Fill the Nan-cells with the last cells values
    iFrame_avg_concat.fillna( method ='ffill', inplace = True)
    
    
    pFrame_std=pd.DataFrame(pFrame_std, columns = [json_files[k]])
    pFrame_std_concat = pd.concat([pFrame_std_concat,pFrame_std], axis=1)
    


    

writer = pd.ExcelWriter('C:/Users/Nasim/Desktop/QU_1st/QU_1stProject.xlsx', engine='xlsxwriter')
    

pFrame_avg_concat.to_excel (writer, index = False, header=True,sheet_name='pFrame_avg') 
iFrame_avg_concat.to_excel (writer, index = False, header=True,sheet_name='iFrame_avg')       
pFrame_std_concat.to_excel (writer, index = False, header=True,sheet_name='pFrame_std')       

      
    
writer.save()













