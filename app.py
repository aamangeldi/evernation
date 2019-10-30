import json

import eq_config

from flask import Flask
from flask import render_template
from sheets import extract_country_data
from sheets import get_sheets_data

app = Flask(__name__)

CONFIG = eq_config.get_config()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the spreadsheet
SPREADSHEET_ID = CONFIG['google_spreadsheet_id']
RANGE = 'D1:J57'

# TODO: replace, orienteer dev for now
MAPS_API_KEY = CONFIG['maps_api_key']

@app.route('/')
def map():
    data = get_sheets_data(SPREADSHEET_ID, RANGE, SCOPES)
    country_data = extract_country_data(data)
    questions = [question_data[0][1] for question_data in country_data]
    print(country_data)
    print('hello')
    return render_template(
        'map.html',
        country_data=country_data,
        questions=questions,
        maps_api_key=MAPS_API_KEY,
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
