
import requests
def get_random_quote():
    url= "https://zenquotes.io/api/random"
    response=requests.get(url)
    data=response.json()
    quote=data[0]["q"]
    author=data[0]["a"]
    return quote,author
