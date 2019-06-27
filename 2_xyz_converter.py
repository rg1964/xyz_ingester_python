import argparse
from pypif import pif
from pypif.obj import *
import os

# directory where to deposit converted pif files
DEST_DIR = './GDB-9-molecules-pif/'    


def check(file): 
    """
    Check filetype to insure that it's an XYZ type file
    """      
    if not file.endswith('.xyz'):
        raise IOError('Filetype not compatible with parser. Please upload a .xyz file.\n')


def converter(*args):
    """
    Ingest .xyz files
    Args (one of these is required):
        listd: directory full path path and a comma separated list of filenames
            to process in that directory
        alld: directory full path path
        files: comma separated list of filenames with their full paths
    Returns: a pif chemical system (JSON-encoded text file) from each ingested .xyz file
    """
    parser = argparse.ArgumentParser(description='convert xyz file(s) to pif')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--listd', help='2 arguments: the source directory full path and a comma separated list of filenames to process in that directory', nargs = 2)
    group.add_argument('-a', '--alld', help='1 argument: the source directory full path path where all files of .xyz type reside', nargs = 1)
    group.add_argument('-f', '--files', help='1 argument: a comma separated list of filenames with their full paths to process', nargs = 1)
    
    args = parser.parse_args()
    
    # Several containers defined
    # stores the extracted data in pif
    my_pif = []
    
    # list of supplied filenames to be processed
    filename_list = []
    
    # same list with each file with its full path
    filename_fullpath_list = []
    
    # data source directory
    data_directory = []
       
    # check if destination directory existd and if not create one
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)    

    # clean destination directory
    for fileName in os.listdir(DEST_DIR):
        os.remove(DEST_DIR + "/" + fileName)

    # Depending on the command line input, process data and create a PIF file
    # 
    # Below is the case when the user specifies a directory and a list of files to be processed
    # from that directory
    if args.listd:
        data_directory = args.listd[0]
        filename_list = [str(item) for item in args.listd[1].split(',')]
        for i in range(len(filename_list)):
            if check(filename_list[i]):
                continue
            filename_fullpath_list = data_directory + '/' + filename_list[i]
            my_pif = parser_xyz(filename_fullpath_list)
            with open(DEST_DIR + filename_list[i].replace('.xyz', '.json'), 'w') as fw:
                pif.dump(my_pif, fw, indent = 4)

    # Belwo is the case when the user specifies a directory and all files
    # from that directory need to be processed
    elif args.alld:
        data_directory = str(args.alld[0])
        filename_list=os.listdir(data_directory)       
        for i in range(len(filename_list)):
            filename_fullpath_list = data_directory + '/' + filename_list[i]
            check(str(filename_fullpath_list))
            my_pif = parser_xyz(str(filename_fullpath_list))
            with open(DEST_DIR + filename_list[i].replace('.xyz', '.json'), 'w') as fw:
                pif.dump(my_pif, fw, indent = 4)

    # Below is the case when the users specifies a list of distinct files with their full path
    # that need to be processed
    elif args.files:
        filename_fullpath_list = [str(item) for item in args.files[0].split(',')]
        for i in range(len(filename_fullpath_list)):
            filename_list = filename_fullpath_list[i].split('/')[-1]
            check(str(filename_fullpath_list[i]))
            my_pif = parser_xyz(str(filename_fullpath_list[i]))
            with open(DEST_DIR + filename_list.replace('.xyz', '.json'), 'w') as fw:
                pif.dump(my_pif, fw, indent = 4)
    else:
        print("Nothing entered")
    


