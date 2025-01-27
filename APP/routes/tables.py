from flask import render_template, session, redirect, url_for, request
import pandas as pd
import os
from flask import Flask
from APP import app
from .utils import (
    calculate_average_age,
    calculate_number_of_persons,
    calculate_top_city,
    calculate_average_number_of_persons,
    calculate_gender_percentage,
    calculate_quality_of_life_statistics
)

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def analyze_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Define a mapping for converting categorical variables
    value_mapping = {
        "Oui": 1, "Non": 0, "oui": 1, "non": 0,
        "Faible": 1, "Moyenne": 2, "Élevée": 3,
        "Insatisfait": 1, "Moyennement satisfait": 2, "Satisfait": 3,
        "Célibataire": 1, "Marié(e)": 2, "Divorcé(e)": 3, "Veuf/Veuve": 4,
        "Masculin":1,"Féminin":2
    }
    
    # Convert specific columns to numerical values based on the mapping
    for column in df.columns:
        if df[column].dtype == object:
            df[column] = df[column].map(value_mapping).fillna(df[column])
    
    # Perform descriptive analysis
    desc = df.describe(include='all').transpose()
    
    # Drop the 'unique', 'top', and 'freq' columns
    desc = desc.drop(columns=['unique', 'top', 'freq'], errors='ignore')
    
    return desc

@app.route('/tables', methods=['GET'])
def tables():
    if 'email' not in session:
        return redirect(url_for('login'))

    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Classeur2.xlsx')
    excel_file = upload_path

    data = pd.read_excel(excel_file) 

    first_5_columns = data.iloc[:, :5]
    table_data = first_5_columns.to_dict(orient='records')

    average_age, min_age, max_age = calculate_average_age()
    top_cities = calculate_top_city()
    average_cities = calculate_average_number_of_persons(top_cities)
    average_personnes = calculate_number_of_persons()
    charmin, charmax = calculate_gender_percentage()
    average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()

    # Analyse descriptive
    desc = analyze_excel(excel_file)
    desc_html = desc.to_html(classes='table table-striped table-bordered', border=0, table_id='desc-table')

    return render_template('tables.html', table_data=table_data,
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
        average_personnes=average_personnes,
        desc_html=desc_html)

@app.route('/tables', methods=['POST'])
def upload_file():
    if 'formFile' not in request.files:
        return redirect(url_for('table', message='No file part'))

    file = request.files['formFile']

    if file.filename == '':
        return redirect(url_for('table', message='No selected file'))

    try:
        if file:
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Classeur2.xlsx')
            print("Upload Path:", upload_path)
            file.save(upload_path)
            return redirect(url_for('table', message='File uploaded successfully'))
    except Exception as e:
        return redirect(url_for('table', message=f'Error: {str(e)}'))

@app.route('/tables')
def table():
    message = request.args.get('message', '')
    return render_template('tables.html', message=message)
