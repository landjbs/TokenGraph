import os
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

def delete_folder(folderPath):
    """ Deletes folderPath and contents """
    if os.path.exists(folderPath):
        for file in os.listdir(folderPath):
            os.remove(f'{folderPath}/{file}')
        os.rmdir(folderPath)
        return True
    else:
        return False


def delete_and_make_folder(folderPath):
    """ Deletes folder if already exists and makes folder """
    delete_folder(folderPath)
    os.mkdir(folderPath)


def safe_make_folder(folderPath):
    """ Wraps delete_and_make_folder but checks with the user first """
    if os.path.exists(folderPath):
        deleteAction = input(f"""{folderPath} already exists.
                                Are you sure you want to delete it? (y/n): """)
        if (deleteAction == 'y'):
            delete_and_make_folder(folderPath)
            return True
        elif (deleteAction == 'n'):
            raise SaverError('Folder deletion safely cancelled.')
        else:
            print("Must input either 'y' or 'n'.")
            safe_make_folder(folderPath)
    else:
        os.mkdir(folderPath)
