from flask import render_template, request, jsonify
from APP import app
import pandas as pd
import plotly.io as pio
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import io
import base64
import plotly.express as px
from .utils import (
    calculate_average_age,
    calculate_number_of_persons,
    calculate_top_city,
    calculate_average_number_of_persons,
    calculate_gender_percentage,
    calculate_quality_of_life_statistics
)
import os 
from APP import app
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Classeur2.xlsx')
def get_confidence_data():
    # Load data
    data = pd.read_excel(upload_path)
    
    # Specify the cities
    specified_cities = ['Boujdour', 'Es-Smara', 'Laâyoune', 'Tarfaya']
    
    # Initialize a dictionary to store population counts
    population_by_city = {}
    Faible_count = {}
    Moyen_count = {}
    Élevé_count = {}
    # Initialize total population counter
    # Calculate population count for each specified city
    for city in specified_cities:
        city_data = data[data['Ville'] == city]
        population_by_city[city] = len(city_data)
        Faible_count[city] = round((len(city_data[city_data['Confiance dans la police locale'] == 'Faible']) / population_by_city[city]) * 100 )
        Moyen_count[city] = round((len(city_data[city_data['Confiance dans la police locale'] == 'Moyenne']) / population_by_city[city]) * 100 )
        Élevé_count[city] = round((len(city_data[city_data['Confiance dans la police locale'] == 'Élevée']) / population_by_city[city]) * 100 )
       
    return population_by_city,Faible_count,Moyen_count,Élevé_count

def get_stacked_bar_data():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Prepare the data for the stacked bar chart
    grouped_data = data.groupby(['Ville', 'Genre', 'Aide juridique']).size().unstack(fill_value=0)

    stacked_bar_data = {
        "categories": grouped_data.index.tolist(),
        "series": [{"name": col, "data": grouped_data[col].tolist()} for col in grouped_data.columns]
    }

    return stacked_bar_data

@app.route('/stacked_bar')
def stacked_bar():
    data = get_stacked_bar_data()
    return jsonify(data)



def get_doughnut_data():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Prepare the data for the doughnut chart
    response_counts = data['Satisfaction de la rapidité de traitement des demandes administratives'].value_counts()
    doughnut_data = {
        "labels": response_counts.index.tolist(),
        "values": response_counts.tolist()
    }

    return doughnut_data

@app.route('/doughnut_16')
def doughnut_16():
    data = get_doughnut_data()
    return jsonify(data)



def get_heatmap_data():
    # Lire le fichier Excel
    data = pd.read_excel(upload_path)

    # Préparer les données pour la heatmap
    heatmap_data = data.pivot_table(index='Ville', columns='Victime', aggfunc='size', fill_value=0)
    
    heatmap_data_dict = {
        "z": heatmap_data.values.tolist(),
        "x": heatmap_data.columns.tolist(),
        "y": heatmap_data.index.tolist()
    }

    return heatmap_data_dict

@app.route('/heatmap_data')
def heatmap_data():
    data = get_heatmap_data()
    return jsonify(data)




def get_pie_chart_data():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Count the number of participants by genre
    pie_data = data.groupby(['Genre', 'Participation à des activités politiques']).size().unstack(fill_value=0)

    # Prepare data for pie chart
    pie_chart_data = {
        "labels": pie_data.index.tolist(),
        "values": pie_data.sum(axis=1).tolist()
    }

    return pie_chart_data

@app.route('/pie_chart_data')
def pie_chart_data():
    data = get_pie_chart_data()
    return jsonify(data)

@app.route('/ODD16')
def ODD16():
   
        average_age, min_age, max_age = calculate_average_age()
     
        # Calculate population by city
        top_cities = calculate_top_city()
        grouped_data = get_stacked_bar_data()
        population_by_city,Faible_count,Moyen_count,Élevé_count = get_confidence_data()
        average_cities = calculate_average_number_of_persons(top_cities)
        average_personnes = calculate_number_of_persons()
        charmin, charmax = calculate_gender_percentage()
        
        # Calculate quality of life statistics
        average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()
        
        return render_template(
            'ODD16.html',
     
            charmin=charmin,
            grouped_data=grouped_data,
            charmax=charmax,
            population_by_city=population_by_city,Faible_count=Faible_count,Moyen_count=Moyen_count,Élevé_count=Élevé_count,
            average_quality=average_quality,
            percentage_oui=percentage_oui,
            percentage_non=percentage_non,
            average_cities=average_cities, 
            top_cities=top_cities,
            average_age=average_age,
            min_age=min_age,
            max_age=max_age,
            average_personnes=average_personnes
        )
   

