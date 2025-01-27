from flask import render_template,session
from APP import app
import io
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns
from .utils import calculate_average_age
from .utils import calculate_number_of_persons
from .utils import calculate_top_city
from .utils import calculate_average_number_of_persons
from .utils import calculate_gender_percentage
from .utils import calculate_quality_of_life_statistics

@app.route('/maps')
def maps():
    if 'email' not in session:
        return redirect(url_for('login'))
       # Calculate average age
    average_age ,min_age, max_age = calculate_average_age()

    # Calculate population by city
    top_cities = calculate_top_city()
    average_cities = calculate_average_number_of_persons(top_cities)
    average_personnes = calculate_number_of_persons()
    charmin , charmax = calculate_gender_percentage()

    # calculate_quality_of_life_statistics
    average_quality, percentage_oui, percentage_non = calculate_quality_of_life_statistics()
    return render_template('maps.html',
   
    charmin=charmin,
    charmax=charmax,
    average_quality=average_quality, percentage_oui=percentage_oui, percentage_non=percentage_non,
    average_cities=average_cities, 
    top_cities=top_cities,
    average_age=average_age,min_age=min_age, max_age=max_age,
    average_personnes=average_personnes, )
 
