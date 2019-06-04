from citrination_client import *
import random
import string

SOURCE_DIR = 'GDB-9-molecules-pif'    


def citrination_uploader():
    """ Using the Python Citrination DataClient to manage data on Citrination.
    Specifically it takes all the files in the DEST_DIR directory and uploads them
    on Citrination. Prints the number of files successfully uploaded.
    """
    client = CitrinationClient('raXn0wbVCf27MOiwx9unQgtt', 'https://citrination.com')
#    client = CitrinationClient(environ['CITRINATION_API_KEY'], 'https://citrination.com')
    data_client = client.data
    
    # generate a random 5 digit string to distinctly define the name of the dataset 
    random_string = ''.join([random.choice(string.ascii_uppercase + string.digits) for i in range(5)])
    data_name = 'GDB-9' + ' ' + random_string
    data_desc = 'Converted XYZ format files containing computed geometric, energetic, electronic, and thermodynamic properties from the GDB-9 database of 134k stable small organic molecules made up of carbon, hydrogen, nitrogen, oxygen, and fluorine'
    dataset = data_client.create_dataset(name=data_name, description=data_desc)
    dataset_id = dataset.id    
    # Upload the converted files directory
    upload_result = data_client.upload(dataset_id=dataset_id, source_path=SOURCE_DIR)
    # number of successfully uploaded files
    print('Number of successful uploads: {}'.format(len(upload_result.successes)))
    
    

if __name__ == "__main__":
    citrination_uploader()

