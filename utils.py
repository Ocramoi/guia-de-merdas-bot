import csv
import json

def readCSV(filename):
    ''' Read an CSV file and returns a list of ordered dicts based on its header '''
    try:
        file_obj = open(filename)
    except IOError:
        error_message = f"{filename} not found"
        print(error_message)
        exit()
    
    csvDictsList = list(csv.DictReader(file_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))
    return csvDictsList

def readJSON(filename):
    try:
        with open(filename, 'r') as file_obj:
            return json.load(file_obj)
    except:
        return None


def writeJSON(data, filename):
    with open(filename, 'w') as file_obj:
        json.dump(data, file_obj)

def appendJSON(filename, new_data):
    with open(filename) as file_obj:
        try: 
            old_data = json.load(file_obj)
            old_data.update(new_data)
        except: #In case there is a .json file but its empty
            old_data = new_data

    writeJSON(old_data, filename)
