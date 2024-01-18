clmns = ["962", "965", "968", "971", "974", "977", "980", "983", "986", "989", "992", "995", "998", "1001", "1004", "1007"]
threads = len(clmns)

import pandas as pd
import sys,os

file_name = 'Cell'
idf = sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] 
at_least = 0
values = []
names = []
for i in range(threads):
    base_name = 'R:/Temp/Threads6/Thread'+str(i)+'/Simulation/output/InData.csv'
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