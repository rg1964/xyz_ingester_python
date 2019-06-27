import shutil, random, os, argparse

# Individual files cannot be larger than 200MB.
# Defined below as FILE_MAX_SIZE 

# size of a kilobyte
KB = 1024
FILE_MAX_SIZE = 200


# Define the source directory where the XYZ files are located and the
# destination directory were the randomized selection of files will be copied to

SOURCE_DIR = 'GDB-9-molecules-all'
DEST_DIR = 'Randomized-xyz'


# Defining the function which parses the user supplied number of files "nr_files" 
# to be selected randomly from the unpacked directory of XYZ files

def random_files_selector(*args):
    """ Reads in the user supplied number of files, selects randomly the requested
    number of files from the SOURCE_DIR and copies them to the DEST_DIR
    """
    parser = argparse.ArgumentParser(description='select a number of random xyz files from "GDB-9-molecules-all" directory and copy to "Randomized-xyz"')
    parser.add_argument('-n', '--nrfiles', help='number of files to select randomly')
    args = parser.parse_args()
    
    # check if destination directory exists and if not creates it
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)    
    
    # remove all the existing files from the already existing directory
    for fileName in os.listdir(DEST_DIR):
        os.remove(DEST_DIR + "/" + fileName)

    # use the python random module function random.sample to return a "nr_files"
    # length list "filename" of unique elements chosen from the source directory
    nr_files = int(args.nrfiles)
    #filenames = random.sample(os.listdir(SOURCE_DIR), nr_files)
    # list all files in dir
    #files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(f)]
    #filenames = np.random.choice(files, nr_files)

    filenames = random.sample(os.listdir(SOURCE_DIR), 100)
    #for fname in filenames:
    #    srcpath = os.path.join(SOURCE_DIR, fname))
    #    shutil.copyfile(srcpath, DEST_DIR)
    
    # for each randomly selected file get the full path, get the file size
    # (in MB) and if it satisfies the size requirement of not exceeding 
    # FILE_MAX_SIZE, copy it to the destination directory
    for fname in filenames:
        source_path = os.path.join(SOURCE_DIR, fname)
        size_mb = (os.path.getsize(source_path)) / (KB**2)
        if size_mb <= FILE_MAX_SIZE:
            shutil.copy(source_path, DEST_DIR)


if __name__ == "__main__":
    random_files_selector()
    
