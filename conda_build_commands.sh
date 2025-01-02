function the_exit() { echo ; exit; }
conda create -n ROOT root=6.30.4 || the_exit "failed to create environment ROOT"
conda activate ROOT || the_exit "unable to activate environment ROOT"
conda install uproot mplhep uncertainties
