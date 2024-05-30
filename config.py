import json
import os

class Config:
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
        config_data = json.load(config_file)
    
    HOST = config_data.get("host", "127.0.0.1")
    PORT = config_data.get("port", 5000)
    DEBUG = config_data.get("debug", True)
    SECRET_KEY = config_data.get("SECRET_KEY", "S^JJ0P&A@xcC*MOupUJ1bd)4aOWdV3iDiHHW@O1romSloFIzuky!nFjck)aj)ONJ")
