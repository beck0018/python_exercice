from fastapi import FastAPI, HTTPException
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
    #sinon on le créer
    with open(CACHE_FILE, "w") as file: 
        json.dump({}, file)             

#Routes si il manque le nom du pokemon
@app.get("/pokemon/")
def undefinded_pokemon() -> JSONResponse:
    raise HTTPException(status_code=500, detail="please join a pokemon name after /")

#Routes pour voir le poid d'un pokemon
@app.get("/pokemon/{pokemon_name}")
def get_pokemon(pokemon_name : str) -> JSONResponse:

    #on lit le fichier
    try:
        with open(CACHE_FILE, "r") as file :  
            data_file = json.load(file) 
    except Exception as e:
        raise HTTPException(status_code=400, detail="error read file")
                       
    #si le pokemon est dans le fichier
    if pokemon_name in data_file:
        #on prend le pokemon
        pokemon = data_file[pokemon_name]
        
        #on retourne le pokemon
        return {"type":"use file", "pokemon": pokemon_name, "poids_kg": pokemon["weight"]}
    #sinon on fait appel à l'api
    else :
        #on essaie l'api
        try :
            res = requests.get(f"{URL_API_POKEMON}{pokemon_name}")
            #si le pokemon n'existe pas
            if res.status_code == 404:
                raise HTTPException(status_code=404, detail="Pokemon not found")
            #on test les autre erreur
            res.raise_for_status()

            ##on récupere le pokemon
            pokemon = res.json()

            if not pokemon["weight"] :
                 raise HTTPException(status_code=502, detail="weight not found")

            data_file[pokemon_name] = {"weight": pokemon["weight"]}
            #on l'ajoute dans le fichier
            with open(CACHE_FILE, 'w') as file :
                json.dump(data_file, file)

            #on retourne le pokemon
            return {"type":"use api", "pokemon": pokemon_name, "poids_kg": pokemon["weight"]}
        #erreur autre de l'api
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=500, detail="error api pokemon") 



@app.post("/toto")
def other():
    print("post")


