import requests
import os 
import json

FACTION = "COSMIC"

PATH_STR = '~/.config/spacetraders/token'

def make_request (endpoint, params=None, headers=None, data=dict(), post=False):
    base_url = 'https://api.spacetraders.io/v2'

    url = os.path.join(base_url, endpoint)
    if headers is None:
        headers=dict()
    if endpoint.startswith('my'):
        headers.update({'Authorization': f'Bearer {get_token(PATH_STR)}'})
        
        

    if post:
        headers.update({'Content-Type': 'application/json'})
        r = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    else:
        r = requests.get(url, params=params, headers=headers)

    return r.json()

def register_agent(faction, path_str):
    endpoint = 'register'
    while True:
        symbol = input("please input symbol! Registering new agent!\n")
        data = {'symbol': symbol, 'faction': faction}


        r = make_request(endpoint,data=data,post=True)

        if 'error' not in r:
            break
        print(r)

    token_path = os.path.expanduser(path_str)
    with open (token_path, 'w') as file: 
        file.write (r['data']['token'])
    
    
def get_token(path_str):
    token_path = os.path.expanduser(path_str)
    with open (token_path, 'r') as file:
        token = file.read().strip()

    return token


def split_waypoint(waypoint):
    pieces = waypoint.split('-')
    output  = {
            "sector": pieces[0],
            "system": "-".join (pieces[:2]),
            "waypoint": waypoint
            }
    return output


def get_location(system, waypoint):
    endpoint = f'systems/{system}/waypoints/{waypoint}'

    
    return  make_request(endpoint)


def get_agent():
    endpoint = 'my/agent'

    r = make_request(endpoint)

    if 'error' in r:
        register_agent(FACTION,PATH_STR)
        r = make_request(endpoint)

    return r 


def view_contracts():
    endpoint = 'my/contracts'
    
    return make_request(endpoint, headers=headers)['data']


def find_e_asteroid(waypoint): 

    swp = split_waypoint(waypoint)

    endpoint = f'systems/{swp["system"]}/waypoints'
    params = {'type': 'ENGINEERED_ASTEROID'}
    
    return  make_request(endpoint,params=params)


def get_all_shipyards(waypoint): 

    swp = split_waypoint(waypoint)

    endpoint = f'systems/{swp["system"]}/waypoints'
    params = {'traits': 'SHIPYARD'}
    
    return  make_request(endpoint,params=params)


def view_ships(shipyard):

    endpoint = f'systems/{shipyard["systemSymbol"]}/waypoints/{shipyard["symbol"]}/shipyard'


    return make_request(endpoint)


def purchase_ship(choicelocation,choiceship):
    endpoint = 'my/ships' 
    
    data = {
            'shipType': choiceship,
            'waypointSymbol': choicelocation
            }


    ## return make_request(endpoint, data=data, post=True)
    print (data)

def purchase_shipui(waypoint):
    shipyard  = find_shipyard(waypoint)
    ship = find_ship(shipyard)
    purchase = purchase_ship (shipyard['symbol'],ship['type'])

    return purchase


def accept_contract(contractid):
    endpoint = f'my/contracts/{contractid}/accept'
    

    return make_request(endpoint, headers=headers, post=True)

def find_shipyard(waypoint):
    shipyards  = get_all_shipyards(waypoint)['data']
    choicelocation = user_choice(shipyards,'symbol')
    return choicelocation


def find_ship(choicelocation): 

    ships  = view_ships(choicelocation)['data']['shipTypes']
    choiceship = user_choice(ships,'type')
    return choiceship


def user_choice(func_var,index_var):
    while True:
        for i, list_stuff in enumerate(func_var,1):
            print (i,list_stuff[index_var])
        input_var = input("Please choose number!")
        if input_var.isdigit():
            return func_var[int(input_var)-1]
        if type(input_var)!= int:
            print("pick a number dillhole")

def main():

    agent = get_agent()
    waypoint = agent['data']['headquarters']

    easteroid = find_e_asteroid(waypoint)
    print (easteroid)
if __name__ == '__main__':
    main()
    
