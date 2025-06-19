from fastapi import  HTTPException
from fastapi.responses import JSONResponse
import os
import json

#ouverture d'un fichier
def open_file(name_file: str) -> dict:
    try:
        with open(name_file, "r") as file :  
            data_file = json.load(file) 
        return data_file
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier introuvable.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="error read file")
    
#création d'un fichier
def create_file(name_file : str):
    try:
        if not os.path.exists(name_file):
            #sinon on le créer
            with open(name_file, "w") as file: 
                json.dump({}, file)    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error create file: {str(e)}")

#ecriture dans le fichier
def write_file(name_file: str, data_file_add : dict ):
    try:
        with open(name_file, 'w') as file :
            json.dump(data_file_add, file)  
    except Exception as e:
        raise HTTPException(status_code=500, detail="error wrire file")
        

#ajout du pokemon dans le fichier
def update_cache(pokemon_name : str, weight : int, name_file : str, data_file : dict):
    data_file[pokemon_name] = {"weight": weight}
    #on l'ajoute dans le fichier
    write_file(name_file, data_file)