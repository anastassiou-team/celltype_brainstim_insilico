targetMean = 8
targetStd = 1.5
initStep = 0

import pandas as pd

resultsMean = []
resultsStd = []
for i in range(40):
    base_name = 'R:/Temp/Threads2/Thread'+str(i)+'/Simulation/output/Data.csv'
    df = pd.read_csv(base_name)
    if df.iloc[0,0]>1000:
        resultsMean.append(0)
    else:
        resultsMean.append(df.iloc[0,0])
    if df.iloc[1,0]>1000:
        resultsStd.append(0)
    else:
        resultsStd.append(df.iloc[1,0])

vdf = pd.read_csv('./required_files/Values.csv')
vdf['Done'] = 0
alldone = 1
for i in range(40):
    if not resultsMean[i]:
        if vdf.iloc[i,4]<targetMean:
            vdf.iloc[i,0] = vdf.iloc[i,0] - vdf.iloc[i,2]
            vdf.iloc[i,2] = vdf.iloc[i,2]/2
        else:
            vdf.iloc[i,0] = vdf.iloc[i,0] + vdf.iloc[i,2]
            vdf.iloc[i,2] = vdf.iloc[i,2]/2
        continue
    cond1 = (abs(resultsMean[i]-targetMean)<0.01 and abs(resultsStd[i]-targetStd)<0.01)
    cond2 = (vdf.iloc[i,2] <= 0.00000000000000005) and (vdf.iloc[i,3] <= 0.00000000000000005)
    if cond1 or cond2:
        vdf.iloc[i,6] = 1
        vdf.iloc[i,4] = resultsMean[i]
        vdf.iloc[i,5] = resultsStd[i]
        continue
    if initStep:
        if abs(resultsMean[i]-targetMean)>0.1:
            vdf.iloc[i,2] = 0.001
        if abs(resultsStd[i]-targetStd)>0.1:
            vdf.iloc[i,3] = 0.001
    if resultsMean[i]>targetMean:
        if vdf.iloc[i,4]<targetMean:
            if vdf.iloc[i,2]>0.00000000000000005:
                if abs(resultsMean[i]-targetMean)>0.1:
                    vdf.iloc[i,2] = vdf.iloc[i,2]*1.8
                vdf.iloc[i,2] = vdf.iloc[i,2]/2
            else:
                vdf.iloc[i,2] = 0.00000000000000005
            vdf.iloc[i,0] = vdf.iloc[i,0] - vdf.iloc[i,2]
        else:
            vdf.iloc[i,0] = vdf.iloc[i,0] - vdf.iloc[i,2]
    else:
        if vdf.iloc[i,4]>targetMean:
            if vdf.iloc[i,2]>0.00000000000000005:
                vdf.iloc[i,2] = vdf.iloc[i,2]/2
            else:
                vdf.iloc[i,2] = 0.00000000000000005
            vdf.iloc[i,0] = vdf.iloc[i,0] + vdf.iloc[i,2]
        else:
            vdf.iloc[i,0] = vdf.iloc[i,0] + vdf.iloc[i,2]
    vdf.iloc[i,4] = resultsMean[i]
    if vdf.iloc[i,0]>4:
        vdf.iloc[i,0] = 0
        vdf.iloc[i,2] = 0.001
    elif vdf.iloc[i,0]<0:
        vdf.iloc[i,0] = 2
        vdf.iloc[i,2] = 0.001
    if resultsStd[i]>targetStd:
        if vdf.iloc[i,5]<targetMean:
            if vdf.iloc[i,3]>0.00000000000000005:
                if abs(resultsStd[i]-targetStd)>0.1:
                    vdf.iloc[i,3] = vdf.iloc[i,3]*1.8
                vdf.iloc[i,3] = vdf.iloc[i,3]/2
            else:
                vdf.iloc[i,3] = 0.00000000000000005
            vdf.iloc[i,1] = vdf.iloc[i,1] - vdf.iloc[i,3]
        else:
            vdf.iloc[i,1] = vdf.iloc[i,1] - vdf.iloc[i,3]
    else:
        if vdf.iloc[i,5]>targetMean:
            if vdf.iloc[i,3]>0.00000000000000005:
                vdf.iloc[i,3] = vdf.iloc[i,3]/2
            else:
                vdf.iloc[i,3] = 0.00000000000000005
            vdf.iloc[i,1] = vdf.iloc[i,1] + vdf.iloc[i,3]
        else:
            vdf.iloc[i,1] = vdf.iloc[i,1] + vdf.iloc[i,3]
    vdf.iloc[i,5] = resultsStd[i]
    if vdf.iloc[i,1]>4:
        vdf.iloc[i,1] = 0
        vdf.iloc[i,3] = 0.001
    elif vdf.iloc[i,1]<0:
        vdf.iloc[i,1] = 0
        vdf.iloc[i,3] = 0.001
    alldone = 0
    
vdf.to_csv('./required_files/Values.csv', index = False)
if alldone:
    raise Exception("All done..")