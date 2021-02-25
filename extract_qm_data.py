#!/usr/bin/env python3

import optparse
import cclib

def prop_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="file", help="log file from QM calculation")
    parser.add_option("-m", "--method", type="string", dest="method", help="QM method used in the calculation (HF, DFT, MP2, CC)")
    parser.add_option("-p", "--properties", dest="properties", type="string", action="callback", callback=prop_callback, help="Properties to be extracted separated by commas (coords,energy)")
    parser.add_option("-g", "--geomopt", dest="geomopt", action="store_true", help="Sets bool to True if used")

    (options, arguments) = parser.parse_args()

    if not options.file:
        parser.error(" [-] Please specify an input file")
    elif not options.method:
        parser.error(" [-] Please specify the used QM method: --method ")
    elif options.method != "HF" and options.method != "DFT" and options.method != "MP2" and options.method != "CC":
        parser.error(" [-] Please use one of the folowing key words: HF, DFT, MP2, CC")
    elif not options.properties:
        parser.error(" [-] Please specify at least one property to extract")

    return options

def get_energy(data, method, gopt):
    if method == "HF" or method == "DFT":
        energy = data.scfenergies
    elif method == "MP2":
        energy = data.mpenergies
    elif method == "CC":
        energy = data.ccenergies

    if gopt: energy = energy[-1]

    return energy

def get_coords(data, f_out, gopt, energy):
    NAMES = {1:"H", 6:"C", 8:"O"}

    coords   = data.atomcoords
    labels   = data.atomnos
    numAtoms = data.natom

    if gopt: coords = coords[-1]

    f = open(f_out, 'w')

    f.write("{}\n{} eV\n".format(numAtoms, energy))

    for i in range(numAtoms):
        f.write("{} {} {} {}\n".format( NAMES[labels[i]], coords[i][0], coords[i][1], coords[i][2]))
    f.close()

if __name__ == '__main__':

    options = get_arguments()

    filename = options.file
    data = cclib.io.ccread(filename)

    if "energy" in options.properties:
        energy = get_energy(data, options.method, options.geomopt)
        #print(" {} energy is: {} eV".format(options.method, energy))
    elif "energy" not in options.properties:
        energy = "0"

    if "coords" in options.properties:
        f_out = (options.file).split('.')[0] + ".xyz"
        get_coords(data, f_out, options.geomopt, energy)
        print(" [+] wrote xyz file: {}".format(f_out))
