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

def generate_boxplot_data():
    # Read the Excel file
    data = pd.read_excel(upload_path)
    
    # Select relevant columns
    databoxplot = data[['Ville', 'Repas de poisson']]
    
    return databoxplot

@app.route('/boxplot_data')
def boxplot_data():
    databoxplot = generate_boxplot_data()
    return databoxplot.to_json(orient='records')

def get_stacked_bar_data():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Group data by city and calculate percentages
    grouped_data = data.groupby('Ville').apply(lambda x: (x['Participation à des nettoyages de plage'].value_counts(normalize=True) * 100, x['Réduction de l\'utilisation de plastique'].value_counts(normalize=True) * 100))

    # Prepare data for the chart
    chart_data = {
        "cities": [],
        "participation_plage": [],
        "reduction_plastique": []
    }

    for city, (participation_plage, reduction_plastique) in grouped_data.items():
        chart_data["cities"].append(city)
        chart_data["participation_plage"].append(participation_plage.get('Oui', 0))
        chart_data["reduction_plastique"].append(reduction_plastique.get('Oui', 0))

    return chart_data

@app.route('/stacked_bar_data')
def stacked_bar_data():
    chart_data = get_stacked_bar_data()
    return jsonify(chart_data)




def get_doughnut_data():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Calculate the counts for Participation à des nettoyages de plage by Genre
    participation_counts = data.groupby(['Genre', 'Participation à des nettoyages de plage']).size().unstack(fill_value=0)

    # Calculate percentages
    participation_percentage = participation_counts.div(participation_counts.sum(axis=1), axis=0) * 100

    # Prepare the data for JSON response
    response_data = []
    for genre in participation_percentage.index:
        response_data.append({
            'Genre': genre,
            'Oui': participation_percentage.loc[genre, 'Oui'],
            'Non': participation_percentage.loc[genre, 'Non']
        })

    return response_data

@app.route('/doughnut_data')
def doughnut_data():
    data = get_doughnut_data()
    return jsonify(data)



def calculate_awareness_percentage():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Count the number of respondents who have heard about plastic pollution issues
    heard_about_plastic_pollution = data['Problèmes de pollution plastique'].value_counts()

    # Calculate the percentage of respondents who have heard about plastic pollution issues
    total_respondents = len(data)
    percentage = (heard_about_plastic_pollution.get('Oui', 0) / total_respondents) * 100

    return percentage

@app.route('/plastic_pollution_awareness')
def plastic_pollution_awareness():
    percentage = calculate_awareness_percentage()
    return jsonify({"percentage": percentage})

def get_grouped_bar_data():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Calculate the total counts for each city and each category
    grouped_data = data.groupby(['Ville', 'Participation à des nettoyages de plage'])['Camping à la plage'].sum().unstack().fillna(0)

    # Calculate percentages
    grouped_data = round(grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100,2)

    # Reset index for easier handling in JSON
    grouped_data = grouped_data.reset_index()

    # Ensure columns are named correctly
    if 'Oui' not in grouped_data.columns:
        grouped_data['Oui'] = 0
    if 'Non' not in grouped_data.columns:
        grouped_data['Non'] = 0

    return grouped_data.to_dict(orient='records')

@app.route('/grouped_bar_data')
def grouped_bar_data():
    data = get_grouped_bar_data()
    return jsonify(data)

@app.route('/ODD14')
def ODD14():
   
        average_age, min_age, max_age = calculate_average_age()
        percentage = calculate_awareness_percentage()
        grouped_data = get_grouped_bar_data()
        databoxplot = generate_boxplot_data()
        chart_data = get_stacked_bar_data()
        # Calculate population by city
        top_cities = calculate_top_city()
        average_cities = calculate_average_number_of_persons(top_cities)
        average_personnes = calculate_number_of_persons()
        charmin, charmax = calculate_gender_percentage()
        
        # Calculate quality of life statistics
        average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()
        
        return render_template(
            'ODD14.html',
            percentage =percentage,
            databoxplot =databoxplot,
            grouped_data = grouped_data,
            chart_data = chart_data,
            charmin=charmin,
            charmax=charmax,
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
   
def descriptive_analysis():
    # Lire le fichier Excel
    data = pd.read_excel(upload_path)
    
    # Effectuer l'analyse descriptive
    description = data.describe()
    
    # Convertir le résumé statistique en un format JSON
    description_json = description.to_json()
    
    return description_json

@app.route('/descriptive_analysis')
def get_descriptive_analysis():
    # Obtenir l'analyse descriptive
    analysis = descriptive_analysis()
    
    return analysis
