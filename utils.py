import pickle

def save_obj(obj, name):
    """ Pickles objectt to file under name """
    with open(f'{name}.sav', 'wb+') as attributeFile:
        pickle.dump(obj, attributeFile)
    return True

def load_obj(name):
    """ Loads object from file under name """
    with open(f'{name}.sav', 'rb') as loadFile:
        obj = pickle.load(loadFile)
    return obj
