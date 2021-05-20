import configparser
import os


def get_config(config_path):
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str        
    #config_path = os.path.join(os.path.abspath(os.path.dirname(__file__))) + '/config.ini'    
    config.read(config_path)
    return config
