clmns = ["1160", "1163", "1166", "1169", "1172", "1175", "1178", "1181", "1184", "1187", "1190", "1193", "1196", "1199", "1202", "1205"]
threads = len(clmns)

import pandas as pd
import sys,os

file_name = 'Cell'
idf = sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] 
at_least = 0
values = []
names = []
for i in range(threads):
    base_name = 'R:/Temp/Threads2/Thread'+str(i)+'/Simulation/output/InData.csv'
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