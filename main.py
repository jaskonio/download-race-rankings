import pandas as pd
import requests
import os
import argparse
from bs4 import BeautifulSoup


def get_rankings_from_sportmaniacs_by_id_rece(race_id):
    url_base = 'https://sportmaniacs.com/es/races/rankings/'
    data = requests.get(url=url_base + race_id)
    data_json = data.json()
    return data_json


def get_rankings_by_club(data, club):
    rankings = data['data']['Rankings']
    rankings_by_club_list = [row for row in rankings if row['club'] == club]
    return rankings_by_club_list


def conver_list_to_data_frame(data_list):
    data_frame = pd.DataFrame(data_list)
    return data_frame


def json_normalize(data):
    return pd.io.json.json_normalize(data)


def set_rankings_format(rankings):
    delete_keys = ['category_id', 'user_id', 'defaultImage', 'photos', 'externalPhotos', 'externalVideos',
                   'externalDiploma', 'Points']
    for row in rankings:
        # delete key pos
        key_pos = [key for key in row.keys() if 'pos_' in key][0]
        delete_keys.append(key_pos)
        # delete keys
        results = [row.pop(key, None) for key in delete_keys]
        # print("Actual Keys")
        # print(results)
        # Update gender value
        row['gender'] = 'Masculino' if row['gender'] == 'gender_0' else 'Femenino'
    return rankings


def create_excel(data, file_name):
    print('create_excel')
    export_folder = os.getcwd() + '/' + 'exports' + '/'

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    print('Folder Export Path: ' + export_folder)
    print('File Name: ' + file_name)

    data_frame = pd.DataFrame(data)
    data_frame.to_excel(export_folder + file_name + '.xlsx')

    return True

def process_link_spormaniacs(url_race):
    process_team_name = 'REDOLAT TEAM'

    race_id = url_race.split('/')[-1]
    race_name = url_race.split('/')[5:6][0]

    data = get_rankings_from_sportmaniacs_by_id_rece(race_id)
    rankings_redolat_team = get_rankings_by_club(data, process_team_name)
    rankings_redolat_team = set_rankings_format(rankings_redolat_team)

    create_excel(rankings_redolat_team, race_name)

def process_ValenciaCiudadDelRunning_data(url, payload):
    print('url: ' + url)
    print('payload: ' + str(payload))

    req = requests.request("POST", url, data=payload)

    status_code = req.status_code

    runners = []

    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        table_section = html.find('table', {'id': 'tabModulos'})
        runners_section = table_section.find_all('tr')
        #print('Processed runners_section. tr: ' + str(runners_section))

        for i, runner_section in enumerate(runners_section):
            #print('Processed runner_section: ' + str(runner_section))

            if i == 0:
                continue

            runner = {}

            elements = runner_section.find_all('td')
            #print('Processed td: ' + str(elements))

            runner_keys = ['Pos General', 'Dorsal', 'Pos Categorai', 'Nombre', 'Tiempo Oficial', 'Tiempo Real',
                           'Ritmo Medio', 'Categoria']

            for index, elem in enumerate(elements):
                #print('Processed index : ' + str(index))
                #print('Processed elem: ' + str(elem))

                runner[runner_keys[index]] = elem.getText()

            #print('Processed Runner: ' + str(runner))

            runners.append(runner)

    else:
        print("Status Code: " + str(status_code))

    return runners

def set_ValenciaCiudadDelRunning_format(runners):
    for runner in runners:

        runner['Genero'] = 'MASCULIN' if runner['Categoria'].startswith('M') else 'FEMENI'
        runner['Club'] = 'REDOLAT TEAM'

    return runners


def process_link_valenciaciudaddelrunning(url):
    """

    :param url: Example: https://www.valenciaciudaddelrunning.com/medio/resultados-medio-maraton-2017/
    :return: None
    """
    url_base = 'https://resultados.valenciaciudaddelrunning.com/medio-maraton-clubs.php?y=$$year$$'

    race_name = 'medio-maraton-clasificados-$$year$$'
    year = ''.join([str(x) for x in [int(s) for s in url if s.isdigit()]])

    url = url_base.replace('$$year$$', year)
    race_name = race_name.replace('$$year$$', year)

    payload_search_box_name = 'search-box' if int(year) > 2017 else'selequipo'
    payload = {payload_search_box_name: 'REDOLAT TEAM'}

    runners = process_ValenciaCiudadDelRunning_data(url, payload)
    runners = set_ValenciaCiudadDelRunning_format(runners)

    #print("runners: " + str(runners))
    create_excel(runners, race_name)


def process_link(url_race):

    if 'sportmaniacs' in url_race:
        print("Platform: Sportmaniacs")
        process_link_spormaniacs(url_race)
    elif 'valenciaciudaddelrunning' in url_race:
        print("Platform: valenciaciudaddelrunning")
        process_link_valenciaciudaddelrunning(url_race)
    else:
        print("Platform not compatible")


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--link", help="Link de la carrera")

args = parser.parse_args()

if args.link:
    url_race = args.link
    print("link: " + url_race)
    process_link(url_race)
