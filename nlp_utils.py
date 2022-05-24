
import json
import logging
import re
import unidecode
import configparser




def read_json_file(json_file_path):
    """
    Reads a json_file and returns it as a python dict
    
    :param string json_file_path: path to a json file with configuration information
    :returns: dict
    """
    try:
        with open(json_file_path) as json_data_files:
            return json.load(json_data_files)
    except Exception as e:
        logging.debug("Error in read_json_file(): %s" % str(e))
        raise Exception("Error in read_json_file(): %s " %str(e))

def read_parameters(file_path):
    """
    Lee un archivo de texto de configuración
    
    :param string file_path: ruta al archivo de texto de configuración
    :returns: dict: dict of a parser object
    """

    parameter_file=check_file(file_path)
    parser=configparser.ConfigParser()
    parser.read(parameter_file)
    return parser._sections



def check_file(file_path):
    '''
    Check if the file exists
    
    :param string file_path: path to file to check
    :return: file_path
    :raises Exception e: General exception if file doesn't exist. 
    '''
    try:
        with open(file_path):
            return file_path

    except Exception as e:
        logging.error("Error in check_file(%s). Error: %s " %(file_path,str(e)))
        raise Exception("Error in check_file(%s). Error: %s " %(file_path,str(e)))
    

def preprocessor(text):
    text=re.sub('<[^>]*>','',text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text)
    text = re.sub('[\W]+',' ', text.lower()) + ''.join(emoticons).replace('-','')
    #Convert characters with spanish acute accent, tilde (virguilla)
    text=unidecode.unidecode(text)
    return text

