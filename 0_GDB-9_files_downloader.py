import os
import requests
import tarfile

# url site from where to download the GDB-9 datafiles
URL = 'https://ndownloader.figshare.com/files/3195389/'

# specific filename to download
FILE = 'dsgdb9nsd.xyz.tar.bz2'

# local directory where to copy the files
DEST_DIR = 'GDB-9-molecules-all'


def download_archive(url, target_file):
    """ check the HTTP code as a response to the request to "url"
    If it's 200, the server successfully answered the http request
    then open the supplied "target_file" in write and binary mode
    and get the raw socket response from the server which is the preferred 
    and recommended way to retrieve the contents when streaming a download
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_file, 'wb') as f:
            f.write(response.raw.read())
    else:
        print("Could not connect")
        

def xyz_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".xyz":
            yield tarinfo


def create_target_directory(name):
    """ first check if the desired directory already exists, and if not,
    create the destination directory where all extracted files from the
    downloaded archive will be deposited to. Alert if process fails, or 
    inform of successfully creating the destination directory
    """
    if not os.path.exists(name):
        try:  
            os.makedirs(name)    
        except OSError:  
            print ("Creation of the directory %s failed" % name)
        else:  
            print ("Successfully created the directory %s " % name)
    
    # if directory already exists, remove all files before it will be reused
    for fileName in os.listdir(name):
        os.remove(name + "/" + fileName)

    

def remove_archive_file(name):
    """ delete the dowloaded archive file from the filesystem
    """
    try:
        os.remove(name)
    except OSError:
        print ("Removal of original archive file %s failed" % name)
    else:
        print ("Successfully removed original archive file %s" % name)


def main():
    # download FILE archive from URL
    download_archive(URL, FILE)
    # open the tarfile FILE in default read mode
    tar = tarfile.open(FILE)
    # create the destination directory where all archoved files will be extracted to
    create_target_directory(DEST_DIR)
    # extract all members from the archive to the pre-defined directory path
    tar.extractall(members=xyz_files(tar), path = '.\\' + DEST_DIR)
    # close the tarfile
    tar.close()
    # remove the downloaded FILE from URL for cleanup and memory preservation
    remove_archive_file(FILE)

            
if __name__ == "__main__":
    main()

