# Reverse Geocode

import googlemaps
import pandas as pd

df = pd.read_csv("all_prediction_data.csv")

lat = df['lat'].tolist()
lng = df['lng'].tolist()
countries = []

for i in range(0, len(lat), 1):
    temp_lat = lat[i]
    temp_lng = lng[i]
    temp = (temp_lat, temp_lng)
    gmaps = googlemaps.Client(key='AIzaSyCjADkN3fdVvVU-LI9IibqUS_QVJ83QYe4')
    geocode_result = gmaps.reverse_geocode(temp)
    if geocode_result != []:
        geocode_result = geocode_result[0]['address_components']

    for c in geocode_result:
        if "country" in c['types']:
            countries.append(c['long_name'])
            break
    else:
        countries.append("Not found")
        