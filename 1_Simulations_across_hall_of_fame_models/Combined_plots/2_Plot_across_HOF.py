import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

#pvalb
spikrate = pd.read_csv('../PvalbA_140Hz_AllHOF/Results/xxs.csv')
current = pd.read_csv('../PvalbA_140Hz_AllHOF/Results/crnts.csv')
veclengs = pd.read_csv('../PvalbA_140Hz_AllHOF/Results/yys.csv')
veclengctrl = pd.read_csv('../PvalbA_140Hz_AllHOF/Results/yysC.csv')

for r in range(len(spikrate)):
    for c in range(len(spikrate.T)):
        if spikrate.iloc[r,c]>180:
            spikrate.iloc[r,c] = np.nan
            current.iloc[r,c] = np.nan
            veclengs.iloc[r,c] = np.nan
            veclengctrl.iloc[r,c] = np.nan

pp = PdfPages('./2_Across_HOF.pdf')

# 2Hz moving average binning
for binsize in range (2,3):
    xs1 = []
    ys1 = []
    ymed1 = []
    xs2 = []
    ys2 = []
    ymed2 = []
    cnt = 0
    for i in range(0,196,binsize):
        xs1.append(i+binsize/2)
        ys1.append([])
        xs2.append(i+binsize/2)
        ys2.append([])
        for l in range(len(spikrate)):
            for c in range(len(spikrate.T)):
                if (spikrate.iloc[l,c]>=i) and (spikrate.iloc[l,c]<i+binsize):
                    ys1[cnt].append(veclengs.iloc[l,c])
                    ys2[cnt].append(veclengctrl.iloc[l,c])
        ymed1.append(np.median(ys1[cnt]))
        ymed2.append(np.median(ys2[cnt]))
        cnt += 1
    
    fig, ax = plt.subplots(figsize=(7,2.8))
    for i in range(len(spikrate)):
        Xvals = np.array(spikrate.iloc[i,:].dropna())[10:-20]
        Yvals = np.array(veclengs.iloc[i,:].dropna())[10:-20]
        sort_index = np.argsort(Xvals)
        ax.plot(Xvals[sort_index],Yvals[sort_index], linewidth=0.5 , color = '#CD3449',alpha = 0.3,label = None)
        
        Xvals = np.array(spikrate.iloc[i,:].dropna())[10:-20]
        Yvals = np.array(veclengctrl.iloc[i,:].dropna())[10:-20]
        sort_index = np.argsort(Xvals)
        ax.plot(Xvals[sort_index],Yvals[sort_index], linewidth=0.5 , c='deepskyblue',alpha = 0.3,label = None)
    ax.plot(xs2,ymed2,c='deepskyblue',label = 'Control', linewidth=2)
    ax.plot(xs1,ymed1,color = '#CD3449',label = '140 Hz ES', linewidth=2)
    ax.plot([140 , 140] , [-1 , 1.5] , '--k' , linewidth=2.0,alpha = 0.5)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel("Spike frequency (Hz)", fontsize=14)
    ax.set_ylabel("Control\n200 nA", fontsize=14)
    plt.legend(frameon=False,loc=(0.53,0.50), prop={'size': 12})
    ticks = np.linspace(35,175,5)
    ax.set_xticks(ticks)
    ax.set_xlim(99,190)
    ax.set_ylim(-0.05,1.05)
    fig.tight_layout()
    pp.savefig(fig)

fig, ax = plt.subplots(figsize=(7,2.8))
for i in range(len(spikrate)):
    if i!=11:
        ax.plot(current.iloc[i,:], spikrate.iloc[i,:], linewidth=0.5 , color = '#CD3449',alpha = 0.6,label = None)
ax.set_xlim(488,632)
ax.set_ylim(107.5,165)
ax.set_ylabel("Spike frequency (Hz)", fontsize=14)
ax.set_xlabel("Injected current (pA)", fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()
pp.savefig(fig)

#pyramidal
spikrate = pd.read_csv('../PyramidalA_8Hz_AllHOF/Results/xxs.csv')
current = pd.read_csv('../PyramidalA_8Hz_AllHOF/Results/crnts.csv')
veclengs = pd.read_csv('../PyramidalA_8Hz_AllHOF/Results/yys.csv')
veclengctrl = pd.read_csv('../PyramidalA_8Hz_AllHOF/Results/yysC.csv')

for r in range(len(spikrate)):
    for c in range(len(spikrate.T)):
        if spikrate.iloc[r,c]>15:
            spikrate.iloc[r,c] = np.nan
            current.iloc[r,c] = np.nan
            veclengs.iloc[r,c] = np.nan
            veclengctrl.iloc[r,c] = np.nan

# 2Hz moving average binning
for binsize in range (2,3):
    xs1 = []
    ys1 = []
    ymed1 = []
    xs2 = []
    ys2 = []
    ymed2 = []
    cnt = 0
    for i in range(0,196,binsize):
        xs1.append(i/10+binsize/20)
        ys1.append([])
        xs2.append(i/10+binsize/20)
        ys2.append([])
        for l in range(len(spikrate)):
            for c in range(len(spikrate.T)):
                if (spikrate.iloc[l,c]*10>=i) and (spikrate.iloc[l,c]*10<i+binsize):
                    ys1[cnt].append(veclengs.iloc[l,c])
                    ys2[cnt].append(veclengctrl.iloc[l,c])
        ymed1.append(np.median(ys1[cnt]))
        ymed2.append(np.median(ys2[cnt]))
        cnt += 1
    
    fig, ax = plt.subplots(figsize=(7,2.8))
    for i in range(len(spikrate)):
        Xvals = np.array(spikrate.iloc[i,:].dropna())
        Yvals = np.array(veclengs.iloc[i,:].dropna())
        sort_index = np.argsort(Xvals)
        ax.plot(Xvals[sort_index],Yvals[sort_index], linewidth=0.5 , color = '#009B81',alpha = 0.3,label = None)
        
        Xvals = np.array(spikrate.iloc[i,:].dropna())
        Yvals = np.array(veclengctrl.iloc[i,:].dropna())
        sort_index = np.argsort(Xvals)
        ax.plot(Xvals[sort_index],Yvals[sort_index], linewidth=0.5 , c='deepskyblue',alpha = 0.3,label = None)
    ax.plot(xs2,ymed2,c='deepskyblue',label = 'Control', linewidth=2)
    ax.plot(xs1,ymed1,color = '#009B81',label = '8 Hz ES', linewidth=2)
    ax.plot([8 , 8] , [-1 , 1.5] , '--k' , linewidth=2.0,alpha = 0.5)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel("Spike frequency (Hz)", fontsize=14)
    ax.set_ylabel("Entrainment\n(vector length)", fontsize=14)
    plt.legend(frameon=False,loc=(0.53,0.50), prop={'size': 12})
    ticks = np.linspace(0,60,16)
    ax.set_xticks(ticks)
    ax.set_xlim(4-0.69,13.714)
    ax.set_ylim(-0.05,1.05)
    fig.tight_layout()
    pp.savefig(fig)

fig, ax = plt.subplots(figsize=(7,2.8))
for i in range(len(spikrate)):
    if i!=5:
        ax.plot(current.iloc[i,:],spikrate.iloc[i,:], linewidth=0.5 , color = '#009B81',alpha = 0.6,label = None)
ax.set_xlim(165,200)
ax.set_ylim(1.75,14.5)
ax.set_ylabel("Spike frequency (Hz)", fontsize=14)
ax.set_xlabel("Injected current (pA)", fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()
pp.savefig(fig)
pp.close()    