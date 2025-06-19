from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import JSONResponse
import json
from fonction_file import *
from pydantic import BaseModel

#appel de l'api
app = FastAPI()

#Constantes
URL_API_POKEMON = "https://pokeapi.co/api/v2/pokemon/"
CACHE_FILE = "pokemon_list.json"

class Pokemon(BaseModel):
    name: str
    weight : int


# S'assurer que le fichier de cache existe
create_file(CACHE_FILE)
                                

#Routes pour voir le poid d'un pokemon
@app.get("/pokemon/{pokemon_name}", response_model=Pokemon)
def get_pokemon(pokemon_name : str):

    #on lit le fichier
    data_file = open_file(CACHE_FILE)
                       
    #si le pokemon est dans le fichier
    if pokemon_name in data_file:
        #on prend le pokemon
        pokemon = data_file[pokemon_name]
        #on retourne le pokemon
        return Pokemon(name = pokemon_name, weight = pokemon["weight"])

    #sinon on fait appel à l'api
    #on essaie l'api
    try :
        res = requests.get(f"{URL_API_POKEMON}{pokemon_name}")
        #on test les autre erreur
        res.raise_for_status()

        #on récupere le pokemon
        pokemon = res.json()
        if not pokemon["weight"] :
            raise HTTPException(status_code=404, detail="weight not found")

        #mise a jour du cache
        update_cache(pokemon_name, pokemon["weight"], CACHE_FILE, data_file)

        #on retourne le pokemon
        return Pokemon(name = pokemon_name, weight = pokemon["weight"])
    #erreur autre de l'api
    except HTTPError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        raise HTTPException(status_code=500, detail="error api pokemon") 



@app.post("/toto")
def other():
    print("post")


