import requests


class Downloader:
    requests_options = {
        'method': 'GET',
        'url': None,
        'data': None
    }

    url = ""
    url_base = None
    race_id = None
    race_name = None
    requests_response = None
    race_data = []
    official_team_name = 'REDOLAT TEAM'
    team_name = ['REDOLAT TEAM', 'REDOLATTEAM', 'Redolat Team', 'RedolatTeam', 'Redolat', 'redolatteam', 'redolat team']

    def __init__(self, url):
        self.url = url
        self.process_url()
        self.get_data()
        self.process_data()
    
    def process_url(self):
        pass

    def get_data(self):
        self.requests_response = requests.request(self.requests_options['method'], self.requests_options['url'], data=self.requests_options['data'])
   
    def process_data(self):
        pass