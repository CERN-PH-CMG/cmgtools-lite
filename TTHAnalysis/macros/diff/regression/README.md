# Code 2019 and 2020 by Pietro Vischia

# Instructions

# Given the friend trees produced using the module higgsDiffRegressionTTH.py, you need to:

a) Run tocsv.py to convert the friend trees to csv format

b) Run tth_regressor.ipynb from a python3 notebook (e.g. with ```ipython3 notebook``` or ```jupyter3 notebook```)

c) Have fun





#  To run the notebook on ingrid:

- in ingrid, run the notebook server on a 88XX port (each user must select a different port, this will lock the port):
```jupyter notebook --no-browser --port=8889```

- in your laptop, run a ssh redirection, where ```ucl``` is the name you gave to the ingrid tunnel in your ssh config, 8889 is the remote port (so if you change it in the previous command, you have to change it here too), and 8888 is the local port:

```ssh -N -f -L localhost:8888:localhost:8889 ucl```

- You can then direct you laptop's browser to http://localhost:8888/tree  (if you change the local port in the previous command, you need to change it also here)