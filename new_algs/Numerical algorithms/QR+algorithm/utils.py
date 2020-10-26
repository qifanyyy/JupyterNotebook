# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 19:48:19 2020

@author: AdilDSW
"""

# Standard Built-in Libraries
import os
import json

status_code = {
    'S0': "Operation completed successfully.",
    'S1': "No results found.",
    'S2': "Operation completed with some errors.",
    'S3': "Constraints OK.",
    'S4': "Attendance already registered.",
    'S5': "Device already registered in the server.",
    'E0': "Invalid data input.",
    'E1': "Required field blank.",
    'E2': "Duplicate data present.",
    'E3': "Illegal service call.",
    'E4': "Incorrect username/password",
    'E5': "Passwords don't match.",
    'E6': "Foreign key missing.",
    'E7': "Organization already registered.",
    'E8': "Insufficient privileges.",
    'E9': "Unexpected error.",
    'E10': "Student is not registered for this class.",
    'E11': "Student already linked to another device.",
    'E12': "Student is attending another session.",
    'E13': "The scanned QR Code has expired.",
    'E14': "Invalid QR Code.",
    'E15': "Data linked as foreign key, cannot be deleted."
    }

def write_config(ip, port, user, pwd, authdb):
    """Writes database configuration into a JSON file."""
    
    db_config = {'ip': ip, 
                 'port': port, 
                 'user': user, 
                 'pwd': pwd, 
                 'authdb': authdb}
    
    with open("config.json", 'w') as config_file:
            json.dump(db_config, config_file)
            
            
def read_config():
    """Reads and returns database configuration as a JSON string."""
    
    if os.path.exists("config.json"):
        with open("config.json") as config_file:
            return json.load(config_file)
    else:
        return None


def delete_config():
    """Deletes database configuration JSON file."""
    
    if os.path.exists("config.json"):
        os.remove("config.json")
