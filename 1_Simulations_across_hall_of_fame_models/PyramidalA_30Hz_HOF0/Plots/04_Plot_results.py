file_name = 'CellJ.json'
Step = 0.1 #ms
Edel = 100 #ms
stopTime = [20000] #ms
rangesL = [10000] #phase calculation crop limit low
rangesH = [-10000] #phase calculation crop limit high
signalInd = 0

import pycircstat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import efel
from scipy.signal import hilbert
from matplotlib.backends.backend_pdf import PdfPages
import neurom as nm
from neurom import viewer

# Locate spikes
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
    for cnt in range(50,500,48):
        en=pd.read_csv('../Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
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
            if (len(Co_begin_indices)==0) or (len(En_begin_indices)==0):
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
        
    co = co.iloc[rangesL[signalInd]:rangesH[signalInd]].reset_index(drop = True)
    en = en.iloc[rangesL[signalInd]:rangesH[signalInd]].reset_index(drop = True)
    en['Phase'] = np.unwrap(np.angle(hilbert(en['Reference']-en['Reference'].mean()))+np.pi/2)*180/np.pi%360
    pp = PdfPages('./Rose_plots_hof'+str(hof) +'.pdf')
    mFile = "../required_files/neuronal_model/" + file_name.replace("J.json", "_rotated.swc")
    m = nm.load_morphology(mFile)
    fig, ax = viewer.draw(m)
    ax.set_title(' ')
    ax.plot(50,0,'x')
    pp.savefig(fig)
    plt.close(fig)
    
    # Find ES corresponding phase for each spike
    Phase_lists = []
    for i in Spike_Start:
        Phase_list = []
        for j in i:
            Phase_list.append(en.iloc[j,-1])
        Phase_lists.append(Phase_list)
    
    for i, cl in enumerate(data_exist):
        if (len(Phase_lists[i*2])>0) and (len(Phase_lists[i*2+1])>0):
            #Create control rose hist
            radians = np.asarray(Phase_lists[i*2])*np.pi/180
            mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
            mean_phase_angle = mean_phase_rad*(180 / np.pi)
            mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
            mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
            fig = plt.figure()
            ax = plt.subplot(1, 1, 1, projection='polar')
            ax.set_ylim(0,1.2)
            Y, X = np.histogram(Phase_lists[i*2], bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
            Xp =(X[1:] + X[:-1]) / 2
            Xp = Xp * np.pi / 180
            normY = np.true_divide(Y, (np.max(Y)))
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="red", alpha=0.5, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"blue",alpha = 0.8)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2])/len(co)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Control '+cl)
            fig.tight_layout()
            pp.savefig(fig)
            plt.close(fig)
            result = []
            result.append("Control")
            result.append(round(mean_phase_angle))
            result.append(round(mean_vector_length,3))
            result.append((len(Phase_lists[i*2])/len(co)*10000))
            result.append(cl)
            results.append(result)
            
            #Create entrained rose hist
            radians = np.asarray(Phase_lists[i*2+1])*np.pi/180
            mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
            mean_phase_angle = mean_phase_rad*(180 / np.pi)
            mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
            mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
            fig = plt.figure()
            ax = plt.subplot(1, 1, 1, projection='polar')
            ax.set_ylim(0,1.2)
            Y, X = np.histogram(Phase_lists[i*2+1], bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
            Xp =(X[1:] + X[:-1]) / 2
            Xp = Xp * np.pi / 180
            normY = np.true_divide(Y, (np.max(Y)))
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="red", alpha=0.5, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"blue",alpha = 0.8)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2+1])/len(en)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Entrain '+cl)
            fig.tight_layout()
            pp.savefig(fig)
            plt.close(fig)
            result = []
            result.append("Entrain")
            result.append(round(mean_phase_angle))
            result.append(round(mean_vector_length,3))
            result.append((len(Phase_lists[i*2+1])/len(en)*10000))
            result.append(cl)
            results.append(result)
    pp.close()