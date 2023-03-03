from bs4 import BeautifulSoup
import requests
from Domain.Downloader import Downloader
from urllib.parse import urlparse

class TopRun(Downloader):
    url_base = 'https://www.toprun.es/stats/$$race_name$$/clasdata/modalidad/$$modalidad$$'

    def __init__(self, url):
        super().__init__(url)

    def process_url(self):
        """
        url: http://www.toprun.es/stats/viii-marato-de-la-calderona-2023/clasificaciones/modalidad/21k
        """
        url_race = urlparse(self.url)
        self.race_id = url_race.path.split('/')[5]
        self.race_name = url_race.path.split('/')[2]

        url_download = self.url_base.replace('$$race_name$$', self.race_name)
        url_download = url_download.replace('$$modalidad$$', self.race_id)

        self.requests_options['url'] = url_download

    def process_data(self):
        runners = self.requests_response.json()['data']
        runners = self.__get_rankings_by_club(runners)
        self.race_data = self.__set_rankings_format(runners)
        print("self.race_data")
        print(self.race_data)
        
    def __get_rankings_by_club(self, runners):
        """
        example = [
                [
            "<font style='background-color:#FFD700; border-style:double;border-radius: 5px 5px 50px 50px; border-color: #FFD700;'><b>1</b></font>",
            "02:08:59",
            "687",
            "<a href='/stats/viii-marato-de-la-calderona-2023/participante/21K/687'><span class='glyphicon glyphicon-plus-sign' aria-hidden='true'></span> <b>MIGUEL ANGEL RODRIGUEZ SANCHEZ</b></a>",
            "M",
            "<font style='background-color:#FFD700; border-style:double; border-radius: 5px 5px 50px 50px; border-color: #FFD700;'><b>1</b></font>",
            "21k-Absoluta M",
            "CORREMON TRAIL",
            "6:08"
        ],...
        ]
        """
        ruuners_by_club = []
        for runner in runners:
            if runner[7] in self.team_name:
                ruuners_by_club.append(runner)

        return ruuners_by_club

    def __set_rankings_format(self, runners):
        new_runners = []

        for runner in runners:
            runner = self.__get_runner_details(runner)
            new_runners.append(runner)

        return new_runners

    def __get_runner_details(self, runner):
        """
        url: https://www.toprun.es/stats/viii-marato-de-la-calderona-2023/participante/21K/687
        """
        url_pattern = 'https://www.toprun.es/stats/$$race_name$$/participante/$$modalidad$$/$$dorsal$$'
        url = url_pattern.replace('$$race_name$$', self.race_name)
        url = url.replace('$$modalidad$$', self.race_id)
        url = url.replace('$$dorsal$$', runner[2])

        response = requests.request('GET', url)
        
        status_code = response.status_code

        new_runner = {}

        if status_code == 200:
            html = BeautifulSoup(response.text, "html.parser")
            properties_htlm = html.find_all('div', {'class': 'row'})[0].find_all('dd')

            dorsal = runner[2]
            name = properties_htlm[1].getText()
            gender = properties_htlm[2].getText()
            category = properties_htlm[3].getText()
            club = properties_htlm[4].getText()
            
            realoficialTime = properties_htlm[5].getText().split('/')
            oficialTime = realoficialTime[0].strip()
            realTime = realoficialTime[1].strip()
            average = properties_htlm[6].getText()
            posCategoryGeneral = properties_htlm[7].getText().split(" ")[0].replace('º','')
            posCategoryGender = properties_htlm[8].getText().split(" ")[0].replace('º','')
            posCategory = properties_htlm[9].getText().split(" ")[0].replace('º','')

            new_runner = self.__build_runner_object(dorsal, name, club, True, gender, oficialTime, realTime, posCategory, posCategoryGeneral, posCategoryGender, average, category, 'None', 'None', 'None', 'None', 'None')
        
        return new_runner

    def __build_runner_object(self, dorsal, name, club, finished, gender, officialTime, realTime, pos, catPos, genPos, averageOficialTime, category, realPos, realCatPos, realGenPos, averageRealTime, nationality=None):
        """
            keys: dorsal, name, club, nationality, finished, gender, officialTime, realTime, pos, catPos, genPos, averageOficialTime, category, realPos, realCatPos, realGenPos	averageRealTime
        """
        runner = {
            "dorsal": dorsal,
            "name": name,
            "club": club,
            "nationality": nationality,
            "finished": finished,
            "gender": gender,
            "officialTime": officialTime,
            "realTime": realTime,
            "pos": pos,
            "catPos": catPos,
            "genPos": genPos,
            "averageOficialTime": averageOficialTime,
            "category": category,
            "realPos": realPos,
            "realCatPos": realCatPos,
            "realGenPos": realGenPos,
            "averageRealTime": averageRealTime
        }

        return runner