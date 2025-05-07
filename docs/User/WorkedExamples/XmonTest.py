import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
os.environ["PMIX_MCA_gds"]="hash"

# Import useful packages
import qiskit_metal as metal
from qiskit_metal import designs, draw
from qiskit_metal import MetalGUI, Dict, open_docs
from qiskit_metal.toolbox_metal import math_and_overrides
from qiskit_metal.qlibrary.core import QComponent
from collections import OrderedDict

# To create plots after geting solution data.
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Packages for the simple design
from SQDMetal.Comps.Xmon import Xmon
from SQDMetal.Comps.Junctions import JunctionDolanPinStretch

# Packages for the simulation
from SQDMetal.PALACE.Eigenmode_Simulation import PALACE_Eigenmode_Simulation
from SQDMetal.Utilities.Materials import MaterialInterface

matplotlib.use('Agg')

# Set up chip design as planar, multiplanar also available
design = designs.DesignPlanar({}, overwrite_enabled=True)

# Set up chip dimensions 
design.chips.main.size.size_x = '500um'
design.chips.main.size.size_y = '500um'
design.chips.main.size.size_z = '500um'
design.chips.main.size.center_x = '0mm'
design.chips.main.size.center_y = '0mm'

leXmon = Xmon(design, 'leXmon', options=Dict(pos_x=0, pos_y=0,
                                    vBar_width='24um', hBar_width='24um', vBar_gap=f'{16}um', hBar_gap=f'{16}um',
                                    cross_width=f'{60*2+24}um', cross_height=f'{60*2+24}um',
                                    gap_up='24um', gap_left='24um', gap_right='24um', gap_down='24um'))

JunctionDolanPinStretch(design, 'junction', options=Dict(pin_inputs=Dict(start_pin=Dict(component=f'leXmon',pin='right')),
                                                         dist_extend='24um',
                                                         layer=2,
                                                         finger_width='0.4um', t_pad_size='0.385um',
                                                         squid_width='5.4um', prong_width='0.9um'));


# rebuild the GUI
# gui = MetalGUI(design)
# gui.rebuild()


design.rebuild()

#Eigenmode Simulation Options
user_defined_options = {
                "mesh_refinement":  0,                             #refines mesh in PALACE - essetially divides every mesh element in half
                "dielectric_material": "silicon",                  #choose dielectric material - 'silicon' or 'sapphire'
                "starting_freq": 5e9,                              #starting frequency in Hz 
                "number_of_freqs": 2,                              #number of eigenmodes to find
                "solns_to_save": 3,                                #number of electromagnetic field visualizations to save
                "solver_order": 2,                                 #increasing solver order increases accuracy of simulation, but significantly increases sim time
                "solver_tol": 1.0e-8,                              #error residual tolerance foriterative solver
                "solver_maxits": 100,                              #number of solver iterations
                "mesh_sampling": 130,                              #number of points to mesh along a geometry
                "fillet_resolution":12,                             #Number of vertices per quarter turn on a filleted path
                "palace_dir":"apptainer run ~/Documents/SQDMetal/palace.sif",#"PATH/TO/PALACE/BINARY",
                "num_cpus": 20
                }

#Creat the Palace Eigenmode simulation
eigen_sim = PALACE_Eigenmode_Simulation(name ='XmonTest',                              #name of simulation
                                        metal_design = design,                                      #feed in qiskit metal design
                                        sim_parent_directory = "",            #choose directory where mesh file, config file and HPC batch file will be saved
                                        mode = 'simPC',                                               #choose simulation mode 'HPC' or 'simPC'                                          
                                        meshing = 'GMSH',                                         #choose meshing 'GMSH' or 'COMSOL'
                                        user_options = user_defined_options,                        #provide options chosen above
                                        view_design_gmsh_gui = False,                               #view design in GMSH gui 
                                        create_files = True)                                        #create mesh, config and HPC batch files
eigen_sim.add_metallic(1)
eigen_sim.add_ground_plane()

#Add in the RF ports
eigen_sim.create_port_JosephsonJunction('junction', L_J=4.3e-9, C_J=10e-15)

# #Fine-mesh routed paths
eigen_sim.fine_mesh_around_comp_boundaries(['leXmon'], min_size=14e-6, max_size=75e-6)

eigen_sim.setup_EPR_interfaces(metal_air=MaterialInterface('Aluminium-Vacuum'), substrate_air=MaterialInterface('Silicon-Vacuum'), substrate_metal=MaterialInterface('Silicon-Aluminium'))

eigen_sim.prepare_simulation()

eigen_sim.run()

# pvdtu = eigen_sim.retrieve_field_plots()
# first_eigenmode_field = pvdtu.get_data_slice(0)
# second_eigenmode_field = pvdtu.get_data_slice(1)
# fig, (left_ax, right_ax) = plt.subplots(1, 2, figsize=(12, 6))
# fig.suptitle('Eigenmode Simulation Results', fontsize=16)
# first_eigenmode_field.plot(np.linalg.norm(first_eigenmode_field.get_data('E_real'), axis=1), 'coolwarm', True, fig=fig, ax=left_ax);
# second_eigenmode_field.plot(np.linalg.norm(second_eigenmode_field.get_data('E_real'), axis=1), 'coolwarm', True, fig=fig, ax=right_ax);
# left_ax.set(aspect='equal')
# right_ax.set(aspect='equal')

# fig.savefig('Xmon_Eigenmode_Simulation_Results.png')