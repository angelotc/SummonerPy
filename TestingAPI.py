
from Summoner import *

def take_input()-> list:
    ''' given the lobby chat, parses the league names and returns a list of the
        summoners.'''
    l = []
    print("Copy/paste your lobby's summonernames:")
    while len(l) != 5:
        
        try:
            x = input()
            l.append(x[:-17])
        except:
            print('Error')
            take_input()
    return l[:6]




if __name__ == '__main__':
    region ='na'

    
    l = take_input()

    for i in l:
        
        s = Summoner(i, 'na')
        s.request_recent_ranked_games()
        s.recent_ranked_win_percentage()
        s.request_rank()
        s.print_rank()
