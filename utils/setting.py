import configparser
import os 


info = """
    [WEBSITE]
    Port = portnumber

    [GMAIL]
    Username = your.mail@gmail.com
    Password = passwd
    Sender = sender.mail@gmail.com
    Receivers = receivers.mail@mail.com

    [ADMIN]
    Username = user
    Password = passwd 
"""

_gmail = {} 
_admin = {} 
_port = 80 


def initialization():
    global _port 
    """Read the configuration file and set the dictionnary variables
    """
    config = configparser.ConfigParser()
    if not os.path.isfile('.config'): 
        raise FileNotFoundError("File '.config' must exist. The configuration format:\n"+ info)
    else: 
        config.read('.config')

    # gmail account
    if 'GMAIL' not in config.keys():
        raise KeyError("'GAMIL' must be configured")
    else: 
        try: 
            _gmail["user"] = config['GMAIL']['Username'] 
            _gmail["passwd"] = config['GMAIL']['Password'] 
            _gmail["sender"] = config['GMAIL']['Sender'] 
            _gmail["receivers"] = config['GMAIL']['Receivers'] 
        except KeyError as e: 
            print("Key " + str(e) + " must be configured") 

    # 
    if 'ADMIN' not in config.keys(): 
        raise KeyError("'ADMIN' must be configured")
    else:
        try: 
            _admin["user"] = config['ADMIN']['Username'] 
            _admin["passwd"] = config['ADMIN']['Password'] 
        except KeyError as e: 
            print("Key " + str(e) + " must be configured") 
        
    # host port 
    if 'WEBSITE' not in config.keys():
        _port = 80
        print("Default port is 80")
    else: 
        try:     
            _port = int(config['WEBSITE']['Port'])
        except: 
            #print("Port must be a integral type, range: 1 - 20000")
            _port = 80 

        print("Port Number is {}".format(_port))

def getGamilConfig():
    return _gmail 

def getAdminConfig():
    return _admin 

def getPortNum():
    return _port 


