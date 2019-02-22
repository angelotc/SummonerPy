
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

        # Instantiate Summoner
        s = Summoner(i, 'na')

        # Populate recent_ranked_games
        s.get_recent_ranked_games()

        # Calculate recent recent ranked win percentage
        s.recent_ranked_win_percentage()

        # Populate the rank within the Summoner object
        s.get_rank()

        # Print the rank frm the Summoner object
        s.print_rank()
