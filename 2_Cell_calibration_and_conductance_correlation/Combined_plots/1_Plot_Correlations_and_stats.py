import pycircstat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import efel
from scipy.signal import hilbert
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sn
from scipy.stats import pearsonr
from copy import copy
from matplotlib.patches import Rectangle

#PVALB
file_name = 'CellJ.json'
Step = 0.1 #ms
Edel = 100 #ms
stopTime = [10000] #ms
rangesL = [10000] #phase calculation crop limit low
rangesH = [-10000] #phase calculation crop limit high
signalInd = 0

#PVALBA
vls=[]
#Gather vector length values
for hof in range(1):
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
    for cnt in range(1):
        en=pd.read_csv('../PvalbA/3_Correlate/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../PvalbA/3_Correlate/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
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
    
    Phase_lists = []
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
        Phase_lists.append(Phase_list)
    
    for i, cl in enumerate(data_exist):
        if (len(Phase_lists[i*2])>0) and (len(Phase_lists[i*2+1])>0):
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
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#CD3449", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2])/len(co)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Control '+cl)
            ax.set_ylim([0,1])
            ax.set_yticks([])
            ax.tick_params(axis='y', colors='grey')
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Control")
            result.append((mean_phase_angle))
            result.append(round(mean_vector_length,3))
            result.append((len(Phase_lists[i*2])/len(co)*10000))
            result.append(cl)
            results.append(result)

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
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#CD3449", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2+1])/len(en)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Entrain '+cl)
            ax.set_ylim([0,1])
            ax.set_yticks([0.5,1])
            ax.set_yticklabels([0.5,1.0], fontsize=16)
            ax.tick_params(axis='y', colors='grey')
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Entrain")
            result.append((mean_phase_angle))
            result.append(round(mean_vector_length,3))
            result.append((len(Phase_lists[i*2+1])/len(en)*10000))
            result.append(cl)
            results.append(result)
            vls.append(round(mean_vector_length,3))

model = 'hof_param_569998790_'
    
vls = pd.DataFrame(vls)
valus = pd.read_csv('../PvalbA/3_Correlate/required_files/Values.csv')
for i in range (len(vls)):
    if (abs(valus.loc[i,'PM']-140)>0.1) or (abs(valus.loc[i,'PS']-5)>0.1):
        vls.iloc[i,0] = np.nan
pp = PdfPages('./1_Vector_lengthsPVA.pdf')

fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(np.arange(40),(vls),'o',color = "#CD3449")
ax.set_xlim(-0.95,40)
ax.set_xlabel("HOF model #", fontsize=14)
ax.set_xticks(np.linspace(0,40,11))
ax.set_ylabel("Entrainment\n(Vector Length)", fontsize=14)
ax.set_ylim(0,1)
ax.spines[['right', 'top']].set_visible(False)
fig.tight_layout()
pp.savefig(fig)
pp.close()

#Gather conductance values
rows = []
first_run = 1
for ii, name in enumerate(range(40)):
    inFile = "../PvalbA/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(name) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(name)
    
    values.append(vls.iloc[ii,0])
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])
combined = df.copy()
for ii in range(0,40):
    inFile = "../PvalbA/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(ii) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(ii)
    
    values.append(0)
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])

#Correlation
sn.set(font_scale=1.0)
sn.set(style="ticks")
def calculate_pvalues(df):
    p = []
    for i in range (len(df.T)):
        p.append(pearsonr(list(df.T.iloc[i,:]),list(df.T.iloc[1,:]))[1])
    return p[2:]

