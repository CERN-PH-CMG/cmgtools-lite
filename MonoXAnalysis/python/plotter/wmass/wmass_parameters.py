# range of index for W mass
# this parameters are used to name the datacards, and represents the steps for the nominal mass shift
# the mass variations are defined in $CMSSW_BASE/src/CMGTools/WMass/python/tools/eventVars_wmass.py

#mass_id_down = 0
#mass_id_up = 38
mass_id_down = 7
mass_id_up = 31
n_mass_id = 1 + int(mass_id_up) - int(mass_id_down)  # odd number, because there are the central value for nominal mass and its up and down variations
mass_id_central = int((int(mass_id_up) + int(mass_id_down))/2.)  # basically it is the mean value of the segment going from mass_id_down to mass_id_up 

#print n_mass_id
#print mass_id_central
