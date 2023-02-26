from Domain.Downloader import Downloader
from bs4 import BeautifulSoup

class Valenciaciudaddelrunning(Downloader):
    url_base = 'https://resultados.valenciaciudaddelrunning.com/medio-maraton-clubs.php?y=$$year$$'

    def __init__(self) -> None:
        super().__init__()
    
    def process_url(self):
        url = self.url
        
        year = ''.join([str(x) for x in [int(s) for s in url if s.isdigit()]])
        url = self.url_base.replace('$$year$$', year)

        race_name = 'medio-maraton-clasificados-$$year$$'
        self.race_name = race_name.replace('$$year$$', year)


        payload_search_box_name = 'search-box' if int(year) > 2017 else'selequipo'
        self.requests_options['data'] = {payload_search_box_name: self.official_team_name}

    def process_data(self):
        self.race_data = self.__process_ValenciaCiudadDelRunning_data()
        self.race_data = self.__set_ValenciaCiudadDelRunning_format()

    def __process_ValenciaCiudadDelRunning_data(self):
        req = self.requests_response

        status_code = req.status_code

        runners = []

        if status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")

            table_section = html.find('table', {'id': 'tabModulos'})
            runners_section = table_section.find_all('tr')

            for i, runner_section in enumerate(runners_section):
                if i == 0:
                    continue

                runner = {}

                elements = runner_section.find_all('td')

                runner_keys = ['Pos General', 'Dorsal', 'Pos Categorai', 'Nombre', 'Tiempo Oficial', 'Tiempo Real',
                            'Ritmo Medio', 'Categoria']

                for index, elem in enumerate(elements):
                    runner[runner_keys[index]] = elem.getText()

                runners.append(runner)

        else:
            print("Status Code: " + str(status_code))

        return runners

    def __set_ValenciaCiudadDelRunning_format(self):
        runners = self.race_data

        for runner in runners:

            runner['Genero'] = 'MASCULIN' if runner['Categoria'].startswith('M') else 'FEMENI'
            runner['Club'] = self.official_team_name

        return runners