a = combined.copy()
a.drop(['ra', 'cm_axon', 'cm_soma', 'cm_dend', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.rename(columns={'Width': 'Entrainment\n(vector length)'})
a = a.dropna()
crl = a.corr().iloc[2:,1:2].dropna()
crl['pval'] = calculate_pvalues(a)

data_for_colors = crl.copy()
data_for_colors.loc[data_for_colors.pval <= 0.05/25, 'pval'] = -2
data_for_colors.loc[data_for_colors.pval > 0.05/25, 'pval'] = 0
indices = [i for i, x in enumerate(data_for_colors.iloc[:,-1]) if x !=0]
data_for_colors = data_for_colors.iloc[:,:-1]
cmap = copy(plt.get_cmap('bwr'))

fig, ax = plt.subplots(figsize=(2.2,6.6))
ax = sn.heatmap(data = data_for_colors, annot=False, cmap=cmap, vmin = -1, vmax = 1, linewidths=1,cbar_kws={'label': 'Correlation coefficient'})
for i in indices:
    ax.add_patch(Rectangle((0, i), 1, 1, fill=False, edgecolor='lime', lw=3))
fig.tight_layout()
plt.savefig("./1_CorrelationsPVA.pdf", format="pdf", bbox_inches="tight")

#Create conductance distribution heatmap
a = df.iloc[-40:,:].reset_index()
a.drop(['ra', 'Width', 'cm_axon', 'cm_soma', 'cm_dend', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.reindex().T
a['Min'] = a.min(axis=1)
a['Max'] = a.max(axis=1)
for i in range(len(a)):
    for j in range(len(a.T)-2):
        a.iloc[i,j] = (a.iloc[i,j]-a.iloc[i,-2])*2/(a.iloc[i,-1]-a.iloc[i,-2])-1
ameans = a.copy()
a['Min'] = float('nan')
a['Max'] = float('nan')
ameans.iloc[:,:-2] = float('nan')
fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True, figsize=(15, 6.2), gridspec_kw={'width_ratios': [1, 6.5]})
sn.heatmap(a.iloc[2:,:-2], annot=False, cmap="Spectral_r", fmt = '.1f', vmin = -1, vmax = 1, linewidths=.5, ax=ax2,square = True, cbar_kws={'shrink': 1, 'pad':0.02})
sn.heatmap(ax = ax1, data = ameans.iloc[2:,-2:], annot = True, fmt = '.2e', cmap = 'ocean',vmin = -1000000, vmax = 1500000, linewidths=.5, cbar=False)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90,fontsize = 14)
ax1.set_xticklabels(ax1.get_xticklabels(),fontsize = 14)
ax1.set_yticklabels(ax1.get_yticklabels(),fontsize = 14)
ax2.collections[0].colorbar.set_ticks([-1, 1])
ax2.collections[0].colorbar.set_ticklabels([t for t in ['Min','Max']],fontsize = 16)#,labelsize=20)

ax2.set_xlabel('HOF model #',fontsize = 18)
ax2.tick_params(left = False)
ax1.set_ylabel('Conductance parameter',fontsize = 18)
fig.tight_layout(pad=0.2)
plt.savefig("./1_ConductancesPVA.pdf", format="pdf", bbox_inches="tight")

#PVALBB
vls=[]
#Gather vector length values
for hof in range(1):
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
    for cnt in range(1):
        en=pd.read_csv('../PvalbB/3_Correlate/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../PvalbB/3_Correlate/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
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
    
    Phase_lists = []
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
        Phase_lists.append(Phase_list)
    
    for i, cl in enumerate(data_exist):
        if (len(Phase_lists[i*2])>0) and (len(Phase_lists[i*2+1])>0):
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
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#CD3449", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2])/len(co)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Control '+cl)
            ax.set_ylim([0,1])
            ax.set_yticks([])
            ax.tick_params(axis='y', colors='grey')
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Control")
            result.append((mean_phase_angle))
            result.append(round(mean_vector_length,3))
            result.append((len(Phase_lists[i*2])/len(co)*10000))
            result.append(cl)
            results.append(result)

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
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#CD3449", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2+1])/len(en)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Entrain '+cl)
            ax.set_ylim([0,1])
            ax.set_yticks([0.5,1])
            ax.set_yticklabels([0.5,1.0], fontsize=16)
            ax.tick_params(axis='y', colors='grey')
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Entrain")
            result.append((mean_phase_angle))
            result.append(round(mean_vector_length,3))
            result.append((len(Phase_lists[i*2+1])/len(en)*10000))
            result.append(cl)
            results.append(result)
            vls.append(round(mean_vector_length,3))

model = 'hof_param_471077857_'
    
vls = pd.DataFrame(vls)
valus = pd.read_csv('../PvalbB/3_Correlate/required_files/Values.csv')
for i in range (len(vls)):
    if (abs(valus.loc[i,'PM']-140)>0.1) or (abs(valus.loc[i,'PS']-5)>0.1):
        vls.iloc[i,0] = np.nan
pp = PdfPages('./1_Vector_lengthsPVB.pdf')

fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(np.arange(40),(vls),'o',color = "#CD3449")
ax.set_xlim(-0.95,40)
ax.set_xlabel("HOF model #", fontsize=14)
ax.set_xticks(np.linspace(0,40,11))
ax.set_ylabel("Entrainment\n(Vector Length)", fontsize=14)
ax.set_ylim(0,1)
ax.spines[['right', 'top']].set_visible(False)
fig.tight_layout()
pp.savefig(fig)
pp.close()

#Gather conductance values
rows = []
first_run = 1
for ii, name in enumerate(range(40)):
    inFile = "../PvalbB/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(name) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(name)
    
    values.append(vls.iloc[ii,0])
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])
combined = df.copy()
for ii in range(0,40):
    inFile = "../PvalbB/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(ii) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(ii)
    
    values.append(0)
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])

