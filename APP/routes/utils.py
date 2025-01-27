
import pandas as pd
import os
from flask import render_template, session, redirect, url_for, request
import pandas as pd
from APP import app
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Classeur2.xlsx')
   
def calculate_average_age():
    # data = pd.read_excel(excel_file) 

    # Check if data is available
    data = pd.read_excel(upload_path)
    
    # Calculate average, minimum, and maximum age
    age = data['Âge'].mean()
    min_age = data['Âge'].min()
    max_age = data['Âge'].max()

    # Round the average age to 2 decimal places
    average_age_rounded = round(age,0)

    return average_age_rounded, min_age, max_age





def calculate_number_of_persons():
    # Load data
    data = pd.read_excel(upload_path)
    
    # Get the number of persons (number of rows in the DataFrame)
    number_of_persons = data.shape[0]
    
    return number_of_persons





def calculate_top_city():
    # Load data
    data = pd.read_excel(upload_path)

    # Calculate population by city
    population_by_city = data['Ville'].value_counts().reset_index()
    population_by_city.columns = ['City', 'Population']

    # Sort cities by population
    population_by_city = population_by_city.sort_values(by='Population', ascending=False)

    # Select the city with the highest population
    top_city_name = population_by_city.iloc[0]['City']

    return top_city_name



def calculate_average_number_of_persons(top_city):
    # Load the data from the Excel file
    data = pd.read_excel(upload_path)


    # Calculate the total number of individuals in all cities
    total_individuals = len(data)

    # Calculate the total number of individuals in the top city
    individuals_in_top_city = len(data[data['Ville'] == top_city])

    # Calculate the average number of individuals in the top city compared to all cities
    calc = (individuals_in_top_city / total_individuals)*100 
    average_number_of_persons = round(calc , 2)
    return average_number_of_persons



import pandas as pd

def calculate_gender_percentage():
    # Load the data from the Excel file
    data = pd.read_excel(upload_path)

    # Calculate the total number of individuals
    total_individuals = len(data)

    # Calculate the number of male individuals
    male_count = len(data[data['Genre'] == 'Masculin'])

    # Calculate the number of female individuals
    female_count = len(data[data['Genre'] == 'Féminin'])

    # Calculate the percentage of male individuals
    male_percentage = (male_count / total_individuals) * 100

    # Calculate the percentage of female individuals
    female_percentage = (female_count / total_individuals) * 100

   # Determine the maximum and minimum percentages
    if male_percentage > female_percentage:
        max_percentage = round(male_percentage, 2)
        charmax = str(max_percentage)+"%"+" "+"M"
        min_percentage = str(round(female_percentage, 2) )
        charmin = str(min_percentage)+"%"+" "+"F"

    else:
        max_percentage = str(round(female_percentage, 2))
        charmax = str(max_percentage)+"%"+" "+"F"
        min_percentage = str(round(male_percentage, 2))
        charmin = str(min_percentage)+"%"+" "+"M"
    return charmax, charmin

def calculate_quality_of_life_statistics():
    # Load data
    data = pd.read_excel(upload_path)

    # Convert 'Qualité de vie' to numeric (1 for 'Oui', 0 for 'Non')
    data['Qualité de vie'] = data['Qualité de vie'].map({'Oui': 1, 'Non': 0})

    # Filter out rows with missing values
    data.dropna(subset=['Qualité de vie'], inplace=True)

    # Calculate average niveau de qualité de vie
    average_quality = round(data['Qualité de vie'].mean()*100,2)

    # Calculate percentages of people who said 'Oui' and 'Non'
    total_count = len(data)
    oui_count = data[data['Qualité de vie'] == 1].count()['Qualité de vie']
    non_count = data[data['Qualité de vie'] == 0].count()['Qualité de vie']
    
    percentage_oui = round((oui_count / total_count) * 100)
    percentage_non = round((non_count / total_count) * 100)

    return average_quality, percentage_oui, percentage_non