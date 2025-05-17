def get_weather(city:str):
    return "31 degree"
available_tools={
    'get_weather':{
        "fn":get_weather,
        "description":"Takes a city name as an input and return current weather of the city"
    }
}
print(available_tools.get('get_weather',False).get("fn")('New York'))