#Correlation
sn.set(font_scale=1.0)
sn.set(style="ticks")
def calculate_pvalues(df):
    p = []
    for i in range (len(df.T)):
        p.append(pearsonr(list(df.T.iloc[i,:]),list(df.T.iloc[1,:]))[1])
    return p[2:]

a = combined.copy()
a.drop(['ra', 'cm_axon', 'cm_soma', 'cm_dend', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.rename(columns={'Width': 'Entrainment\n(vector length)'})
a = a.dropna()
crl = a.corr().iloc[2:,1:2].dropna()
crl['pval'] = calculate_pvalues(a)

data_for_colors = crl.copy()
data_for_colors.loc[data_for_colors.pval <= 0.05/25, 'pval'] = -2
data_for_colors.loc[data_for_colors.pval > 0.05/25, 'pval'] = 0
indices = [i for i, x in enumerate(data_for_colors.iloc[:,-1]) if x !=0]
data_for_colors = data_for_colors.iloc[:,:-1]
cmap = copy(plt.get_cmap('bwr'))

fig, ax = plt.subplots(figsize=(2.2,6.6))
ax = sn.heatmap(data = data_for_colors, annot=False, cmap=cmap, vmin = -1, vmax = 1, linewidths=1,cbar_kws={'label': 'Correlation coefficient'})
for i in indices:
    ax.add_patch(Rectangle((0, i), 1, 1, fill=False, edgecolor='lime', lw=3))
fig.tight_layout()
plt.savefig("./1_CorrelationsPVB.pdf", format="pdf", bbox_inches="tight")

#Create conductance distribution heatmap
a = df.iloc[-40:,:].reset_index()
a.drop(['ra', 'Width', 'cm_axon', 'cm_soma', 'cm_dend', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.reindex().T
a['Min'] = a.min(axis=1)
a['Max'] = a.max(axis=1)
for i in range(len(a)):
    for j in range(len(a.T)-2):
        a.iloc[i,j] = (a.iloc[i,j]-a.iloc[i,-2])*2/(a.iloc[i,-1]-a.iloc[i,-2])-1
ameans = a.copy()
a['Min'] = float('nan')
a['Max'] = float('nan')
ameans.iloc[:,:-2] = float('nan')
fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True, figsize=(15, 6.2), gridspec_kw={'width_ratios': [1, 6.5]})
sn.heatmap(a.iloc[2:,:-2], annot=False, cmap="Spectral_r", fmt = '.1f', vmin = -1, vmax = 1, linewidths=.5, ax=ax2,square = True, cbar_kws={'shrink': 1, 'pad':0.02})
sn.heatmap(ax = ax1, data = ameans.iloc[2:,-2:], annot = True, fmt = '.2e', cmap = 'ocean',vmin = -1000000, vmax = 1500000, linewidths=.5, cbar=False)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90,fontsize = 14)
ax1.set_xticklabels(ax1.get_xticklabels(),fontsize = 14)
ax1.set_yticklabels(ax1.get_yticklabels(),fontsize = 14)
ax2.collections[0].colorbar.set_ticks([-1, 1])
ax2.collections[0].colorbar.set_ticklabels([t for t in ['Min','Max']],fontsize = 16)#,labelsize=20)

ax2.set_xlabel('HOF model #',fontsize = 18)
ax2.tick_params(left = False)
ax1.set_ylabel('Conductance parameter',fontsize = 18)
fig.tight_layout(pad=0.2)
plt.savefig("./1_ConductancesPVB.pdf", format="pdf", bbox_inches="tight")

#PYRAMIDAL
file_name = 'CellJ.json'
Step = 0.1 #ms
Edel = 100 #ms
stopTime = [20000] #ms
rangesL = [10000] #phase calculation crop limit low
rangesH = [-10000] #phase calculation crop limit high
signalInd = 0

#PYRAMIDALA
vls=[]
#Gather vector length values
for hof in range(1):
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
    for cnt in range(1):
        en=pd.read_csv('../PyramidalA/3_Correlate/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../PyramidalA/3_Correlate/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
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
    
    Phase_lists = []
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
        Phase_lists.append(Phase_list)
    
    for i, cl in enumerate(data_exist):
        if (len(Phase_lists[i*2])>0) and (len(Phase_lists[i*2+1])>0):
            radians = np.asarray(Phase_lists[i*2])*np.pi/180
            mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
            mean_phase_angle = mean_phase_rad*(180 / np.pi)
            mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
            mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
            fig = plt.figure()
            ax = plt.subplot(1, 1, 1, projection='polar')
            ax.set_ylim(0,1)
            ax.set_yticks([])
            ax.tick_params(axis='y', colors='grey')
            Y, X = np.histogram(Phase_lists[i*2], bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
            Xp =(X[1:] + X[:-1]) / 2
            Xp = Xp * np.pi / 180
            normY = np.true_divide(Y, (np.max(Y)))
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#009B81", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2])/len(co)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Control '+cl)
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Control")
            result.append((mean_phase_angle))
            result.append((mean_vector_length))
            result.append((len(Phase_lists[i*2])/len(co)*10000))
            result.append(cl)
            results.append(result)
            
            radians = np.asarray(Phase_lists[i*2+1])*np.pi/180
            mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
            mean_phase_angle = mean_phase_rad*(180 / np.pi)
            mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
            mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
            fig = plt.figure()
            ax = plt.subplot(1, 1, 1, projection='polar')
            ax.set_ylim([0,1])
            ax.set_yticks([0.5,1])
            ax.set_yticklabels([0.5,1.0], fontsize=16)
            ax.tick_params(axis='y', colors='grey')
            Y, X = np.histogram(Phase_lists[i*2+1], bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
            Xp =(X[1:] + X[:-1]) / 2
            Xp = Xp * np.pi / 180
            normY = np.true_divide(Y, (np.max(Y)))
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#009B81", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2+1])/len(en)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Entrain '+cl)
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Entrain")
            result.append((mean_phase_angle))
            result.append((mean_vector_length))
            result.append((len(Phase_lists[i*2+1])/len(en)*10000))
            result.append(cl)
            results.append(result)
            vls.append(round(mean_vector_length,3))

model = 'hof_param_314822529_'
    
vls = pd.DataFrame(vls)
valus = pd.read_csv('../PyramidalA/3_Correlate/required_files/Values.csv')
for i in range (len(vls)):
    if (abs(valus.loc[i,'PM']-8)>0.1) or (abs(valus.loc[i,'PS']-1.5)>0.1):
        vls.iloc[i,0] = np.nan
pp = PdfPages('./1_Vector_lengthsPYA.pdf')

fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(np.arange(40),(vls),'o',color = "#009B81")
ax.set_xlim(-0.95,40)
ax.set_xlabel("HOF model #", fontsize=14)
ax.set_xticks(np.linspace(0,40,11))
ax.set_ylabel("Entrainment\n(Vector Length)", fontsize=14)
ax.set_ylim(0,1)
ax.spines[['right', 'top']].set_visible(False)
fig.tight_layout()
pp.savefig(fig)
pp.close()

#Gather conductance values
rows = []
first_run = 1
for ii, name in enumerate(range(40)):
    inFile = "../PyramidalA/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(name) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(name)
    
    values.append(vls.iloc[ii,0])
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])
combined = df.copy()
for ii in range(0,40):
    inFile = "../PyramidalA/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(ii) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(ii)
    
    values.append(0)
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])

#Correlation
sn.set(font_scale=1.0)
sn.set(style="ticks")
def calculate_pvalues(df):
    p = []
    for i in range (len(df.T)):
        p.append(pearsonr(list(df.T.iloc[i,:]),list(df.T.iloc[1,:]))[1])
    return p[2:]

a = combined.copy()
a.drop(['ra', 'cm_axon', 'cm_soma', 'cm_dend', 'cm_apic', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma','ena_apic', 'ek_apic', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.rename(columns={'Width': 'Entrainment\n(vector length)'})
crl = a.corr().iloc[2:,1:2].dropna()
crl['pval'] = calculate_pvalues(a)

data_for_colors = crl.copy()
data_for_colors.loc[data_for_colors.pval <= 0.05/29, 'pval'] = -2
data_for_colors.loc[data_for_colors.pval > 0.05/29, 'pval'] = 0
indices = [i for i, x in enumerate(data_for_colors.iloc[:,-1]) if x !=0]
data_for_colors = data_for_colors.iloc[:,:-1]
cmap = copy(plt.get_cmap('bwr'))

fig, ax = plt.subplots(figsize=(2.2,6.6))
ax = sn.heatmap(data = data_for_colors, annot=False, cmap=cmap, vmin = -1, vmax = 1, linewidths=1,cbar_kws={'label': 'Correlation coefficient'})
for i in indices:
    ax.add_patch(Rectangle((0, i), 1, 1, fill=False, edgecolor='lime', lw=3))
fig.tight_layout()
plt.savefig("./1_CorrelationsPYA.pdf", format="pdf", bbox_inches="tight")

#Create conductance distribution heatmap
a = df.iloc[-40:,:].reset_index()
a.drop(['ra','Width', 'cm_axon', 'cm_soma', 'cm_dend', 'cm_apic', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma','ena_apic', 'ek_apic', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.reindex().T
a['Min'] = a.min(axis=1)
a['Max'] = a.max(axis=1)
for i in range(len(a)):
    for j in range(len(a.T)-2):
        a.iloc[i,j] = (a.iloc[i,j]-a.iloc[i,-2])*2/(a.iloc[i,-1]-a.iloc[i,-2])-1
ameans = a.copy()
a['Min'] = float('nan')
a['Max'] = float('nan')
ameans.iloc[:,:-2] = float('nan')
fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True, figsize=(15, 6.2), gridspec_kw={'width_ratios': [1, 6.5]})
sn.heatmap(a.iloc[2:,:-2], annot=False, cmap="Spectral_r", fmt = '.1f', vmin = -1, vmax = 1, linewidths=.5, ax=ax2,square = True, cbar_kws={'shrink': 1, 'pad':0.02})
sn.heatmap(ax = ax1, data = ameans.iloc[2:,-2:], annot = True, fmt = '.2e', cmap = 'ocean',vmin = -1000000, vmax = 1500000, linewidths=.5, cbar=False)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90,fontsize = 14)
ax1.set_xticklabels(ax1.get_xticklabels(),fontsize = 14)
ax1.set_yticklabels(ax1.get_yticklabels(),fontsize = 14)
ax2.collections[0].colorbar.set_ticks([-1, 1])
ax2.collections[0].colorbar.set_ticklabels([t for t in ['Min','Max']],fontsize = 16)#,labelsize=20)

ax2.set_xlabel('HOF model #',fontsize = 18)
ax2.tick_params(left = False)
ax1.set_ylabel('Conductance parameter',fontsize = 18)
fig.tight_layout(pad=-3.2)
plt.savefig("./1_ConductancesPYA.pdf", format="pdf", bbox_inches="tight")

#PYRAMIDALB
vls=[]
#Gather vector length values
for hof in range(1):
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
    for cnt in range(1):
        en=pd.read_csv('../PyramidalB/3_Correlate/Results/Entrain_'+str(cnt)+'_'+str(hof)+'.csv')
        co=pd.read_csv('../PyramidalB/3_Correlate/Results/Control_'+str(cnt)+'_'+str(hof)+'.csv')
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
    
    Phase_lists = []
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
        Phase_lists.append(Phase_list)
    
    for i, cl in enumerate(data_exist):
        if (len(Phase_lists[i*2])>0) and (len(Phase_lists[i*2+1])>0):
            radians = np.asarray(Phase_lists[i*2])*np.pi/180
            mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
            mean_phase_angle = mean_phase_rad*(180 / np.pi)
            mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
            mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
            fig = plt.figure()
            ax = plt.subplot(1, 1, 1, projection='polar')
            ax.set_ylim(0,1)
            ax.set_yticks([])
            ax.tick_params(axis='y', colors='grey')
            Y, X = np.histogram(Phase_lists[i*2], bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
            Xp =(X[1:] + X[:-1]) / 2
            Xp = Xp * np.pi / 180
            normY = np.true_divide(Y, (np.max(Y)))
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#009B81", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2])/len(co)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Control '+cl)
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Control")
            result.append((mean_phase_angle))
            result.append((mean_vector_length))
            result.append((len(Phase_lists[i*2])/len(co)*10000))
            result.append(cl)
            results.append(result)
            
            radians = np.asarray(Phase_lists[i*2+1])*np.pi/180
            mean_phase_rad = pycircstat.descriptive.mean(np.array(radians))
            mean_phase_angle = mean_phase_rad*(180 / np.pi)
            mean_pvalue_z=pycircstat.rayleigh(np.array(radians))
            mean_vector_length = pycircstat.descriptive.vector_strength(np.array(radians))
            fig = plt.figure()
            ax = plt.subplot(1, 1, 1, projection='polar')
            ax.set_ylim([0,1])
            ax.set_yticks([0.5,1])
            ax.set_yticklabels([0.5,1.0], fontsize=16)
            ax.tick_params(axis='y', colors='grey')
            Y, X = np.histogram(Phase_lists[i*2+1], bins=[0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360])
            Xp =(X[1:] + X[:-1]) / 2
            Xp = Xp * np.pi / 180
            normY = np.true_divide(Y, (np.max(Y)))
            bars = ax.bar(Xp, normY,  width=0.4, edgecolor = 'black', color="#009B81", alpha=0.8, linewidth=1.2)
            ax.set_axisbelow(True)
            thetaticks = np.arange(0,360,90)
            radius = [0,mean_vector_length]
            theta = [mean_phase_rad,mean_phase_rad]
            ax.plot(theta,radius,"black",linewidth = 2)
            ax.set_xlabel('Spiking rate: {:0.0f}Hz\nVector length: {:0.3f}\nVector angle: {:0.2f}'.format(round(len(Phase_lists[i*2+1])/len(en)*10000),mean_vector_length, mean_phase_rad * 180./np.pi), size=10, labelpad = 15)     
            ax.set_title('Entrain '+cl)
            fig.tight_layout()
            plt.close(fig)
            result = []
            result.append("Entrain")
            result.append((mean_phase_angle))
            result.append((mean_vector_length))
            result.append((len(Phase_lists[i*2+1])/len(en)*10000))
            result.append(cl)
            results.append(result)
            vls.append(round(mean_vector_length,3))

model = 'hof_param_354190013_'
    
vls = pd.DataFrame(vls)
valus = pd.read_csv('../PyramidalB/3_Correlate/required_files/Values.csv')
for i in range (len(vls)):
    if (abs(valus.loc[i,'PM']-8)>0.1) or (abs(valus.loc[i,'PS']-1.5)>0.1):
        vls.iloc[i,0] = np.nan
pp = PdfPages('./1_Vector_lengthsPYB.pdf')

fig, ax = plt.subplots(figsize=(3.5,2.8))
ax.plot(np.arange(40),(vls),'o',color = "#009B81")
ax.set_xlim(-0.95,40)
ax.set_xlabel("HOF model #", fontsize=14)
ax.set_xticks(np.linspace(0,40,11))
ax.set_ylabel("Entrainment\n(Vector Length)", fontsize=14)
ax.set_ylim(0,1)
ax.spines[['right', 'top']].set_visible(False)
fig.tight_layout()
pp.savefig(fig)
pp.close()

#Gather conductance values
rows = []
first_run = 1
for ii, name in enumerate(range(40)):
    inFile = "../PyramidalB/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(name) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(name)
    
    values.append(vls.iloc[ii,0])
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])
combined = df.copy()
for ii in range(0,40):
    inFile = "../PyramidalB/3_Correlate/required_files/neuronal_model/hof_models_fixed/" + model + str(ii) + ".json"
    fin = open(inFile, "rt")
   
    titles = []
    values = []
    titles.append("hof")
    titles.append("Width")
    values.append(ii)
    
    values.append(0)
    section = 1
    cm = 0
    ena = 0
    genome = 0
    temp = " "
    for line in fin:
        if section == 1:
            if "ra" in line:
                titles.append("ra")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "section" in line:
                titles.append("cm_"+line.split(":")[1].split('"')[1])
                cm = 1
            elif cm == 1:
                values.append(float(line.split(":")[1]))
                cm = 0
            elif "e_pas" in line:
                titles.append("e_pas")
                values.append(float(line.split(":")[1]))
                section = 2
        elif section:
            if "junction_potential" in line:
                titles.append("junction_potential")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "celcius" in line:
                titles.append("celcius")
                values.append(float(line.split(":")[1].split(",")[0]))
            elif "ena" in line:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 1
            elif ena == 1:
                titles.append("ena_"+line.split(":")[1].split('"')[1])
                titles.append("ek_"+line.split(":")[1].split('"')[1])
                ena = 2
            elif ena == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                ena = 0
            elif "v_init" in line:
                titles.append("v_init")
                values.append(float(line.split(":")[1]))
                section = 0
        else:
            if "section" in line:
                temp = line.split(":")[1].split('"')[1]
                genome = 1
            elif genome == 1:
                titles.append(line.split(":")[1].split('"')[1]+"_"+temp)
                genome = 2
            elif genome == 2:
                values.append(float(line.split(":")[1].split(",")[0]))
                genome = 0
    if first_run:
        rows.append(titles)
        rows.append(values)
        first_run = 0
    else:
        if titles != rows[0]:
            raise ValueError('Not all hof same!')
        else:
            rows.append(values)
            
df = pd.DataFrame(rows[1:], columns=rows[0])

#Correlation
sn.set(font_scale=1.0)
sn.set(style="ticks")
def calculate_pvalues(df):
    p = []
    for i in range (len(df.T)):
        p.append(pearsonr(list(df.T.iloc[i,:]),list(df.T.iloc[1,:]))[1])
    return p[2:]

a = combined.copy()
a.drop(['ra', 'cm_axon', 'cm_soma', 'cm_dend', 'cm_apic', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma','ena_apic', 'ek_apic', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.rename(columns={'Width': 'Entrainment\n(vector length)'})
a = a.dropna()
crl = a.corr().iloc[2:,1:2].dropna()
crl['pval'] = calculate_pvalues(a)

data_for_colors = crl.copy()
data_for_colors.loc[data_for_colors.pval <= 0.05/29, 'pval'] = -2
data_for_colors.loc[data_for_colors.pval > 0.05/29, 'pval'] = 0
indices = [i for i, x in enumerate(data_for_colors.iloc[:,-1]) if x !=0]
data_for_colors = data_for_colors.iloc[:,:-1]
cmap = copy(plt.get_cmap('bwr'))

fig, ax = plt.subplots(figsize=(2.2,6.6))
ax = sn.heatmap(data = data_for_colors, annot=False, cmap=cmap, vmin = -1, vmax = 1, linewidths=1,cbar_kws={'label': 'Correlation coefficient'})
for i in indices:
    ax.add_patch(Rectangle((0, i), 1, 1, fill=False, edgecolor='lime', lw=3))
fig.tight_layout()
plt.savefig("./1_CorrelationsPYB.pdf", format="pdf", bbox_inches="tight")

#Create conductance distribution heatmap
a = df.iloc[-40:,:].reset_index()
a.drop(['ra','Width', 'cm_axon', 'cm_soma', 'cm_dend', 'cm_apic', 'e_pas', 'junction_potential', 'ena_soma', 'ek_soma','ena_apic', 'ek_apic', 'ena_axon', 'ek_axon','ena_dend', 'ek_dend', 'v_init', 'g_pas_apic', 'g_pas_dend', 'g_pas_soma', 'g_pas_axon'],axis = 1, inplace = True)
strings1 = a.columns[:2]
strings2 = sorted(sorted(a.columns[2:]), key=lambda x: x[-4:], reverse=True)
strings = [j for i in [strings1, strings2] for j in i] 
a = a[strings]
a = a.reindex().T
a['Min'] = a.min(axis=1)
a['Max'] = a.max(axis=1)
for i in range(len(a)):
    for j in range(len(a.T)-2):
        a.iloc[i,j] = (a.iloc[i,j]-a.iloc[i,-2])*2/(a.iloc[i,-1]-a.iloc[i,-2])-1
ameans = a.copy()
a['Min'] = float('nan')
a['Max'] = float('nan')
ameans.iloc[:,:-2] = float('nan')
fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True, figsize=(15, 6.2), gridspec_kw={'width_ratios': [1, 6.5]})
sn.heatmap(a.iloc[2:,:-2], annot=False, cmap="Spectral_r", fmt = '.1f', vmin = -1, vmax = 1, linewidths=.5, ax=ax2,square = True, cbar_kws={'shrink': 1, 'pad':0.02})
sn.heatmap(ax = ax1, data = ameans.iloc[2:,-2:], annot = True, fmt = '.2e', cmap = 'ocean',vmin = -1000000, vmax = 1500000, linewidths=.5, cbar=False)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90,fontsize = 14)
ax1.set_xticklabels(ax1.get_xticklabels(),fontsize = 14)
ax1.set_yticklabels(ax1.get_yticklabels(),fontsize = 14)
ax2.collections[0].colorbar.set_ticks([-1, 1])
ax2.collections[0].colorbar.set_ticklabels([t for t in ['Min','Max']],fontsize = 16)#,labelsize=20)

ax2.set_xlabel('HOF model #',fontsize = 18)
ax2.tick_params(left = False)
ax1.set_ylabel('Conductance parameter',fontsize = 18)
fig.tight_layout(pad=-3.2)
plt.savefig("./1_ConductancesPYB.pdf", format="pdf", bbox_inches="tight")