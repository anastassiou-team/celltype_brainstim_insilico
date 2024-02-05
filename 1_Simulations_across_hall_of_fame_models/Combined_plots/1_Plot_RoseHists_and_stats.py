import pycircstat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import efel
from scipy.signal import hilbert
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

#pvalb
file_name = 'CellJ.json'
paths4 = ['PvalbA_8Hz_HOF0','PvalbA_30Hz_HOF0','PvalbA_140Hz_AllHOF']
Step = 0.1 #ms
Edel = 100 #ms
stopTime = [10000] #ms
rangesL = [10000] #phase calculation crop limit low
rangesH = [-10000] #phase calculation crop limit high
signalInd = 0

pp = PdfPages('./1_RoseHists_and_stats.pdf')
fig1, ax1 = plt.subplots(figsize=(3.5,3.5))
fig, ax = plt.subplots(3,2,figsize=(5.2,7)) 

listA = []
listB = []
listC = []
listD = []
listE = []

#Create rose histograms
for pth in range(len(paths4)):    
    hof = 0
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
    CoISI=[]
    for cnt in range(488,600,48):
        en=pd.read_csv('../'+paths4[pth]+'/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../'+paths4[pth]+'/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
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
            Co_ISIs = 10000/(Co_begin_indices[1:]-Co_begin_indices[:-1])
            trace1 = {}
            trace1['T'] = en.index*Step
            trace1['V'] = en.iloc[:,i]
            trace1['stim_start'] = [Edel]
            trace1['stim_end'] = [stopTime[signalInd]]
            traces = [trace1]
            En_begin_indices = efel.getFeatureValues(traces, ['peak_indices'])[0]['peak_indices']
            En_ISIs = 10000/(En_begin_indices[1:]-En_begin_indices[:-1])
            if (Co_begin_indices is None) or (En_begin_indices is None):
                continue
            if (Co_ISIs is None) or (En_ISIs is None):
                continue
            for k in Co_ISIs:
                CoISI.append(k)
        
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

    if pth==0:
        sns.set_style("ticks")
        sns.histplot(CoISI,bins=18, binrange = (0,200), color='#CD3449', stat='density',line_kws={'linewidth': 3},edgecolor="white", linewidth=3, ax=ax1)
        ax1.set_xlim(0,200)
        ax1.spines[['left','right', 'top']].set_visible(False)
    Co_rose = []
    En_rose = []
    for c,i in enumerate(Spike_Start):
        Phase_list = []
        for j in i:
            Phase_list.append(en.iloc[j,-1])
            if c%2:
                En_rose.append(en.iloc[j,-1])
            else:
                Co_rose.append(en.iloc[j,-1])
    
    radians = np.asarray(Co_rose)*np.pi/180
    mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
    mean_phase_angle = mean_phase_rad*(180 / np.pi)
    mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
    mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
    ax = plt.subplot(3, 2, (1+pth)*2-1, projection='polar')
    ax.set_ylim(0,1.2)
    Y, X = np.histogram(Co_rose, bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
    Xp =(X[1:] + X[:-1]) / 2
    Xp = Xp * np.pi / 180
    normY = np.true_divide(Y, (np.max(Y)))
    bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#CD3449", alpha=0.8, linewidth=1.2)
    ax.set_axisbelow(True)
    thetaticks = np.arange(0,360,90)
    radius = [0,mean_vector_length]
    theta = [mean_phase_rad,mean_phase_rad]
    ax.plot(theta,radius,"black",linewidth = 2)
    ax.set_ylim([0,1])
    ax.set_yticks([])
    ax.set_xticks(np.pi/180. * np.linspace(0,  360, 4, endpoint=False))
    lbs = []
    for x, label in zip(ax.get_xticks(), ax.get_xticklabels()):
        if x==np.pi:
            label.set_text('180°   ')
            lbs.append(label)
        elif x==np.pi/2 and pth==0:
            lbs.append(label)
        elif x==np.pi*3/2 and pth==2:
            lbs.append(label)
        else:
            lbs.append(label.set_text(' '))
    ax.set_xticklabels(lbs,fontsize=16)
    ax.tick_params(axis='y', colors='grey')
    
    listA.append(pth)
    listB.append(mean_vector_length)
    listD.append(-np.log10(mean_pvalue_z[0]))

    radians = np.asarray(En_rose)*np.pi/180
    mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
    mean_phase_angle = mean_phase_rad*(180 / np.pi)
    mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
    mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
    ax = plt.subplot(3, 2, (1+pth)*2, projection='polar')
    ax.set_ylim(0,1.2)
    Y, X = np.histogram(En_rose, bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
    Xp =(X[1:] + X[:-1]) / 2
    Xp = Xp * np.pi / 180
    normY = np.true_divide(Y, (np.max(Y)))
    bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#CD3449", alpha=0.8, linewidth=1.2)
    ax.set_axisbelow(True)
    thetaticks = np.arange(0,360,90)
    radius = [0,mean_vector_length]
    theta = [mean_phase_rad,mean_phase_rad]
    ax.plot(theta,radius,"black",linewidth = 2)
    ax.set_ylim([0,1])
    ax.set_yticks([0.5,1])
    ax.set_yticklabels([0.5,1.0], fontsize=16)
    ax.set_xticks(np.pi/180. * np.linspace(0,  360, 4, endpoint=False))
    lbs = []
    for x, label in zip(ax.get_xticks(), ax.get_xticklabels()):
        if x==0:
            lbs.append(label)
        elif x==np.pi/2 and pth==0:
            lbs.append(label)
        elif x==np.pi*3/2 and pth==2:
            lbs.append(label)
        else:
            lbs.append(label.set_text(' '))
    ax.set_xticklabels(lbs,fontsize=16)
    ax.tick_params(axis='y', colors='grey')
    listC.append(mean_vector_length)
    listE.append(-np.log10(mean_pvalue_z[0]))
    print(len(Co_rose))
fig.tight_layout()
fig1.tight_layout()
pp.savefig(fig)
pp.savefig(fig1)

#Plot vector length metrics
a = ['Control', '8 Hz', '30 Hz', '140 Hz']
pvb = [np.mean(listB)]
pvb.append(listC[0])
pvb.append(listC[1])
pvb.append(listC[2])
ppv = [np.mean(listD)]
ppv.append(listE[0])
ppv.append(listE[1])
if listE[2]>150:
    ppv.append(150)
else:
    ppv.append(listE[2])

stv = []
for i in range(len(ppv)):
    if ppv[i]>4:
        stv.append('****')
    elif ppv[i]>3:
        stv.append('***')
    elif ppv[i]>2:
        stv.append('**')
    elif ppv[i]>1.3:
        stv.append('*')
    else:
        stv.append('')
fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(a,pvb,'o-', color = '#CD3449')#, label = 'Pvalb')
ax.set_xlabel('ES Frequency (Hz)', fontsize=14)
ax.set_ylabel('Vector length', fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylim(0,0.35)
plt.legend(frameon=False,loc='upper left', prop={'size': 12})
fig.tight_layout()
pp.savefig(fig)

fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(a,ppv,'o-', color = '#CD3449')#, label = 'Pvalb')
ax.set_xlabel('ES Frequency (Hz)', fontsize=14)
ax.set_ylabel('Rayleigh\n-log10(p-value)', fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for i,s in enumerate(stv):
    if i:
        ax.text(x=a[i], y=ppv[i]+2, s=s, fontsize=14,horizontalalignment='center')
plt.legend(frameon=False,loc='upper left', prop={'size': 12})
fig.tight_layout()
pp.savefig(fig)

#Pyramidal
file_name = 'CellJ.json'
paths1 = ['PyramidalA_8Hz_AllHOF','PyramidalA_30Hz_HOF0','PyramidalA_140Hz_HOF0']

fig1, ax1 = plt.subplots(figsize=(3.5,3.5)) 
fig, ax = plt.subplots(3,2,figsize=(5.2,7)) 

listA = []
listB = []
listC = []
listD = []
listE = []

#Create rose histograms
for pth in range(len(paths1)):    
    hof = 0
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
    CoISI=[]
    for cnt in range(146,242,48):
        en=pd.read_csv('../'+paths1[pth]+'/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../'+paths1[pth]+'/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
        for i, cl in enumerate(co.columns):
            if int(cl)<190 or int(cl)>220:
                continue
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
            Co_ISIs = 10000/(Co_begin_indices[1:]-Co_begin_indices[:-1])
            trace1 = {}
            trace1['T'] = en.index*Step
            trace1['V'] = en.iloc[:,i]
            trace1['stim_start'] = [Edel]
            trace1['stim_end'] = [stopTime[signalInd]]
            traces = [trace1]
            En_begin_indices = efel.getFeatureValues(traces, ['peak_indices'])[0]['peak_indices']
            En_ISIs = 10000/(En_begin_indices[1:]-En_begin_indices[:-1])
            if (Co_begin_indices is None) or (En_begin_indices is None):
                continue
            if (Co_ISIs is None) or (En_ISIs is None):
                continue
            for k in Co_ISIs:
                CoISI.append(k)
        
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

    if pth==0:
        sns.set_style("ticks")
        sns.histplot(CoISI,bins=18, binrange = (0,20), color='#009B81', stat='density',line_kws={'linewidth': 3},edgecolor="white", linewidth=3, ax=ax1)
        ax1.set_xlim(0,20)
        ax1.spines[['left','right', 'top']].set_visible(False)
    Co_rose = []
    En_rose = []
    for c,i in enumerate(Spike_Start):
        Phase_list = []
        for j in i:
            Phase_list.append(en.iloc[j,-1])
            if c%2:
                En_rose.append(en.iloc[j,-1])
            else:
                Co_rose.append(en.iloc[j,-1])
    
    radians = np.asarray(Co_rose)*np.pi/180
    mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
    mean_phase_angle = mean_phase_rad*(180 / np.pi)
    mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
    mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
    ax = plt.subplot(3, 2, (1+pth)*2-1, projection='polar')
    ax.set_ylim(0,1.2)
    Y, X = np.histogram(Co_rose, bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
    Xp =(X[1:] + X[:-1]) / 2
    Xp = Xp * np.pi / 180
    normY = np.true_divide(Y, (np.max(Y)))
    bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#009B81", alpha=0.8, linewidth=1.2)
    ax.set_axisbelow(True)
    thetaticks = np.arange(0,360,90)
    radius = [0,mean_vector_length]
    theta = [mean_phase_rad,mean_phase_rad]
    ax.plot(theta,radius,"black",linewidth = 2)
    ax.set_ylim([0,1])
    ax.set_yticks([])
    ax.set_xticks(np.pi/180. * np.linspace(0,  360, 4, endpoint=False))
    lbs = []
    for x, label in zip(ax.get_xticks(), ax.get_xticklabels()):
        if x==np.pi:
            label.set_text('180°   ')
            lbs.append(label)
        elif x==np.pi/2 and pth==0:
            lbs.append(label)
        elif x==np.pi*3/2 and pth==2:
            lbs.append(label)
        else:
            lbs.append(label.set_text(' '))
            
    ax.set_xticklabels(lbs,fontsize=16)
    ax.tick_params(axis='y', colors='grey')
    
    listA.append(pth)
    listB.append(mean_vector_length)
    listD.append(-np.log10(mean_pvalue_z[0]))
    
    radians = np.asarray(En_rose)*np.pi/180
    mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
    mean_phase_angle = mean_phase_rad*(180 / np.pi)
    mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
    mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
    ax = plt.subplot(3, 2, (1+pth)*2, projection='polar')
    ax.set_ylim(0,1.2)
    Y, X = np.histogram(En_rose, bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
    Xp =(X[1:] + X[:-1]) / 2
    Xp = Xp * np.pi / 180
    normY = np.true_divide(Y, (np.max(Y)))
    bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#009B81", alpha=0.8, linewidth=1.2)
    ax.set_axisbelow(True)
    thetaticks = np.arange(0,360,90)
    radius = [0,mean_vector_length]
    theta = [mean_phase_rad,mean_phase_rad]
    ax.plot(theta,radius,"black",linewidth = 2)
    ax.set_ylim([0,1])
    ax.set_yticks([0.5,1])
    ax.set_yticklabels([0.5,1.0], fontsize=16)
    ax.set_xticks(np.pi/180. * np.linspace(0,  360, 4, endpoint=False))
    lbs = []
    for x, label in zip(ax.get_xticks(), ax.get_xticklabels()):
        if x==0:
            lbs.append(label)
        elif x==np.pi/2 and pth==0:
            lbs.append(label)
        elif x==np.pi*3/2 and pth==2:
            lbs.append(label)
        else:
            lbs.append(label.set_text(' '))
    ax.set_xticklabels(lbs,fontsize=16)
    ax.tick_params(axis='y', colors='grey')
    listC.append(mean_vector_length)
    listE.append(-np.log10(mean_pvalue_z[0]))
    print(len(Co_rose))
fig.tight_layout()
fig1.tight_layout()
pp.savefig(fig)
pp.savefig(fig1)

#Plot vector length metrics
pyr = [np.mean(listB)]
pyr.append(listC[0])
pyr.append(listC[1])
pyr.append(listC[2])
ppy = [np.mean(listD)]
ppy.append(listE[0])
ppy.append(listE[1])
ppy.append(listE[2])

sty = []
for i in range(len(ppv)):
    if ppy[i]>4:
        sty.append('****')
    elif ppy[i]>3:
        sty.append('***')
    elif ppy[i]>2:
        sty.append('**')
    elif ppy[i]>1.3:
        sty.append('*')
    else:
        sty.append('')

fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(a,pyr,'o-', color = '#009B81')#, label = 'Pyramidal')
ax.set_xlabel('ES Frequency (Hz)', fontsize=14)
ax.set_ylabel('Vector length', fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylim(0,0.35)
plt.legend(frameon=False,loc='upper left', prop={'size': 12})
fig.tight_layout()
pp.savefig(fig)

fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(a,ppy,'o-', color = '#009B81')#, label = 'Pyramidal')
ax.set_xlabel('ES Frequency (Hz)', fontsize=14)
ax.set_ylabel('Rayleigh\n-log10(p-value)', fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for i,s in enumerate(sty):
    if i:
        ax.text(x=a[i], y=ppy[i]+2, s=s, fontsize=14,horizontalalignment='center')
plt.legend(frameon=False,loc='upper left', prop={'size': 12})
fig.tight_layout()
pp.savefig(fig)

pp.close()