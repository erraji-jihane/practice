# GET request practice — JokeAPI

import requests

# calling the JokeAPI ------ no API key needed just a GET request
r = requests.get('https://v2.jokeapi.dev/joke/Any')

# .json() parses the response into a Python dictionary
print("=======================================================\n")
dataJson = r.json()
print(dataJson)

#after we checked teh json we can go ahead and access specific attributes
print("=======================================================\n")
print(dataJson['error']) #this is to check the error
print(dataJson['setup']) #this is to check the message (setup)
print(dataJson['delivery']) #this is to check the answer(delivery)
print(dataJson['lang']) #this is to check the language
print(dataJson['flags']['religious']) #this is to check if it is a religious flag inside the dictionary flag


# dir(r) shows all available attributes and methods on the response object
print("=======================================================\n")
print(dir(r))

# .content returns the raw response as bytes (it starts with b)
print("=======================================================\n")
print(r.content)

# .text returns the response as a plain string (not parsed)
print("=======================================================\n")
print(r.text)