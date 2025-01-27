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

def get_grouped_bar_chart_data():
    # Lire le fichier Excel
    data = pd.read_excel(upload_path)

    # Calculer le nombre de personnes pour chaque combinaison de "Possession d'un jardin" et "Contribution à la plantation d'arbres"
    grouped_data = data.groupby(['Possession dun jardin', 'Contribution à la plantation darbres']).size().unstack(fill_value=0)

    # Convertir les données au format JSON
    grouped_bar_chart_data = {
        'labels': grouped_data.index.tolist(),
        'datasets': [
            {
                'label': 'Oui',
                'data': grouped_data['Oui'].tolist(),
                'backgroundColor': 'rgba(75, 192, 192, 0.5)'
            },
            {
                'label': 'Non',
                'data': grouped_data['Non'].tolist(),
                'backgroundColor': 'rgba(255, 99, 132, 0.5)'
            }
        ]
    }

    return grouped_bar_chart_data

# Route pour récupérer les données du diagramme en barres groupées
@app.route('/grouped_bar_chart_data')
def grouped_bar_chart_data():
    data = get_grouped_bar_chart_data()
    return jsonify(data)


def get_pie_chart_data():
    # Lire le fichier Excel
    data = pd.read_excel(upload_path)

    # Calculer le pourcentage d'implication dans des initiatives de bénévolat (oui et non) pour chaque ville
    percentage_data = data.groupby(['Ville', 'Possession dun jardin']).size().unstack(fill_value=0)
    percentage_data['Total'] = percentage_data.sum(axis=1)
    percentage_data['Pourcentage_oui'] = round(percentage_data['Oui'] / percentage_data['Total'] * 100)
    percentage_data['Pourcentage_non'] = round(percentage_data['Non'] / percentage_data['Total'] * 100)

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




# Route pour récupérer les données du pie chart
@app.route('/pie_data')
def pie_data():
    data = get_pie_chart_data()
    return jsonify(data)

def get_percentage_data():
    # Lire le fichier Excel
    # file_path = r"C:\Users\pc\Desktop\New folder\stage\Project-stage\Classeur2 (version 1).xlsx"
    data = pd.read_excel(upload_path)

    # Vérifier les colonnes disponibles dans le DataFrame
    required_columns = ['Ville', 'Genre', 'Fréquence des activités']
    if not all(column in data.columns for column in required_columns):
        raise KeyError(f"Les colonnes nécessaires ne sont pas présentes dans le fichier Excel : {required_columns}")

    # Calculer le pourcentage de la fréquence des activités pour chaque ville et genre
    percentage_data = data.groupby(['Ville', 'Genre'])['Fréquence des activités'].value_counts(normalize=True).mul(100).reset_index(name='Percentage')

    return percentage_data

# Route pour récupérer les données du diagramme à barres
@app.route('/percentage_data')
def percentage_data():
    data = get_percentage_data()
    return data.to_json(orient='records')



def calculate_awareness_percentage():
    # Read the Excel file
    data = pd.read_excel(upload_path)

    # Count the number of respondents who have heard about plastic pollution issues
    heard_about_plastic_pollution = data['Participation à des programmes de sensibilisation'].value_counts()

    # Calculate the percentage of respondents who have heard about plastic pollution issues
    total_respondents = len(data)
    percentage = (heard_about_plastic_pollution.get('Oui', 0) / total_respondents) * 100

    return percentage

@app.route('/plastic_awareness')
def plastic_awareness():
    percentage = calculate_awareness_percentage()
    return jsonify({"percentage": percentage})





def get_doughnut_data():
    # Lire le fichier Excel
    # file_path = r"C:\Users\pc\Desktop\New folder\stage\Project-stage\Classeur2 (version 1).xlsx"
    data = pd.read_excel(upload_path)

    # Vérifier la colonne disponible dans le DataFrame
    column_name = 'Efficacité des efforts'
    if column_name not in data.columns:
        raise KeyError(f"La colonne nécessaire n'est pas présente dans le fichier Excel : {column_name}")

    # Compter les occurrences de chaque valeur (1 à 5)
    value_counts = data[column_name].value_counts().sort_index()

    # Calculer le pourcentage de chaque valeur
    total_responses = value_counts.sum()
    percentages = [round((count / total_responses) * 100, 2) for count in value_counts]
    
    # Préparer les données pour le diagramme en anneau
    doughnut_data = {
        'labels': ['1 (Faible)', '2', '3', '4', '5 (Élevée)'],
        'datasets': [{
            'data': percentages,
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        }]
    }

    return doughnut_data


# Route pour récupérer les données du diagramme en anneau
@app.route('/doughnut_da')
def doughnut_da():
    data = get_doughnut_data()
    return jsonify(data)


@app.route('/ODD15')
def ODD15():
   
        average_age, min_age, max_age = calculate_average_age()
     
        # Calculate population by city
        top_cities = calculate_top_city()
        average_cities = calculate_average_number_of_persons(top_cities)
        average_personnes = calculate_number_of_persons()
        charmin, charmax = calculate_gender_percentage()
        
        # Calculate quality of life statistics
        average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()
        
        return render_template(
            'ODD15.html',
     
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
   

