BaseDir = "R:/Temp/Threads4/Thread0"
MeanCurr = 0.150
StdCurr = 0.150

file_name = 'Cell'
durations = [9900] #ms
stopTime = [10000] #ms
rangesL = [10000] #phase calculation crop limit low
rangesH = [-10000] #phase calculation crop limit high
resultsdir = BaseDir+'/Results/Results.txt'

#Simulation
Step = 0.1 #ms

#Intra
signalInd = 0
Iamp = MeanCurr #nA
Idel = 100 #ms
Idur = durations[signalInd] #ms

from bmtk.builder.networks import NetworkBuilder
from bmtk.utils.sim_setup import build_env_bionet
from bmtk.simulator import bionet
import shutil, datetime, h5py
import pandas as pd
import numpy as np
import efel
from scipy.stats import norm

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

print ("Simulation set.")

shutil.copyfile(BaseDir+'/neuronal_model/'+file_name+'J_fixed.json', BaseDir+'/Simulation/components/biophysical_neuron_models/'+file_name+'J_fixed.json')
shutil.copyfile(BaseDir+'/neuronal_model/'+file_name+'_rotated.swc', BaseDir+'/Simulation/components/morphologies/'+file_name+'_rotated.swc')
shutil.copyfile(BaseDir+'/neuronal_model/nrnmech.dll', BaseDir+'/Simulation/components/mechanisms/nrnmech.dll')

    
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
ig.stdev=StdCurr
ig.mean=0.0
sim._iclamps.append(ig)

sim.run()
print ("Simulation done at "+str(datetime.datetime.now()))

#Create dataframes from h5 files 
soma_data_output_file = BaseDir+'/Simulation/output/v_report.h5' #Soma spike train file

with h5py.File(soma_data_output_file, "r") as f: #Read soma spike train file
    report = f['report']
    single_neuron = report['single_neuron'] #Depends on network name (NetworkBuilder BMTK)
    data2=single_neuron['data'][()]
f.close()
co = pd.DataFrame(np.array(data2))

thrs = co.iloc[rangesL[signalInd]:rangesH[signalInd]]
thrs = (thrs.max()-thrs.min())/2+thrs.min()
print("Threshold: "+str(thrs))
efel.setThreshold(thrs)
trace1 = {}
trace1['T'] = co.index*Step
trace1['V'] = co.iloc[:,0]
trace1['stim_start'] = [rangesL[signalInd]/10]
trace1['stim_end'] = [(len(co)-rangesH[signalInd])/10]
traces = [trace1]
Peak_indices = efel.getFeatureValues(traces, ['peak_indices'])[0]['peak_indices']

start = len(Peak_indices)
stop = 0
for j in range(len(Peak_indices)):
    if Peak_indices[j]<rangesL[signalInd]:
        start = j
    if Peak_indices[j]<=(len(co)-rangesH[signalInd]):
        stop = j
Peak_indices = Peak_indices[start+1:stop]

ISIs = Peak_indices[1:]-Peak_indices[:-1]

ISIs = 10000 / ISIs

mean,std=norm.fit(ISIs)
pd.DataFrame([mean,std]).to_csv(BaseDir+'/Simulation/output/Data.csv',index=False)