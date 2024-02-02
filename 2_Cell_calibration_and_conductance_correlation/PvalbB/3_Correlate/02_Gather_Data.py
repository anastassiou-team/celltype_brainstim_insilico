clmns = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]
threads = len(clmns)

import pandas as pd
import sys,os

file_name = 'Cell'
idf = sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] 
at_least = 0
values = []
names = []
for i in range(threads):
    base_name = 'R:/Temp/Threads11/Thread'+str(i)+'/Simulation/output/InData.csv'
    if os.path.exists(base_name):
        at_least = 1
        df = pd.read_csv(base_name)
        values.append(df.iloc[:,0])
        names.append(clmns[i])
if at_least:
    if 'Control' not in idf:
        values.append(df.iloc[:,-2])
        names.append('Reference')
    fr = pd.concat(values, axis=1)
    fr.columns = names
    fr.to_csv('./Results/'+idf+'.csv', index = False)
else:
    print("************************************")
    print("****NO DATA! CHANGE PARAMETERS******")
    print("************************************")