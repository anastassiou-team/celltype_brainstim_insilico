from bmtk.builder.networks import NetworkBuilder

net = NetworkBuilder('single_neuron')
net.add_nodes(cell_name='Cell_471077857',
              potental='exc',
              model_type='biophysical',
              model_template='ctdb:Biophys1.hoc',
              model_processing='aibs_perisomatic',
              dynamics_params='hof_param_471077857_0.json',
              morphology='Cell_rotated.swc')

net.build()
net.save_nodes(output_dir='ModelH')

from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(
    base_dir='SimulationH',
    config_file='config.json',
    network_dir='ModelH',
    tstop=4000.0, dt=0.1,
    report_vars=['v', 'cai'],
    current_clamp={
        'amp': 0.510,
        'delay': 1000.0,
        'duration': 1000.0
    },
    include_examples=False,
    compile_mechanisms=False
)

import shutil
import os
from subprocess import call

#Copy component files
shutil.copyfile('./Required_files/hof_param_471077857_0.json', './SimulationH/components/biophysical_neuron_models/hof_param_471077857_0.json')
shutil.copyfile('./Required_files/Cell_rotated.swc', './SimulationH/components/morphologies/Cell_rotated.swc')
shutil.copytree('./Required_files/modfiles','./SimulationH/components/mechanisms/modfiles')

#Compile mechanisms
status=call("nrnivmodl modfiles",cwd=os.getcwd()+"/SimulationH/components/mechanisms",shell=True)
if status:
    print ("NEURON ERROR")
else:
    print ("Compilation done!")
    
from bmtk.simulator import bionet

conf = bionet.Config.from_json('SimulationH/config.json')
conf.build_env()
conf
net = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=net)
sim.run()
