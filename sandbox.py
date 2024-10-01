def main(waypoint):
    pieces = waypoint.split('-')    
    output  = {
            "sector": pieces[0],
            "system": "-".join (pieces[:2]),
            "waypoint": waypoint
            }
    return output
if __name__ == '__main__':
    print(main("X1-ZB2-A1"))

