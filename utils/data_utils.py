import urllib
import pickle
import json 
import pathlib
import os

#----------------------------------------------------------------------------------------------
class paths_():
    def __init__(self) -> None:
        self.project = pathlib.Path(__file__).parents[1].resolve()
        self.result = os.path.join(self.project, "results") 
    
    def get_json(self, path):
        path_ = self.get_folder(path)
        with open(path_, "rb") as file:
            file = json.load(file)
        return file
    
    def set_pickle(self, path, file):
        path = self.get_folder(path)
        with open(path, "wb") as archivo:
            pickle.dump(file, archivo)
            
    def get_pickle(self, path):
        path = self.get_folder(path)
        with open(path, "rb") as archivo:
            file = pickle.load(archivo)
        return file
    
    def get_folder(self, folder):
        return os.path.join(self.project, folder)
#----------------------------------------------------------------------------------------------