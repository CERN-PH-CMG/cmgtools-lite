# range of index for W mass
# this parameters are used to name the datacards, and represents the steps for the nominal mass shift
# the mass variations are defined in $CMSSW_BASE/src/CMGTools/WMass/python/tools/eventVars_wmass.py

luminosity = 35.9

wmass_steps_MeV = [x for x in range(0,24,2)] + [x for x in range(24,54,10)] + [x for x in range(54,141,20)]
n_wmass_steps_MeV = 1 + 2 * (len(wmass_steps_MeV) - 1)  # count + and - variations: subtract the central value, double the number and add the central again
#print n_wmass_steps_MeV
#mass_id_down = 0
#mass_id_up = 38
mass_id_down = 7
mass_id_up = 31
n_mass_id = 1 + int(mass_id_up) - int(mass_id_down)  # odd number, because there are the central value for nominal mass and its up and down variations
mass_id_central = int((int(mass_id_up) + int(mass_id_down))/2.)  # basically it is the mean value of the segment going from mass_id_down to mass_id_up 

if (n_wmass_steps_MeV < n_mass_id):
    print "Error in wmass_parameters.py: using more ids than the mass steps. Please check!"
    quit()
#print n_mass_id
#print mass_id_central
