import argparse
import csv
import datetime
import os
import statsapi
import sys

from operator import itemgetter

date_time = datetime.datetime.now()
global USER
USER = os.path.expanduser('~')


def parse_boolean(value):

    value = value.lower()

    if value == "true":
        return True
    elif value =='false':
        return False


def search_players(players_list: list, mlb_stats: list) -> list:

    my_team = []
    points = int()
    for player in mlb_stats:
        for my_player in players_list:
            if my_player.__eq__(player['player_name']):
                my_team.append(player)
                points += player['home_runs']

    return points, my_team


def grab_mlb_stats(print_bool: bool) -> list:
    rookie_hr = statsapi.league_leaders('homeRuns', season=2022, playerPool = None, limit=1000)
    rookie_hr_leaders = rookie_hr.split('\n')
    hr_leaders = []
    state = True
    number_of_players = int()

    for item in rookie_hr_leaders:
        if item == '' or state:
            state = False
            continue

        name = item.split(" ")[3]
        last = item.split(" ")[4]

        if name == "":
            name = item.split(" ")[4].strip()
            last = item.split(" ")[5]

        hr_var = item.replace(" ", "")
        home_runs = hr_var[-1]

        if hr_var[-2].isnumeric():
            home_runs = hr_var[-2] + home_runs

        if last == 'A.':
            also_last = item.split(" ")[5]
            home_runs = item.split(" ")[19]
            hr_leaders.append({"player_name": f"{name} {last} {also_last}", "home_runs": int(home_runs) })
            continue

        hr_leaders.append({"player_name": f"{name} {last}", "home_runs": int(home_runs)})

    hr_leaders_format = sorted(hr_leaders, key = itemgetter('home_runs'), reverse=True)

    for player in hr_leaders_format:
        if player['player_name']:
            number_of_players += 1
        if print_bool:
            print(f"{player['player_name']}")
            print(f"Home Run's: {player['home_runs']}\n")

    return hr_leaders_format, number_of_players


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-pl", "--players-list",
                        required=False,
                        type=str,
                        help="Give a list of players to parse (in csv format)")

    parser.add_argument("-pb", "--print-bool",
                        required=False,
                        type=parse_boolean,
                        help="True or False to print players out")

    parser.add_argument("-wcb", "--write-csv-bool",
                        required=False,
                        type=parse_boolean,
                        help="True or False to write out your teams csv")

    args = parser.parse_args()

    os.chdir(f"{USER}/Documents")
    players_list = []

    if args.players_list:
        with open(args.players_list, 'r') as file:
                csvfile = csv.reader(file)
                for line in csvfile:
                    for name in line:
                        if name == 'Name':
                            continue
                        elif not name == '':
                            players_list.append(name)

    mlb_stats, number_of_players = grab_mlb_stats(args.print_bool)

    points, my_players_list = search_players(players_list, mlb_stats)

    if args.write_csv_bool:
        with open(f"mlb_hr_leaders_{date_time}.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            fields = ['Name', 'Homeruns']

            csvwriter.writerow(fields)

            for player in mlb_stats:
                row = [player['player_name'], player['home_runs']]
                csvwriter.writerow(row)

        if args.players_list:
            with open(f"homerun_team_{date_time}.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                fields = ['Name', 'Homeruns', f"My Points: {points}"]

                csvwriter.writerow(fields)

                for player in my_players_list:
                    row = [player['player_name'], player['home_runs']]
                    csvwriter.writerow(row)

    if args.players_list:
        print(f"Points: {points}")
        print("Your Team:")
        for each in my_players_list:
            print(f"\n{each['player_name']} : {each['home_runs']} home run(s)")

if __name__ == '__main__':
    main()
