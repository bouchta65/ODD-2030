from flask import render_template
from APP import app
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns
from flask import render_template, session, redirect, url_for
from APP import app
from .utils import (calculate_average_age, calculate_number_of_persons,
                    calculate_top_city, calculate_average_number_of_persons,
                    calculate_gender_percentage, calculate_quality_of_life_statistics)

import os

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Classeur2.xlsx')
excel_file = upload_path

file_path = excel_file


def load_data(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

def calculate_average_age_by_gender(data):
    avg_age_by_gender = data.groupby('Genre')['Âge'].mean().reset_index()
    avg_age_by_gender_dict = avg_age_by_gender.set_index('Genre').to_dict()['Âge']
    return avg_age_by_gender_dict

def calculate_population_by_city(data):
    population_by_city = data['Ville'].value_counts().reset_index()
    population_by_city.columns = ['City', 'Population']
    population_by_city_dict = population_by_city.set_index('City').to_dict()['Population']
    return population_by_city_dict

def calculate_salary_distribution(data):
    salary_ranges = ['>2000', '2000-4000', '4000-6000', '6000-8000', '<8000','-']
    salary_distribution = {range: {'Masculin': 0, 'Féminin': 0} for range in salary_ranges}
    for index, row in data.iterrows():
        salary_range = row['Salaire mensuel']
        gender = row['Genre']
        if salary_range in salary_ranges:
            salary_distribution[salary_range][gender] += 1
    return salary_distribution

def calculate_population_chaque_city(data):
    specified_cities = ['Boujdour', 'Es-Smara', 'Laâyoune', 'Tarfaya']
    population_by_city = {}
    male_count_by_city = {}
    female_count_by_city = {}
    total_population, total_males, total_females = 0, 0, 0
    for city in specified_cities:
        city_data = data[data['Ville'] == city]
        population_by_city[city] = len(city_data)
        male_count_by_city[city] = round((len(city_data[city_data['Genre'] == 'Masculin']) / population_by_city[city]) * 100 )
        female_count_by_city[city] = round((len(city_data[city_data['Genre'] == 'Féminin']) / population_by_city[city]) * 100 )
        total_population += population_by_city[city]
        total_males += (male_count_by_city[city] / 4)
        total_females += (female_count_by_city[city] / 4)
    population_by_city['Total'] = total_population
    male_count_by_city['Total'] = total_males
    female_count_by_city['Total'] = total_females
    return population_by_city, male_count_by_city, female_count_by_city

def create_satisfaction_quality_chart(data):
    data['Satisfaction au travail'] = data['Satisfaction au travail'].map({'Oui': 1, 'Non': 0})
    data['Qualité de vie'] = data['Qualité de vie'].map({'Oui': 1, 'Non': 0})
    data.dropna(subset=['Âge', 'Satisfaction au travail', 'Qualité de vie'], inplace=True)
    age_bins = [18, 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77, 82, 87, 92, 97, 102]
    age_labels = [f'{start}-{end}' for start, end in zip(age_bins[:-1], age_bins[1:])]
    data['Age Group'] = pd.cut(data['Âge'], bins=age_bins, labels=age_labels, right=False)
    grouped_data = data.groupby('Age Group')[['Satisfaction au travail', 'Qualité de vie']].mean().reset_index()
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.lineplot(data=grouped_data, x='Age Group', y='Satisfaction au travail', label='Satisfaction au travail', marker='o', color='blue', ax=ax)
    sns.lineplot(data=grouped_data, x='Age Group', y='Qualité de vie', label='Qualité de vie', marker='o', color='green', ax=ax)
    ax.set_xlabel('Groupe d\'âge', fontsize=14)
    ax.set_ylabel('Score moyen', fontsize=14)
    ax.legend(title='Légende', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    return img_str

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    data = load_data(file_path)
    if data is None:
        return "File not found. Please check the file path."

    average_age, min_age, max_age = calculate_average_age()
    avg_age_by_gender = calculate_average_age_by_gender(data)
    population_by_city_dict = calculate_population_by_city(data)
    top_cities = calculate_top_city()
    average_cities = calculate_average_number_of_persons(top_cities)
    img_str = create_satisfaction_quality_chart(data)
    average_personnes = calculate_number_of_persons()
    salary_distribution = calculate_salary_distribution(data)
    population_by_city, male_count_by_city, female_count_by_city = calculate_population_chaque_city(data)
    charmin, charmax = calculate_gender_percentage()
    average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()

    return render_template('dashboard.html',
                           population_by_city=population_by_city,
                           male_count_by_city=male_count_by_city,
                           female_count_by_city=female_count_by_city,
                           charmin=charmin,
                           population_by_city_dict=population_by_city_dict,
                           charmax=charmax,
                           average_quality=average_quality,
                           percentage_oui=percentage_oui,
                           percentage_non=percentage_non,
                           img_str=img_str,
                           average_cities=average_cities,
                           top_cities=top_cities,
                           average_age=average_age,
                           min_age=min_age,
                           max_age=max_age,
                           average_personnes=average_personnes,
                           avg_age_by_gender=avg_age_by_gender,
                           salary_distribution=salary_distribution)
