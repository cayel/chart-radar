import pandas as pd
import random
import string
from datetime import datetime, timedelta

def create_df_ranking() :
    # Define the data
    data = {
        'id': ['efe220cb-4981-40c7-8a6b-bd89b3569a17', generate_fake_id()],
        'name': ['Far Out', generate_fake_name()],
        'description': ['The 10 greatest goth albums of all time', generate_fake_description()],
        'url': ['https://faroutmagazine.co.uk/the-10-greatest-goth-albums-of-all-time/', generate_fake_url()],
        'style': ['Gothic', generate_fake_style()],
        'year': ['', generate_fake_year()],
        'date': ['22/05/2023', generate_fake_date('01/01/2010', '31/12/2023')],
        'language': ['en', 'fr'],
        'created_date': ['26/02/2024', generate_fake_date('01/01/2024', '29/02/2024')],
        'active': [True, True]
    }    
    # Create a DataFrame from the data
    df = pd.DataFrame(data)
    return df

def generate_fake_id():
    # Generate a random string of fixed length
    id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=36))

    return id

def generate_fake_name():
    # Generate a random string of fixed length
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    return name

def generate_fake_description():
    # Generate a random string of fixed length
    description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))

    return description

def generate_fake_url():
    # Generate a random string of fixed length
    url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    return url  

def generate_fake_style():
    # Generate a random string of fixed length
    style = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    return style    

def generate_fake_year():
    # Generate a random string of fixed length
    year = ''.join(random.choices(string.digits, k=4))

    return year 

def generate_fake_date(start_date, end_date):
    # Convertir les dates en objets datetime
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    # Calculer le nombre de jours entre les deux dates
    days_between = (end_date - start_date).days

    # Générer un nombre aléatoire de jours à ajouter à la date de début
    random_number_of_days = random.randrange(days_between)

    # Ajouter le nombre aléatoire de jours à la date de début
    random_date = start_date + timedelta(days=random_number_of_days)

    # Convertir la date aléatoire en string au format "dd/mm/yyyy"
    random_date_str = random_date.strftime("%d/%m/%Y")

    return random_date_str
