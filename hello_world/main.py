from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
import json
import os

#appel de l'api
app = FastAPI()

#Constantes
URL_API_POKEMON = "https://pokeapi.co/api/v2/pokemon/"
CACHE_FILE = "pokemon_list.json"


# S'assurer que le fichier de cache existe
if not os.path.exists(CACHE_FILE):
    file = open(CACHE_FILE, "w")   
    json.dump({}, file)             
    file.close()                     

#Routes pour voir le poid d'un pokemon
@app.get("/pokemon/{pokemon_name}")
def get_pokemon(pokemon_name : str) -> JSONResponse:
    try:
        file = open(CACHE_FILE, "r")  
        data_file = json.load(file) 
        file.close()  
    except Exception as e:
        print("error read file", e)
                       

    if pokemon_name in data_file:
        pokemon = data_file[pokemon_name]
        return {"pokemon": pokemon_name, "poids_kg": pokemon["weight"]}
    else :
        try :
            res = requests.get(f"{URL_API_POKEMON}{pokemon_name}")
            if res.status_code == 404:
                raise HTTPException(status_code=404, detail="Pokemon not found")
            res.raise_for_status()
            pokemon = res.json()
            data_file[pokemon_name] = {"weight": pokemon["weight"]}
            file = open(CACHE_FILE, "w")  
            json.dump(data_file, f)
            file.close()  

            return {"pokemon": pokemon_name, "poids_kg": pokemon["weight"]}
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=500, detail="error api pokemon") 



@app.post("/toto")
def other():
    print("post")


