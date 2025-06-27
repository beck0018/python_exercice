from fastapi import  HTTPException
from fastapi.responses import JSONResponse
import os
import json

#open file
def open_file(file_name: str) -> dict[str, any]:
    with open(file_name, "r") as file :  
        data_file = json.load(file) 
    return data_file
   
#create file
def create_file(file_name : str) -> None:
    if not os.path.exists(file_name):
        #sinon on le créer
        with open(file_name, "w") as file: 
            json.dump({}, file)    

#write file
def write_file(file_name: str, data_file_add : dict[str, any] ) -> None:
    with open(file_name, 'w') as file :
        json.dump(data_file_add, file)  
    

#add pokemon on the file
def update_cache(pokemon_name : str, weight : int, file_name : str, data_file : dict[str, any]) -> None: 
    data_file[pokemon_name] = {"weight": weight}
    #on l'ajoute dans le fichier
    write_file(file_name, data_file)