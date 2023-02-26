import pandas as pd
import requests
import os
import argparse

from Domain.Sportmaniacs import Sportmaniacs
from Domain.Valenciaciudaddelrunning import Valenciaciudaddelrunning

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

def race_factory(url_race):
    downloader = None

    if 'sportmaniacs' in url_race:
        print("Platform: Sportmaniacs")
        downloader = Sportmaniacs(url_race)

    elif 'valenciaciudaddelrunning' in url_race:
        print("Platform: valenciaciudaddelrunning")
        downloader = Valenciaciudaddelrunning(url_race)
    else:
        print("Platform not compatible")

    return downloader

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--link", help="Link de la carrera")

args = parser.parse_args()

if args.link:
    url_race = args.link
    print("link: " + url_race)

    downloader = race_factory(url_race)
    race_name = downloader.race_name
    data = downloader.race_data

    create_excel(data, race_name)
