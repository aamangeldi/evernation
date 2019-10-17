from __future__ import print_function

import os.path
import pickle

import eq_config

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CONFIG = eq_config.get_config()


def get_sheets_data(spreadsheet_id, range, scopes):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token, protocol=2)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
        majorDimension='COLUMNS',
    ).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    return values


def identify_countries(bad_data):
    bad_data = bad_data.lower()
    identified = []
    if any(
        hint in bad_data for hint in [
            'russia',
        ]
    ):
        identified.append('Russia')
    if any(
        hint in bad_data for hint in [
            'china',
            'chinese',
        ]
    ):
        identified.append('China')
    if bad_data == 'us' or any(
        hint in bad_data for hint in [
            'united states',
            'maine',
            'california',
            'america',
            'usa',
            ', ny',
            ', ca',
            'boston',
            'new york',
            'the us',
            '/ usa',
            ', us',
        ]
    ):
        identified.append('United States')
    if any(
        hint in bad_data for hint in [
            'india',
        ]
    ) and 'indiana' not in bad_data:
        identified.append('India')
    if any(
        hint in bad_data for hint in [
            'canada',
            'canadian'
        ]
    ):
        identified.append('Canada')
    if any(
        hint in bad_data for hint in [
            'israel',
            'jewish'
        ]
    ):
        identified.append('Israel')
    if any(
        hint in bad_data for hint in [
            'kazakh',
        ]
    ):
        identified.append('Kazakhstan')
    if any(
        hint in bad_data for hint in [
            'jamaica',
        ]
    ):
        identified.append('Jamaica')
    if any(
        hint in bad_data for hint in [
            'ukraine',
            'ukrainian',
        ]
    ):
        identified.append('Ukraine')
    if any(
        hint in bad_data for hint in [
            'italy',
            'italian',
        ]
    ):
        identified.append('Italy')
    # uk might also be in other countries
    if bad_data == 'uk' or any(
        hint in bad_data for hint in [
            'british',
            '/ uk /',
            'scotland',
        ]
    ):
        identified.append('United Kingdom')
    if any(
        hint in bad_data for hint in [
            'turkmenistan',
        ]
    ):
        identified.append('Turkmenistan')
    if any(
        hint in bad_data for hint in [
            'mexico',
            'mexican',
        ]
    ):
        identified.append('Mexico')
    if any(
        hint in bad_data for hint in [
            'brazil',
        ]
    ):
        identified.append('Brazil')
    if any(
        hint in bad_data for hint in [
            'belarus',
        ]
    ):
        identified.append('Belarus')
    if any(
        hint in bad_data for hint in [
            'nepal',
        ]
    ):
        identified.append('Nepal')
    if any(
        hint in bad_data for hint in [
            'taiwan',
        ]
    ):
        identified.append('Taiwan')
    if any(
        hint in bad_data for hint in [
            'ethiopia',
        ]
    ):
        identified.append('Ethiopia')
    if not identified:
        identified.append('UNCLEAR')
    return identified


def extract_country_data(data):
    question_and_country_data = []
    for column in data:
        # print('------------------------')
        country_data = []
        country_dict = {}
        for index, row in enumerate(column):
            # remove emojis, tnx Binam!
            row = row.encode('ascii', 'ignore')
            if index == 0:
                country_data.append(['Country', row])
                # print(row)
            else:
                countries = identify_countries(row)
                # print(row)
                for country in countries:
                    if country in country_dict.keys():
                        country_dict[country] += 1
                    else:
                        country_dict[country] = 1
        # print(country_dict)

        for key, value in country_dict.items():
            country_data.append([key, value])
        question_and_country_data.append(country_data)
    # NOTE: for now only care about the first 3 questions
    return question_and_country_data[0:3]


if __name__ == '__main__':
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = CONFIG['google_spreadsheet_id']
    RANGE = 'D1:J29'

    data = get_sheets_data(SPREADSHEET_ID, RANGE, SCOPES)
    country_data = extract_country_data(data)
    # print(country_data)
