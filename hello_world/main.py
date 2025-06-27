from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import JSONResponse
import json
from file import *
from schema import Pokemon

#call the api
app = FastAPI()

#Constants
URL_API_POKEMON = "https://pokeapi.co/api/v2/pokemon/"
CACHE_FILE = "pokemon_list.json"



#initialize the cache
create_file(CACHE_FILE)
                                

#route to get pokemon's weight
@app.get("/pokemon/{pokemon_name}", response_model=Pokemon)
def get_pokemon(pokemon_name : str):

    #read cache file
    data_file = open_file(CACHE_FILE)
                       
    #if pokemon on the file
    if pokemon_name in data_file:
        #take pokemon
        pokemon = data_file[pokemon_name]
        #return the pokemon
        return Pokemon(name = pokemon_name, weight = pokemon["weight"])

    #else fetch from pokemon api
    #try api
    try :
        res = requests.get(f"{URL_API_POKEMON}{pokemon_name}")
        #try errors
        res.raise_for_status()

        #grab the pokemon information
        pokemon = res.json()
        if not pokemon["weight"] :
            raise HTTPException(status_code=404, detail="weight not found")

        #update the local cache
        update_cache(pokemon_name, pokemon["weight"], CACHE_FILE, data_file)

        #return the pokemon information
        return Pokemon(name = pokemon_name, weight = pokemon["weight"])
    except HTTPError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        #other error
        raise HTTPException(status_code=500, detail="error api pokemon") 



@app.post("/toto")
def other():
    print("post")


