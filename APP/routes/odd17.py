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

def get_heatmap_data():
    # Lire le fichier Excel
    data = pd.read_excel(r"C:\Users\pc\Desktop\New folder\stage\Project-stage\Classeur2 (version 1).xlsx")

    # Préparer les données pour la heatmap
    heatmap_data = data.pivot_table(index='Ville', columns='Satisfaction de laccès aux infrastructures publiques', aggfunc='size', fill_value=0)
    
    heatmap_data_dict = {
        "z": heatmap_data.values.tolist(),
        "x": heatmap_data.columns.tolist(),
        "y": heatmap_data.index.tolist()
    }

    return heatmap_data_dict

# Route pour récupérer les données de la heatmap
@app.route('/heatmap')
def heatmap():
    data = get_heatmap_data()
    return data                              


# Fonction pour récupérer les données du pourcentage d'implication dans des initiatives de bénévolat par ville
def get_doughnut_data():
    # Lire le fichier Excel
    data = pd.read_excel(upload_path)

    # Calculer le pourcentage d'implication dans des initiatives de bénévolat (oui et non) pour chaque ville
    percentage_data = data.groupby(['Ville', 'Implication dans des initiatives de bénévolat']).size().unstack(fill_value=0)
    percentage_data['Total'] = percentage_data.sum(axis=1)
    percentage_data['Pourcentage_oui'] = percentage_data['Oui'] / percentage_data['Total'] * 100
    percentage_data['Pourcentage_non'] = percentage_data['Non'] / percentage_data['Total'] * 100

    # Convertir les données au format JSON
    doughnut_data = {
        'labels': percentage_data.index.tolist(),
        'datasets': [
            {
                'data': percentage_data['Pourcentage_oui'].tolist(),
                'backgroundColor': ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
                'label': 'Pourcentage de participation (Oui)'
            },
            {
                'data': percentage_data['Pourcentage_non'].tolist(),
                'backgroundColor': ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
                'label': 'Pourcentage de non-participation (Non)'
            }
        ]
    }

    return doughnut_data

# Route pour récupérer les données du diagramme en anneau
@app.route('/doug')
def doug():
    data = get_doughnut_data()
    return jsonify(data)



# Fonction pour récupérer les données du pourcentage de participation à des projets de développement communautaire par statut matrimonial
def get_bar_chart_data():
    # Lire le fichier Excel
    data = pd.read_excel(upload_path)

    # Calculer le pourcentage de participation à des projets de développement communautaire (oui et non) pour chaque statut matrimonial
    percentage_data = data.groupby(['Statut matrimonial', 'Participation à des projets de développement communautaire']).size().unstack(fill_value=0)
    percentage_data['Total'] = percentage_data.sum(axis=1)
    percentage_data['Pourcentage_oui'] = percentage_data['Oui'] / percentage_data['Total'] * 100
    percentage_data['Pourcentage_non'] = percentage_data['Non'] / percentage_data['Total'] * 100

    # Convertir les données au format JSON
    bar_chart_data = {
        'labels': percentage_data.index.tolist(),
        'datasets': [
            {
                'label': 'Pourcentage de participation (Oui)',
                'data': percentage_data['Pourcentage_oui'].tolist(),
                'backgroundColor': 'rgba(255, 99, 132, 0.5)' # Couleur pour la participation (Oui)
            },
            {
                'label': 'Pourcentage de non-participation (Non)',
                'data': percentage_data['Pourcentage_non'].tolist(),
                'backgroundColor': 'rgba(54, 162, 235, 0.5)' # Couleur pour la non-participation (Non)
            }
        ]
    }

    return bar_chart_data

# Route pour récupérer les données du graphique à barres
@app.route('/bar')
def bar():
    data = get_bar_chart_data()
    return jsonify(data)

@app.route('/ODD17')
def ODD17():
   
        average_age, min_age, max_age = calculate_average_age()
     
        # Calculate population by city
        top_cities = calculate_top_city()
        average_cities = calculate_average_number_of_persons(top_cities)
        average_personnes = calculate_number_of_persons()
        charmin, charmax = calculate_gender_percentage()
        
        # Calculate quality of life statistics
        average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()
        
        return render_template(
            'ODD17.html',
     
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
   

