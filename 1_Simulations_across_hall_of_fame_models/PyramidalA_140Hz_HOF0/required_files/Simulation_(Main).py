BaseDir = "R:/Temp/Threads6/Thread0"
InnCurr = 150
import sys

file_name = 'Cell'
probeXs = [50] #um
probeYs = [0] #um
frequencies = [140] #Hz
ampltudes = [0.0002, 0] #Hz
DCampltudes = [0.25, 0.35, 0.45, 0.55, 0.65] #Hz
durations = [19900] #ms
stopTime = [20000] #ms
rangesL = [10000] #phase calculation crop limit low
rangesH = [-10000] #phase calculation crop limit high
resultsdir = BaseDir+'/Results/Results.txt'

probeXInd = 0
print ("Ex El X position: "+str(probeXs[int(probeXInd)]))
probeYInd = 0
print ("Ex El Y position: "+str(probeYs[probeYInd]))
signalInd = 0
AmpInd = sys.argv[1]
print ("Frequency: "+str(frequencies[signalInd]))
print ("Ampltude: "+str(ampltudes[int(AmpInd)]))
print ("Duration: "+str(durations[signalInd]))
print ("StopTime: "+str(stopTime[signalInd]))
print ("RangeL: "+str(rangesL[signalInd]))
print ("RangeH: "+str(rangesH[signalInd]))

#Simulation
Step = 0.1 #ms

#Intra
Iamp = InnCurr/1000 #nA
Idel = 100 #ms
Idur = durations[signalInd] #ms

#Extra
Eshp = "sin"
Eamp = ampltudes[int(AmpInd)] #mA
Edel = 100 #ms
Eoff = -0.00 #mA

from bmtk.builder.networks import NetworkBuilder
from bmtk.utils.sim_setup import build_env_bionet
from bmtk.simulator import bionet
import os, re, shutil, datetime, h5py
import pandas as pd
import numpy as np

print ("Started at "+str(datetime.datetime.now()))

#Build network (single cell)
net = NetworkBuilder('single_neuron')
net.add_nodes(cell_name=file_name,
              potental='exc',
              model_type='biophysical',
              model_template='ctdb:Biophys1.hoc',
              model_processing='aibs_perisomatic',
              dynamics_params=file_name+'J_fixed.json',
              morphology=file_name+'_rotated.swc')

net.build()
net.save_nodes(output_dir=BaseDir+'/Model')
print ("Network done.")

#Preset simulation (only to create files)
build_env_bionet(
    base_dir=BaseDir+'/Simulation',
    config_file='config.json',
    network_dir=BaseDir+'/Model',
    tstop=durations[signalInd], dt=Step,
    report_vars=['v', 'cai'],
    current_clamp={
        'amp': Iamp,
        'delay': Idel,
        'duration': Idur
    },
    include_examples=False,
    compile_mechanisms=False
)

#Set simulation (poke files and set values)
sim_file=BaseDir+'/Simulation/simulation_config.json'
f = open(sim_file,'r')
filedata = f.read()
f.close()

#Replace dummy input with intra and extra stimulation
filedata=re.sub('"inputs": {.*?},','"inputs": {\n    \
"current_clamp": {\n      \
"input_type": "current_clamp",\n      \
"module": "IClamp",\n      \
"node_set": "all",\n      \
"gids": "all",\n      \
"amp": '+str(Iamp)+',\n      \
"delay": '+str(Idel)+',\n      \
"duration": '+str(Idur)+'\n    \
},\n    \
"extra_stim": {\n      \
"input_type": "lfp",\n      \
"module": "xstim",\n      \
"node_set": "all",\n      \
"positions_file": "$BASE_DIR/inputs/xstim_electrode.csv",\n      \
"waveform": {\n        \
"shape": "'+Eshp+'",\n        \
"del": '+str(Edel)+',\n        \
"amp": '+str(Eamp)+',\n        \
"freq": '+str(frequencies[signalInd])+',\n        \
"offset": '+str(Eoff)+',\n        \
"dur": '+str(durations[signalInd])+'\n      \
}\n    \
}\n  \
},',filedata, flags=re.DOTALL)

#Replace calcium report with vd (dendrites) reports within reports section
filedata=re.sub('"cai_report": {.*?}','"v_dend": {\n      \
"variable_name": "v",\n      \
"cells": "all",\n      \
"module": "membrane_report",\n      \
"sections": "dend"\n    \
}',filedata, flags=re.DOTALL)
f = open(sim_file,'w')
f.write(filedata)
f.close()
print ("Simulation set.")

#Copy component files
os.mkdir(BaseDir+'/Simulation/inputs/')
f = open(BaseDir+'/Simulation/inputs/xstim_electrode.csv', 'w')

#Extracellular stimuli probe
Epositions=[]
Epositions.append('ip pos_x pos_y pos_z rotation_x rotation_y rotation_z\n')
Epositions.append('0 '+str(probeXs[int(probeXInd)])+' '+str(probeYs[probeYInd])+' 0.0 0.0 0.0 0.0')
f.writelines(Epositions)
f.close()
shutil.copyfile(BaseDir+'/neuronal_model/'+file_name+'J_fixed.json', BaseDir+'/Simulation/components/biophysical_neuron_models/'+file_name+'J_fixed.json')
shutil.copyfile(BaseDir+'/neuronal_model/'+file_name+'_rotated.swc', BaseDir+'/Simulation/components/morphologies/'+file_name+'_rotated.swc')
shutil.copytree('./required_files/neuronal_model/modfiles',BaseDir+'/Simulation/components/mechanisms/modfiles')
shutil.copyfile('./required_files/neuronal_model/nrnmech.dll', BaseDir+'/Simulation/components/mechanisms/nrnmech.dll')

    
#Run simulation
print ("Simulation started at "+str(datetime.datetime.now()))
conf = bionet.Config.from_json(BaseDir+'/Simulation/config.json')
conf.build_env()
conf
net = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=net)

cell = sim.net.get_cell_gid(0)
ig = sim.h.InGauss(cell._secs[0](0.5))
ig.delay=Idel
ig.dur=Idur
ig.stdev=0.065
ig.mean=0.0
sim._iclamps.append(ig)

sim.run()
print ("Simulation done at "+str(datetime.datetime.now()))
#Create dataframes from h5 files 
neuron_data_output_file = BaseDir+'/Simulation/output/v_dend.h5' #Dendrite spike train file
soma_data_output_file = BaseDir+'/Simulation/output/v_report.h5' #Soma spike train file
param_file = BaseDir+'/neuronal_model/'+file_name+'J_fixed.json'

f = open(param_file, 'r')
lns = f.readlines()
f.close()
vrest = -70
for i in lns:
    if "v_init" in i:
        vrest = float(i.split(": ")[1].split("\n")[0])
        break

with h5py.File(soma_data_output_file, "r") as f: #Read soma spike train file
    report = f['report']
    single_neuron = report['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data2=single_neuron['data'][()]
f.close()
df = pd.DataFrame(np.array(data2))
segments_count = len(df.T)
df = df - vrest
gf = df.copy()
df[str(len(df.T))] = 0
df[str(len(df.T))] = 0

t=[]
for i in range(len(df)):
    t.append(i*Step)
    df.iloc[i,-2] = sim._sim_mods[0]._electrode.waveform.calculate(i*Step)
    if i*Step>Idel and i*Step<=Idel+Idur:
        df.iloc[i,-1] = Iamp
    else:
        df.iloc[i,-1] = 0.0

df.to_csv(BaseDir+'/Simulation/output/InData.csv',index=False)