# reference https://github.com/suarez605/SpainRentalHeatMaps

import os
from flask import Flask
from flask import render_template
import pandas as pd
import folium
from folium.plugins import HeatMap


app = Flask(__name__)

app.secret_key = 'Veritas'

@app.route('/')
def display_intro():
    return render_template('index.html')

@app.route('/emergency_symptoms')
def display_emergency_symptoms():
    return render_template('emergency_symptoms.html')

@app.route('/exposure')
def display_exposure():
    return render_template('exposure.html')

@app.route('/view_survey_results')
def display_survey_results():
    return render_template('view_survey_results.html')

@app.route('/drawMap')
def draw_map():

    map_data = pd.read_csv("./Data/data_01.csv", sep=';')
    lat = map_data['LATITUDE'].mean()
    lon = map_data['LONGITUDE'].mean()
    startingLocation = [lat, lon]  # [39.47, -0.37]
    hmap = folium.Map(location=startingLocation, zoom_start=15)
    max_amount = map_data['PricePerSquareMeters'].max()
    hm_wide = HeatMap(
        list(zip(map_data.LATITUDE.values, map_data.LONGITUDE.values, map_data.PricePerSquareMeters.values)),
        min_opacity=0.2,
        max_val=max_amount,
        radius=17, blur=15,
        max_zoom=1)

    # Adds the heatmap element to the map
    hmap.add_child(hm_wide)
    # Saves the map to heatmap.html
    hmap.save(os.path.join('./templates', 'heatmap.html'))
    # Render the heatmap
    return render_template('heatmap.html')

