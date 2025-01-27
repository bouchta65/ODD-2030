from flask import render_template, request, jsonify, session, redirect, url_for
from APP import app
import pandas as pd
import plotly.io as pio
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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
   


def generate_bar():
    data = pd.read_excel(upload_path)
    filtered_data = data[data['Participation à des activités de sensibilisation'] == 'Oui']
    bar_data = filtered_data.groupby('Ville').size().reset_index(name='Count')
    bar_data_json = bar_data.to_json(orient='records')
    return bar_data_json

@app.route('/bar_data')
def bar_data():
    if 'email' not in session:
        return redirect(url_for('login'))
    bar_data_json = generate_bar()
    return jsonify({'bar_data_json': bar_data_json})

def calculate_relationship():
    data = pd.read_excel(upload_path)
    relationship = data.groupby(['Augmentation des températures', 'Mesures contre les changements climatiques']).size().reset_index(name='Count')
    relationship_data = relationship.to_dict(orient='records')
    return relationship_data

def generate_doughnut_chart_data():
    data = pd.read_excel(upload_path)
    doughnut_data = data['Connaissance des politiques gouvernementales'].value_counts().reset_index()
    doughnut_data.columns = ['Connaissance', 'Count']
    doughnut_data_json = doughnut_data.to_json(orient='records')
    return doughnut_data_json

@app.route('/doughnut')
def doughnut():
    if 'email' not in session:
        return redirect(url_for('login'))
    doughnut_data_json = generate_doughnut_chart_data()
    return jsonify({'doughnut_data_json': doughnut_data_json})

def generate_bar_chart_data():
    data = pd.read_excel(upload_path)
    bar_data = data.groupby(['Transports durables', 'Tri et recyclage des déchets'])['Mesures contre les changements climatiques'].size().reset_index(name='Frequency')
    bar_data_json = bar_data.to_json(orient='records')
    return bar_data_json

@app.route('/dt')
def dt():
    if 'email' not in session:
        return redirect(url_for('login'))
    bar_data_json = generate_bar_chart_data()
    return jsonify({'bar_data_json': bar_data_json})

@app.route('/data')
def data():
    if 'email' not in session:
        return redirect(url_for('login'))
    relationship_data = calculate_relationship()
    return jsonify(relationship_data)

def calculate_statistics():
    data = pd.read_excel(upload_path)
    stats_dict = {}
    for city, group in data.groupby('Ville'):
        variable = group['Appareils électroniques en veille']
        stats_dict[city] = {
            'Minimum': round(np.min(variable), 2),
            'Maximum': round(np.max(variable), 2),
            'Moyenne': round(np.mean(variable), 2),
            'Médiane': round(np.median(variable), 2),
            'Écart': round(np.std(variable), 2),
            'Variance': round(np.var(variable), 2),
            'Quartile1': round(np.percentile(variable, 25), 2),
            'Médian': round(np.percentile(variable, 50), 2),
            'Quartile3': round(np.percentile(variable, 75), 2)
        }
    return stats_dict

@app.route('/ODD13')
def ODD13():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    bar_data = generate_bar()
    stats_dict = calculate_statistics()
    relationship_data = calculate_relationship()
    doughnut_data_json = generate_doughnut_chart_data()
    bar_data_json = generate_bar_chart_data()

    average_age, min_age, max_age = calculate_average_age()
    top_cities = calculate_top_city()
    average_cities = calculate_average_number_of_persons(top_cities)
    average_personnes = calculate_number_of_persons()
    charmin, charmax = calculate_gender_percentage()
    average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()
    
    return render_template(
        'ODD13.html',
        relationship_data=relationship_data,
        stats_dict=stats_dict,
        doughnut_data_json=doughnut_data_json,
        bar_data_json=bar_data_json,
        charmin=charmin,
        bar_data=bar_data,
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
