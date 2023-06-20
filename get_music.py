import requests
import os
import random
from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes
import csv

# get client data
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

#authorization
token_header = {"Content-Type": "application/x-www-form-urlencoded"}

data = {
   "grant_type": "client_credentials",
   "client_id": client_id,
   "client_secret": client_secret
}

x = requests.post("https://accounts.spotify.com/api/token",headers = token_header,data = data)
x = x.json()
token = x.get('access_token')
token_type = x.get('token_type')
authorization_header = {"Authorization":token_type + " " + token}

#user inputs  
while True:
   genre = str(input("Genre: ")).strip().lower()
   # request for available genres
   result = requests.get('https://api.spotify.com/v1/recommendations/available-genre-seeds',headers= authorization_header)
   genres = result.json()
   # check genre in a genre-seeds
   if genre not in genres['genres']:
      print("genre isn't available")
   else:
      break

while True:
   number = int(input("How many tracks ? "))
   if number == 0 or number > 50:
      print('number of tracks (1-50)')
   else:
      break

# request for total track 
total = requests.get(f'https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track',headers= authorization_header)
total = total.json()
total = total['tracks']['total']
offset = random.randint(0,total - 1)

#request
result = requests.get(f'https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&limit={number}&offset={offset}',headers= authorization_header)
response = result.json()

# printing song , artist and url 
table = PrettyTable(header=True, padding_width=10)
table = ColorTable(theme=Themes.OCEAN)
table.field_names = [" ","song", "artist","link"]
for i in range(number):
   x = response['tracks']['items'][i]['uri'].split(":")
   table.add_row([i+1,response['tracks']['items'][i]['name'],response['tracks']['items'][i]['artists'][0]['name'],f'http://open.spotify.com/track/{x[2]}'],divider=True)
   
print(table)

# saving playlist to csv
with open('playlist.csv', 'w') as file:
   writer = csv.writer(file)
   field = ["song", "artist", "link"]

   writer.writerow(field)
   for i in range(number):
      writer.writerow([response['tracks']['items'][i]['name'],response['tracks']['items'][i]['artists'][0]['name'],f'http://open.spotify.com/track/{x[2]}'])











