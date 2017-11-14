import requests
import urllib.parse
import json

API_KEY = '<your_key_goes_here>'


region_dic = {'BR'	:	'br1.api.riotgames.com',
                'EUNE'	: 	'eun1.api.riotgames.com',
                'EUW'	:	'euw1.api.riotgames.com',
                'JP'	:	'jp1.api.riotgames.com',
                'KR'	:	'kr.api.riotgames.com',
                'LAN'	:	'la1.api.riotgames.com',
                'LAS'	:	'la2.api.riotgames.com',
                'NA'	:	'na1.api.riotgames.com',
                'OCE'	:	'oc1.api.riotgames.com',
                'TR'    :	'tr1.api.riotgames.com',
                'RU'	:	'ru.api.riotgames.com',
                'PBE'	:	'pbe1.api.riotgames.com'}

#whatareOURodds



class Summoner: 
    def __init__(self, summoner_name: str, region: str):
        self.base_url =  'https://' + region_dic[region.upper()]
        self.summoner_id = None
        self.summoner_name = summoner_name
        self.account_id = None
        self.rank = None
        self.last_ranked_games = []
        # Below this, we initialize summoner_id and account_id.    
        try:
            request_url =  '{}/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(self.base_url, self.summoner_name ,API_KEY)
            response = requests.get(request_url)
            json_object = response.json()
            response.close()
            self.summoner_id = json_object['id']
            self.account_id = json_object['accountId']
        except:
            print( json_object['status']['message'])

    def request_rank(self)->str:
        ''' Finds the rank of a summoner. (e.g. Diamond V 18LP) '''
        if self.rank == None:         
            request_url =  '{}/lol/league/v3/leagues/by-summoner/{}?api_key={}'.format(self.base_url,  str(self.summoner_id) , API_KEY)
            response = requests.get(request_url)
            json_object = response.json()
            response.close()
            try:
                
                self.rank = '{} {} {} LP'.format(json_object[0]['tier'] , json_object[0]['entries'][0]['rank'] ,
                                           str(json_object[0]['entries'][0]['leaguePoints']))
                return self.rank
            except:
                print( json_object['status']['message'])

        return self.rank

    def recent_ranked_win_percentage(self):
        '''Takes self.last_ranked_games and finds the winrate'''
        win_perc = 0.0
        if len(self.last_ranked_games) != 0:
            # win_list = []
            for match_id in self.last_ranked_games:
                json_object = None
                try:
                    request_url = '{}/lol/match/v3/matches/{}?api_key={}'.format(self.base_url, str(match_id), API_KEY)
                    response = requests.get(request_url)
                    json_object = response.json()
                    response.close()
                except:
                    print('hotdog')
                for player in json_object['participantIdentities']:
                    if player['player']['accountId'] == self.account_id:
                        pId = player['participantId']
                        break
                teamId = json_object['participants'][pId-1]['teamId']

                win = False
                if (json_object['teams'][0]['teamId'] == teamId):
                    if (json_object['teams'][0]['win'] == 'Win'):
                        win = True
                else:
                    if (json_object['teams'][1]['win'] == 'Win'):
                        win = True
                if win:
                    win_perc += 100.0
                # win_list.append(win)
            print('{} has a {:.2f}% win rate in the past {} ranked games.'.format(self.summoner_name, (win_perc / len(self.last_ranked_games)),len(self.last_ranked_games)))
            
        else:
            print('{} has had no ranked games in the last 20 games.'.format(self.summoner_name))

    
    def request_recent_ranked_games(self):
        ''' Returns a list of ranked games in the past 20 games in a list.'''
        if self.base_url and self.account_id:
            try:
                ranked_id_list = []
                URL =  '{}/lol/match/v3/matchlists/by-account/{}/recent?api_key={}'.format(self.base_url, self.account_id , API_KEY)
                response = requests.get(URL)
                json_object = response.json()
                response.close()
                for match in json_object['matches']:
                    if match['queue'] == 420:
                        ranked_id_list.append(match['gameId'])
                self.last_ranked_games = ranked_id_list
            except:
                print('Error.')

    def print_rank(self):
        return(self.rank)
    
