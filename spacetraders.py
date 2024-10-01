import requests
import os 
import json

FACTION = "COSMIC"

PATH_STR = '~/.config/spacetraders/token'

def make_request (endpoint, params=None, headers=None, data=None, post=False):
    base_url = 'https://api.spacetraders.io/v2'


    url = os.path.join(base_url, endpoint)
    if post:
        r = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    else:
        r = requests.get(url, params=params, headers=headers)

    return r.json()

def register_agent(faction, path_str):
    endpoint = 'register'
    headers = {'Content-Type': 'application/json'}
    while True:
        symbol = input("please input symbol!\n")
        data = {'symbol': symbol, 'faction': faction}


        r = make_request(endpoint,headers=headers,data=data,post=True)

        if 'error' not in r:
            break
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


def get_location(token, system, waypoint):
    endpoint = f'systems/{system}/waypoints/{waypoint}'
    headers = {'Authorization': f'Bearer {token}'}

    
    return  make_request(endpoint,headers=headers)


def get_agent(token):
    endpoint = 'my/agent'

    headers = {'Authorization': f'Bearer {token}'}


    r = make_request(endpoint, headers=headers)
    if 'error' in r:
        register_agent(FACTION,PATH_STR)
        r = make_request(endpoint, headers=headers)

    return r 


def view_contracts(token):
    endpoint = 'my/contracts'
    headers = {'Authorization': f'Bearer {token}'}
    
    return make_request(endpoint, headers=headers)['data']


def get_all_shipyards(token,waypoint): 

    swp = split_waypoint(waypoint)

    endpoint = f'systems/{swp["system"]}/waypoints'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'traits': 'SHIPYARD'}
    
    return  make_request(endpoint,headers=headers,params=params)


def view_ships(token,shipyard):

    endpoint = f'systems/{shipyard["systemSymbol"]}/waypoints/{shipyard["symbol"]}/shipyard'
    headers = {'Authorization': f'Bearer {token}'}


    return make_request(endpoint, headers=headers)


def purchase_ship(token,shipType,waypoint):
    endpoint = 'my/ships' 
    headers = {'Authorization': f'Bearer {token}'}
    
    data = {
            'shipType': shipType,
            'waypointSymbol': waypoint
            }


    return make_request(endpoint, headers=headers, data=data, post=True)


def purchase_shipui(token,waypoint):
    find = find_shipyard(token,waypoint)  
    view = view_ships(token,find)
    print(view)
    return
    purchase = purchase_ship (token,shipType,waypoint)


   ## return make_request(endpoint, headers=headers, data=data, params=params, post=True)





## worflow = find shipyard based on existing system, via waypoint use view_ships, user input to define what type of ship using purchase_ship. Construct purchase_shipui, use as wrapper for previous 3 functions to streamline this process.  


def accept_contract(token, contractid):
    endpoint = f'my/contracts/{contractid}/accept'
    headers = {'Authorization': f'Bearer {token}'}
    

    return make_request(endpoint, headers=headers, post=True)

def find_shipyard(token,waypoint,):
    shipyards  = get_all_shipyards(token,waypoint)['data']
    choice = user_choice(shipyards,'symbol')
    return choice


def find_ship(token,shipyard): 

    ships  = view_ships(token,shipyard)['data']['shipTypes']
    choice = user_choice(ships,'type')
    return choice
    # while True:
        # for i, shiptype in enumerate(view,1):
            # print (i,shiptype['type'])
        # shipchoice = input("Pleae choose number!")
        # if shipchoice.isdigit():
            # return view[int(shipchoice)-1]
        # if type(shipchoice)!= int:
            # print("pick a number dillhole")


def user_choice(func_var,index_var):
    while True:
        for i, list_stuff in enumerate(func_var,1):
            print (i,list_stuff[index_var])
        input_var = input("Please choose number!")
        if input_var.isdigit():
            return func_var[int(input_var)-1]
        if type(input_var)!= int:
            print("pick a number dillhole")
##  Goals weeek of 9/16: create seperate funtion to abstract above 2 functions. Goal is to achieve same output with user choosing shipyard and ship all housed under one "choice" function.

def main():

    token = get_token(PATH_STR)
    agent = get_agent(token)
    waypoint = agent['data']['headquarters']

    shipyard = find_shipyard(token,waypoint)
    # print (testfind)
    findship = find_ship(token,shipyard)
    print (findship)
    ##  shipui = purchase_shipui(token,waypoint)
    ## request = make_request("factions")
    ## print(request)

if __name__ == '__main__':
    main()
    
