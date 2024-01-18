file_name = 'CellJ.json'
Step = 0.1 #ms
Edel = 100 #ms
stopTime = [10000] #ms
rangesL = [10000] #phase calculation crop limit low
rangesH = [-10000] #phase calculation crop limit high
signalInd = 0

import pandas as pd
import matplotlib.pyplot as plt
import efel
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib

#Pvalb
for hof in range(0,1):
    data_exist = []
    Spike_Start = []
    results = []
    result = []
    result.append("Setup")
    result.append("Mean vector angle")
    result.append("Mean vector length")
    result.append("Spike rate")
    result.append("Current")
    results.append(result)
    for cnt in range(536,540,48):
        en=pd.read_csv('../PvalbA_140Hz_AllHOF/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../PvalbA_140Hz_AllHOF/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
        for i, cl in enumerate(co.columns):
            thrs = co.loc[rangesL[signalInd]*2:len(co)+rangesH[signalInd]*2,cl]
            thrs = (thrs.max()-thrs.min())/2+thrs.min()
            print(thrs)
            efel.setThreshold(thrs)
            trace1 = {}
            trace1['T'] = co.index*Step
            trace1['V'] = co.iloc[:,i]
            trace1['stim_start'] = [Edel]
            trace1['stim_end'] = [stopTime[signalInd]]
            traces = [trace1]
            Co_begin_indices = efel.getFeatureValues(traces, ['peak_indices'])[0]['peak_indices']
            trace1 = {}
            trace1['T'] = en.index*Step
            trace1['V'] = en.iloc[:,i]
            trace1['stim_start'] = [Edel]
            trace1['stim_end'] = [stopTime[signalInd]]
            traces = [trace1]
            En_begin_indices = efel.getFeatureValues(traces, ['peak_indices'])[0]['peak_indices']
            if (Co_begin_indices is None) or (En_begin_indices is None):
                continue
            if (len(Co_begin_indices) <100) or (len(En_begin_indices) <100):
                continue
        
            start = len(Co_begin_indices)
            stop = 0
            for j in range(len(Co_begin_indices)):
                if Co_begin_indices[j]<rangesL[signalInd]:
                    start = j
                if Co_begin_indices[j]<=len(co)+rangesH[signalInd]:
                    stop = j
            Spike_Start.append(Co_begin_indices[start+1:stop]-rangesL[signalInd])
            
            start = len(En_begin_indices)
            stop = 0
            for j in range(len(En_begin_indices)):
                if En_begin_indices[j]<rangesL[signalInd]:
                    start = j
                if En_begin_indices[j]<=len(en)+rangesH[signalInd]:
                    stop = j
            Spike_Start.append(En_begin_indices[start+1:stop]-rangesL[signalInd])
            print(cl)
            print (len(En_begin_indices))
            
            data_exist.append(cl)
        
    co = co.iloc[900:1700,:].reset_index(drop = True)
    en = en.iloc[900:1700,:].reset_index(drop = True)

    gg = PdfPages('./0_Traces.pdf')
    fig, ax1 = plt.subplots(figsize=(4.8,3.2))
    ax1.set_xlabel('Time (ms)', fontsize = 14)
    ax1.set_title('Membrane potential control (no ES)', fontsize = 14)
    ax1.plot(co.index/10,co.iloc[:,0]+50, linewidth=2, color = '#CD3449')
    ax1.set_xlabel('Time (ms)', fontsize = 14)
    ax1.set_title('Membrane potential 140Hz ES', fontsize = 14)
    ax1.plot(co.index/10+90,en.iloc[:,0]+50, linewidth=2, color = '#CD3449')
    ax1.set_xlabel('1mV 25mV 250ms 25ms', fontsize = 14)
    ax1.set_title('Extracellular current', fontsize = 14)
    ax1.plot(co.index/10+90,en['Reference']*100000+160, linewidth=2, color = 'grey')
    ax1.set_xlabel('500pA')
    ax1.set_title('Intracellular current', fontsize = 14)
    en.loc[en.index/10 >= 10, 'Reference'] = 25
    ax1.plot(co.index/10,en['Reference'], linewidth=2, color = 'grey')
    ax1.plot(co.index/10+90,en['Reference'], linewidth=2, color = 'grey')
    en.loc[en.index/10 >= 10, 'Reference'] = 0
    ax1.plot(co.index/10,en['Reference']+160, linewidth=2, color = 'grey')
    
    rect = matplotlib.patches.Rectangle((172, 140), 1, 20, linewidth=0.2, edgecolor='k', facecolor='k')
    ax1.add_patch(rect)
    ax1.text(173, 135,'1 mV',rotation=270, fontsize = 12)
    rect = matplotlib.patches.Rectangle((172, 60), 1, 20, linewidth=0.2, edgecolor='k', facecolor='k')
    ax1.add_patch(rect)
    ax1.text(173, 51,'25 mV',rotation=270, fontsize = 12)
    rect = matplotlib.patches.Rectangle((150, 15), 20, 1, linewidth=0.9, edgecolor='k', facecolor='k')
    ax1.add_patch(rect)
    ax1.text(148, 0,'20 ms', fontsize = 12.2)

    fig.tight_layout()
    gg.savefig(fig)

#Pyramidal
for hof in range(0,1):
    data_exist = []
    Spike_Start = []
    results = []
    result = []
    result.append("Setup")
    result.append("Mean vector angle")
    result.append("Mean vector length")
    result.append("Spike rate")
    result.append("Current")
    results.append(result)
    for cnt in range(242,243,48):
        en=pd.read_csv('../PyramidalA_8Hz_AllHOF/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../PyramidalA_8Hz_AllHOF/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
        for i, cl in enumerate(co.columns):
            thrs = co.loc[rangesL[signalInd]*2:len(co)+rangesH[signalInd]*2,cl]
            thrs = (thrs.max()-thrs.min())/2+thrs.min()
            print(thrs)
            efel.setThreshold(thrs)
            trace1 = {}
            trace1['T'] = co.index*Step
            trace1['V'] = co.iloc[:,i]
            trace1['stim_start'] = [Edel]
            trace1['stim_end'] = [stopTime[signalInd]]
            traces = [trace1]
            Co_begin_indices = efel.getFeatureValues(traces, ['peak_indices'])[0]['peak_indices']
            trace1 = {}
            trace1['T'] = en.index*Step
            trace1['V'] = en.iloc[:,i]
            trace1['stim_start'] = [Edel]
            trace1['stim_end'] = [stopTime[signalInd]]
            traces = [trace1]
            En_begin_indices = efel.getFeatureValues(traces, ['peak_indices'])[0]['peak_indices']
            if (Co_begin_indices is None) or (En_begin_indices is None):
                continue
            if (len(Co_begin_indices) <100) or (len(En_begin_indices) <100):
                continue
        
            start = len(Co_begin_indices)
            stop = 0
            for j in range(len(Co_begin_indices)):
                if Co_begin_indices[j]<rangesL[signalInd]:
                    start = j
                if Co_begin_indices[j]<=len(co)+rangesH[signalInd]:
                    stop = j
            Spike_Start.append(Co_begin_indices[start+1:stop]-rangesL[signalInd])
            
            start = len(En_begin_indices)
            stop = 0
            for j in range(len(En_begin_indices)):
                if En_begin_indices[j]<rangesL[signalInd]:
                    start = j
                if En_begin_indices[j]<=len(en)+rangesH[signalInd]:
                    stop = j
            Spike_Start.append(En_begin_indices[start+1:stop]-rangesL[signalInd])
            print(cl)
            print (len(En_begin_indices))
            
            data_exist.append(cl)
    en.iloc[1000:21000, -1] = en.iloc[1250:21250, -1]    
    co = co.iloc[:8500,:].reset_index(drop = True)
    en = en.iloc[:8500,:].reset_index(drop = True)

    fig, ax1 = plt.subplots(figsize=(4.8,3.2))
    ax1.set_xlabel('Time (ms)', fontsize = 14)
    ax1.set_title('Membrane potential control (no ES)', fontsize = 14)
    ax1.plot(co.index/10,co.iloc[:,0]+50, linewidth=2, color = '#009B81')
    ax1.set_xlabel('Time (ms)', fontsize = 14)
    ax1.set_title('Membrane potential 140Hz ES', fontsize = 14)
    ax1.plot(co.index/10+980,en.iloc[:,0]+50, linewidth=2, color = '#009B81')
    ax1.set_xlabel('1mV 25mV 250ms 25ms', fontsize = 14)
    ax1.set_title('Extracellular current', fontsize = 14)
    ax1.plot(co.index/10+980,en['Reference']*100000+160, linewidth=2, color = 'grey')
    ax1.set_xlabel('500pA')
    ax1.set_title('Intracellular current', fontsize = 14)
    en.loc[en.index/10 >= 100, 'Reference'] = 25
    ax1.plot(co.index/10,en['Reference'], linewidth=2, color = 'grey')
    ax1.plot(co.index/10+980,en['Reference'], linewidth=2, color = 'grey')
    en.loc[en.index/10 >= 100, 'Reference'] = 0
    ax1.plot(co.index/10,en['Reference']+160, linewidth=2, color = 'grey')
    
    rect = matplotlib.patches.Rectangle((1860, 140), 10, 20, linewidth=0.2, edgecolor='k', facecolor='k')
    ax1.add_patch(rect)
    ax1.text(1870, 135,'1 mV',rotation=270, fontsize = 12)
    rect = matplotlib.patches.Rectangle((1860, 60), 10, 20, linewidth=0.2, edgecolor='k', facecolor='k')
    ax1.add_patch(rect)
    ax1.text(1870, 51,'25 mV',rotation=270, fontsize = 12)
    rect = matplotlib.patches.Rectangle((1630, 15), 200, 1, linewidth=0.9, edgecolor='k', facecolor='k')
    ax1.add_patch(rect)
    ax1.text(1580, 0,'200 ms', fontsize = 12.2)

    fig.tight_layout()
    gg.savefig(fig)
    gg.close()