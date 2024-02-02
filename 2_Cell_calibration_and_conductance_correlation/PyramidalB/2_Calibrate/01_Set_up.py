file_name = 'CellJ.json'
model_name = 'hof_param_354190013_'

import os, shutil
import pandas as pd

vdf = pd.read_csv('./required_files/Values.csv')

#Create threads
os.mkdir('R:/Temp/Threads16/')
for i in range(40):
    base_name = 'R:/Temp/Threads16/Thread'+str(i)+'/'
    os.mkdir(base_name)
    os.mkdir(base_name+'neuronal_model/')
    shutil.copyfile('./required_files/neuronal_model/'+file_name.replace("J.json", "_rotated.swc"), base_name+'neuronal_model/Cell_rotated.swc')
    shutil.copyfile('./required_files/neuronal_model/hof_models_fixed/'+model_name+str(i)+'.json', base_name+'neuronal_model/CellJ_fixed.json')
    shutil.copyfile('./required_files/Simulation_(Main).py', base_name+'Simulation_(Main).py')
    shutil.copyfile('./required_files/ais_functions.py', base_name+'ais_functions.py')
    shutil.copyfile('./required_files/cell_functions.py', base_name+'cell_functions.py')
    shutil.copyfile('./required_files/neuronal_model/nrnmech.dll', base_name+'neuronal_model/nrnmech.dll')
    lines = []
    fin = open(base_name+'Simulation_(Main).py', "rt")
    cnt = 0
    for line in fin:
        if cnt == 0:
            lines.append('BaseDir = "R:/Temp/Threads16/Thread'+str(i)+'"\n')
        elif cnt == 1:
            lines.append('MeanCurr = '+str(vdf.iloc[i,0])+'\n')
        elif cnt == 2:
            lines.append('StdCurr = '+str(vdf.iloc[i,1])+'\n')
        else:
            lines.append(line)
        cnt += 1
    fin.close()
    fout = open(base_name+'Simulation_(Main).py', "wt")
    for line in lines:
        fout.write(line)
    fout.close()