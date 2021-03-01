# QM_data_exctraction
Wrapper for the cclib python library
</br>
### Usage:
```
python3 extract_qm_data.py --file <filename> --method DFT --properties energy,forces --geomopt
```
The output will be written as an xyz file (same name as the log file) and all the properties will be written to the second line of the xyz file
### TODO:
Add more properties:
- forces
- enthalpy
- polarizabilities
- vibrational frequencies
- orbital energies
- ...