def sect4_properties(n_a, nr):
    """ Helper function to deal with the harmonic vibrational frequencies
    Their number depends on the number of atoms n_a, and whether the molecules
    are linear or non-linear 
    nr is the number of harmonic vibrational frequencies read from the XYZ file
    """
    # define possible expected numbers of frequencies
    a = 3 * n_a - 5
    b = 3 * n_a - 6
    
    # if a linear molecule
    if nr == a:
        return str(a) + ' harmonic vibrational frequencies ($3 \cdot n_{a}-5$)'

    # if a non-linear molecule
    elif nr == b:
        return str(b) + ' harmonic vibrational frequencies ($3 \cdot n_{a}-6$)'

    # for some of the molecules n_r is a multiplier of the linear or non-linear case
    elif nr % a == 0:
        sets = int(nr / a)
        return str(nr) + ' harmonic vibrational frequencies (nonlinear molecule of ' + str(sets) + ' $3 \cdot n_{a}-5$)'
    elif nr % b == 0:
        sets = int(nr / b)
        return str(nr) + ' harmonic vibrational frequencies (nonlinear molecule of ' + str(sets) + ' sets of $3 \cdot n_{a}-6$)'
    else:
        raise IOError('Calculation wrong!')

                    
def parser_xyz(filepath):
    """
    Loads a .xyz file and returns a ChemicalSystem() with properties extracted
    from .xyz file. Parsing is based on the information supplied in the 
    Ramakrishnan et al published in Scientific Data 1:140022 (online)

    Args:
        filepath: The input file (.xyz) with full path


    Returns:
        system: ChemicalSystem() with properties extracted from the .xyz file.
    """

    # open file and read lines
    f = open(filepath, 'r')
    line = f.readline()
    
    # how many lines need to scan thorugh and extract information and get out
    # of the reading loop when done
    total_lines = len(f.readlines())
    f.close()
    
    # define column headers for the different sections of the .xyz file format
    # the 1st line the number of atoms n_a
    sect1_properties = ['number of atoms $n_{a}$']
    
    # the 2nd line contains 17 calculated
    # below are definitions for all them in terms of properties, units, temperatures
    sect2_properties = ['gdb database indentifier', 'file id', 'Rotational constant A',
                    'Rotational constant B', 'Rotational constant C',
                    'Dipole moment $\\mu$', 'Isotropic polarizability $\\alpha$',
                    'Energy of HOMO $\\epsilon$HOMO', 'Energy of LUMO $\\epsilon$LUMO',
                    '$\\epsilon$Gap $\\epsilon$LUMO-$\\epsilon$HOMO', 
                    'Electronic spatial extent $< R^{2} >$',
                    'Zero point vibrational energy $zpve$', 'Internal energy $U_{0}$',
                    'Internal energy $U$', 'Enthalpy $H$',
                    'Free energy $G$', 'Heat capacity $C_{v}$'
                    ]
    sect2_units = ['', '','GHz', 'GHz', 'GHz', 'D', '$\\AA_{0}^{3}$', 'Ha', 'Ha', 
                   'Ha', '$\\AA_{0}^{2}$', 'Ha', 'Ha', 'Ha', 'Ha', 'Ha', 'cal / (mol K)'
                  ]
    sect2_temp = ['', '', '', '', '', '', '', '', '', '', '', '', '0 K',
                  '298.15 K', '298.15 K', '298.15 K', '298.15 K']
    
    # definitions for the element type, coordinate (x, y, z, in Å),
    # Mulliken partial charges (in e) on atoms, for each atom in the molecular structure
    # this section is defined as a subsystem and it will not show up on Citrination
    # when uploaded
    sect3_properties = ['Element type',	'coordinate x', 'coordinate y',	'coordinate z',
                    'Mulliken partial charges on atoms']
    sect3_units = ['', '$\\AA$', '$\\AA$', '$\\AA$', '$e$']
    
    
    # definitions for harmonic vibrational frequencies
    # sect4_header defined above as a function above to account for the 
    # dependency on n_a
    # this section is defined as a subsystem and it will not show up on Citrination
    # when uploaded
    sect4_units = ['$cm^{-1}$']
    
    # sect5 header defintions for SMILES strings from GDB-17 and from B3LYP relaxation
    sect5_properties = ['SMILES strings from GDB-17',
                    'SMILES strings from B3LYP relaxation']
    
    # sect5 header defintions for relaxation types
    sect5_relaxation_type = ['GDB-17', 'B3LYP']
    
    # sect6 header defintions for InChI strings for Corina and B3LYP geometries 
    sect6_properties = ['InChI strings for Corina geometries',
                    'InChI strings for B3LYP geometries']
    
    # sect6 header defintions for geometry type
    sect6_geometry_type = ['Corina', 'B3LYP']

    # read in the .xyz file, extract the data conforming to the pif format
    with open(filepath, 'r', encoding="ISO-8859-1") as fp:
        # define the main system as a ChemicalSystem() which contains all the info
        # define containers for different types of information to be extracted
        system = ChemicalSystem()
        system.chemicalFormula = []
        system.properties = []
        system.ids = []
        system.tags = ['quantum machine', 'QM9', 'GDB-9']
        chem_string = ''

        # define the sybsystem for element types, atomic coordinates and Mulliken charges
        sect3 = ChemicalSystem(names = ["Element type, coordinate (x, y, z, in $\\AA$), Mulliken partial charges (in $e$) on atoms"])
        sect3.properties = []

        # define the subsystem for harmonic vibrational frequencies
        sect4 = ChemicalSystem(names = ["Harmonic vibrational frequencies ($cm^{-1}$)"])
        sect4.properties = []

        # define the array of subsystems
        system.subsystem = [sect3, sect4]

        # iterate through each line of the .xyz file and extract specific information
        # and assign it appropriately into the ChemicalSystem()
        for i, line in enumerate(fp):
            if i == 0:
                # number_of_atoms
                n_a = line.strip()
                system.properties.append(Property(name = sect1_properties[0],
                        scalars = Scalar(value = n_a)))
            elif i == 1:
                # scalar properties
                x_y_z = line.split()
                for j in range(1):
                    system.properties.append(Property(name = sect2_properties[j],
                        scalars = [Scalar(value = x_y_z[j])], units = sect2_units[j]))
                for j in range(1,2):
                    system.ids.append(Property(name = sect2_properties[j],
                    value = x_y_z[j])) 
                for j in range(2,17):
                    system.properties.append(Id(name = sect2_properties[j],
                        scalars = [Scalar(value = x_y_z[j])], units = sect2_units[j], dataType = 'COMPUTATIONAL', Temperature = sect2_temp[j]))          
            elif((2 <= i) and (i <= (int(n_a) + 1))):
                # element type, atomic Cartesian coordinates (x, y, z),
                # Mulliken partial charges
                x_y_z = line.split()
                for j in range(5):
                    sect3.properties.append(Property(name = sect3_properties[j],
                        scalars = [Scalar(value = x_y_z[j])], units = sect3_units[j], dataType = 'COMPUTATIONAL'))
            elif(i == (int(n_a) + 2)):
                # harmonic vibrational frequencies
                x_y_z = line.split()
                nr = int(len(x_y_z))
                val_comp = x_y_z[0]
                for j in range(1, nr):
                    val_comp = val_comp + ',' + x_y_z[j]
                sect4.properties.append(Property(name = sect4_properties(int(n_a), nr),
                    scalars = Scalar(value = val_comp), units = sect4_units[0]))
            elif(i == (int(n_a) + 3)):
                # SMILES strings from GDB-17 and B3LYP relaxation 
                x_y_z = line.split()
                for j in range(2):
                    system.properties.append(Property(name = sect5_properties[j],
                        scalars = [str(x_y_z[j])], relaxationType = sect5_relaxation_type[j]))
            elif(i == (int(n_a) + 4)):
                # InChI strings for Corina and B3LYP geometries
                x_y_z = line.split()
                # get chemical_formula and append it to system.chemical_formula
                chem_string = str(x_y_z[0].split("/")[1])
                system.chemicalFormula = chem_string
                for j in range(2):
                    x_y_z[j] = str(x_y_z[j]).strip('InChl=')
                    system.properties.append(Property(name = sect6_properties[j],
                        scalars = [x_y_z[j]], geometryType = sect6_geometry_type[j]))
            elif i > total_lines:
                fp.close()
    return system


if __name__ == "__main__":
    converter()
