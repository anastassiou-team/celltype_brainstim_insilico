from matplotlib.backends.backend_pdf import PdfPages
import h5py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

gg = PdfPages('./0_Traces.pdf')

#PVALBA
nwb_file = '../PvalbA/1_Supplemental/569998751_ephys.nwb'
with h5py.File(nwb_file, "r") as f: #Read spike train file
    acq = f['acquisition']
    timeser = acq['timeseries'] #Depends on network name (NetworkBuilder BMTK)
    sw48 = timeser['Sweep_48']
    data1=sw48['data'][()]
    sw51 = timeser['Sweep_51']
    data2=sw51['data'][()]
f.close()

df1 = pd.DataFrame(data1)*1000+100
df1['time'] = df1.index/5
df1 = df1.reset_index(drop = True).iloc[9000*5:21500*5,:]

df2 = pd.DataFrame(data2)*1000+100
df2['time'] = df2.index/5+14000
df2 = df2.reset_index(drop = True).iloc[9000*5:21500*5,:]

sim_file1 = '../PvalbA/1_Supplemental/SimulationL/output/v_report.h5'
sim_file2 = '../PvalbA/1_Supplemental/SimulationH/output/v_report.h5'

with h5py.File(sim_file1, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf1 = pd.DataFrame(data)+15
sf1['current'] = -150
sf1['current'] = np.where(sf1.index>=100000, 350/10-150, sf1['current'])
sf1['current'] = np.where(sf1.index>200000, -150, sf1['current'])
sf1['time'] = sf1.index+1900
sf1 = sf1.iloc[90000:215000,:]

with h5py.File(sim_file2, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf2 = pd.DataFrame(data)+15
sf2['current'] = -150
sf2['current'] = np.where(sf2.index>=100000, 410/10-150, sf2['current'])
sf2['current'] = np.where(sf2.index>200000, -150, sf2['current'])
sf2['time'] = sf2.index+1900+140000
sf2 = sf2.iloc[90000:215000,:]

fig, ax = plt.subplots(figsize=(4,5))
ax.plot(df1['time'],df1.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf1['time']/10,sf1.iloc[:,0],color = '#CD3449', label = 'Simulation')
ax.plot(sf1['time']/10,sf1['current'],color = 'grey', label = 'Current')
ax.plot(df2['time'],df2.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf2['time']/10,sf2.iloc[:,0],color = '#CD3449', label = 'Simulation')
ax.plot(sf2['time']/10,sf2['current'],color = 'grey', label = 'Current')
ax.set_ylim(-160,200)
ax.set_xlim(9000,37000)
ax.set_ylabel("PVALB_A", fontsize = 10)
rect = matplotlib.patches.Rectangle((34800, -140), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -54,'25 mV',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((34800, -55), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -139,'250 pA',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((30200, -141), 2500, 2.5, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(29500, -152,'250 ms', fontsize = 9)
fig.tight_layout()
gg.savefig(fig)

#PVALBB
nwb_file = '../PvalbB/1_Supplemental/471077853_ephys.nwb'
with h5py.File(nwb_file, "r") as f: #Read spike train file
    acq = f['acquisition']
    timeser = acq['timeseries'] #Depends on network name (NetworkBuilder BMTK)
    sw56 = timeser['Sweep_56']
    data1=sw56['data'][()]
    sw59 = timeser['Sweep_59']
    data2=sw59['data'][()]
f.close()
df1 = pd.DataFrame(data1)*1000+100
df1['time'] = df1.index/20
df1 = df1.reset_index(drop = True).iloc[9000*20:21500*20,:]

df2 = pd.DataFrame(data2)*1000+100
df2['time'] = df2.index/20+14000
df2 = df2.reset_index(drop = True).iloc[9000*20:21500*20,:]

sim_file1 = '../PvalbB/1_Supplemental/SimulationL/output/v_report.h5'
sim_file2 = '../PvalbB/1_Supplemental/SimulationH/output/v_report.h5'

with h5py.File(sim_file1, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf1 = pd.DataFrame(data)+15
sf1['current'] = -150
sf1['current'] = np.where(sf1.index>=100000, 450/10-150, sf1['current'])
sf1['current'] = np.where(sf1.index>200000, -150, sf1['current'])
sf1['time'] = sf1.index+1900
sf1 = sf1.iloc[90000:215000,:]

with h5py.File(sim_file2, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf2 = pd.DataFrame(data)+15
sf2['current'] = -150
sf2['current'] = np.where(sf2.index>=100000, 510/10-150, sf2['current'])
sf2['current'] = np.where(sf2.index>200000, -150, sf2['current'])
sf2['time'] = sf2.index+1900+140000
sf2 = sf2.iloc[90000:215000,:]

fig, ax = plt.subplots(figsize=(4,5))
ax.plot(df1['time'],df1.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf1['time']/10,sf1.iloc[:,0],color = '#CD3449', label = 'Simulation')
ax.plot(sf1['time']/10,sf1['current'],color = 'grey', label = 'Current')
ax.plot(df2['time'],df2.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf2['time']/10,sf2.iloc[:,0],color = '#CD3449', label = 'Simulation')
ax.plot(sf2['time']/10,sf2['current'],color = 'grey', label = 'Current')
ax.set_ylim(-160,200)
ax.set_xlim(9000,37000)
ax.set_ylabel("PVALB_B", fontsize = 10)
rect = matplotlib.patches.Rectangle((34800, -140), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -54,'25 mV',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((34800, -55), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -139,'250 pA',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((30200, -141), 2500, 2.5, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(29500, -152,'250 ms', fontsize = 9)
fig.tight_layout()
gg.savefig(fig)

#PYRAMA
nwb_file = '../PyramidalA/1_Supplemental/488698339_ephys.nwb'

with h5py.File(nwb_file, "r") as f: #Read spike train file
    acq = f['acquisition']
    timeser = acq['timeseries'] #Depends on network name (NetworkBuilder BMTK)
    sw44 = timeser['Sweep_44']
    data1=sw44['data'][()]
    sw47 = timeser['Sweep_47']
    data2=sw47['data'][()]
f.close()
df1 = pd.DataFrame(data1)*1000+100
df1['time'] = df1.index/20
df1 = df1.reset_index(drop = True).iloc[9000*20:21500*20,:]

df2 = pd.DataFrame(data2)*1000+100
df2['time'] = df2.index/20+14000
df2 = df2.reset_index(drop = True).iloc[9000*20:21500*20,:]

sim_file1 = '../PyramidalA/1_Supplemental/SimulationL/output/v_report.h5'
sim_file2 = '../PyramidalA/1_Supplemental/SimulationH/output/v_report.h5'

with h5py.File(sim_file1, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf1 = pd.DataFrame(data)+15
sf1['current'] = -150
sf1['current'] = np.where(sf1.index>=100000, 190/10-150, sf1['current'])
sf1['current'] = np.where(sf1.index>200000, -150, sf1['current'])
sf1['time'] = sf1.index+1900
sf1 = sf1.iloc[90000:215000,:]

with h5py.File(sim_file2, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf2 = pd.DataFrame(data)+15
sf2['current'] = -150
sf2['current'] = np.where(sf2.index>=100000, 250/10-150, sf2['current'])
sf2['current'] = np.where(sf2.index>200000, -150, sf2['current'])
sf2['time'] = sf2.index+1900+140000
sf2 = sf2.iloc[90000:215000,:]

fig, ax = plt.subplots(figsize=(4,5))
ax.plot(df1['time'],df1.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf1['time']/10,sf1.iloc[:,0],color = '#009B81', label = 'Simulation')
ax.plot(sf1['time']/10,sf1['current'],color = 'grey', label = 'Current')
ax.plot(df2['time'],df2.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf2['time']/10,sf2.iloc[:,0],color = '#009B81', label = 'Simulation')
ax.plot(sf2['time']/10,sf2['current'],color = 'grey', label = 'Current')
ax.set_ylim(-160,200)
ax.set_xlim(9000,37000)
ax.set_ylabel("PYRAM_B", fontsize = 10)
rect = matplotlib.patches.Rectangle((34800, -140), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -54,'25 mV',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((34800, -55), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -139,'250 pA',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((30200, -141), 2500, 2.5, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(29500, -152,'250 ms', fontsize = 9)
fig.tight_layout()
gg.savefig(fig)

#PYRAMB
nwb_file = '../PyramidalB/1_Supplemental/354190011_ephys.nwb'

with h5py.File(nwb_file, "r") as f: #Read spike train file
    acq = f['acquisition']
    timeser = acq['timeseries'] #Depends on network name (NetworkBuilder BMTK)
    sw50 = timeser['Sweep_50']
    data1=sw50['data'][()]
    sw53 = timeser['Sweep_53']
    data2=sw53['data'][()]
f.close()
df1 = pd.DataFrame(data1)*1000+100
df1['time'] = df1.index/20
df1 = df1.reset_index(drop = True).iloc[9000*20:21500*20,:]

df2 = pd.DataFrame(data2)*1000+100
df2['time'] = df2.index/20+14000
df2 = df2.reset_index(drop = True).iloc[9000*20:21500*20,:]

sim_file1 = '../PyramidalB/1_Supplemental/SimulationL/output/v_report.h5'
sim_file2 = '../PyramidalB/1_Supplemental/SimulationH/output/v_report.h5'

with h5py.File(sim_file1, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf1 = pd.DataFrame(data)+15
sf1['current'] = -150
sf1['current'] = np.where(sf1.index>=100000, 210/10-150, sf1['current'])
sf1['current'] = np.where(sf1.index>200000, -150, sf1['current'])
sf1['time'] = sf1.index+1900
sf1 = sf1.iloc[90000:215000,:]

with h5py.File(sim_file2, "r") as f: #Read spike train file
    rep = f['report']
    sineu = rep['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data=sineu['data'][()]
f.close()
sf2 = pd.DataFrame(data)+15
sf2['current'] = -150
sf2['current'] = np.where(sf2.index>=100000, 270/10-150, sf2['current'])
sf2['current'] = np.where(sf2.index>200000, -150, sf2['current'])
sf2['time'] = sf2.index+1900+140000
sf2 = sf2.iloc[90000:215000,:]

fig, ax = plt.subplots(figsize=(4,5))
ax.plot(df1['time'],df1.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf1['time']/10,sf1.iloc[:,0],color = '#009B81', label = 'Simulation')
ax.plot(sf1['time']/10,sf1['current'],color = 'grey', label = 'Current')
ax.plot(df2['time'],df2.iloc[:,0],color = 'deepskyblue', label = 'Experimental')
ax.plot(sf2['time']/10,sf2.iloc[:,0],color = '#009B81', label = 'Simulation')
ax.plot(sf2['time']/10,sf2['current'],color = 'grey', label = 'Current')
ax.set_ylim(-160,200)
ax.set_xlim(9000,37000)
ax.set_ylabel("PYRAM_B", fontsize = 10)
rect = matplotlib.patches.Rectangle((34800, -140), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -54,'25 mV',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((34800, -55), 250, 25, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(35500, -139,'250 pA',rotation=90, fontsize = 8.6)
rect = matplotlib.patches.Rectangle((30200, -141), 2500, 2.5, linewidth=1, edgecolor='k', facecolor='k')
ax.add_patch(rect)
ax.text(29500, -152,'250 ms', fontsize = 9)
fig.tight_layout()
gg.savefig(fig)

gg.close()