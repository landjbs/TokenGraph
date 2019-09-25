import pickle

def save_attribute(obj, name):
    """ Helper saves attribute to file under path """
    with open(f'{path}/{name}.sav', 'wb+') as attributeFile:
        pickle.dump(obj, attributeFile)
    return True
