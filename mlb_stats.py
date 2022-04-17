import argparse
import csv
import datetime
import logging
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


def grab_player_stats(players_id: list, players_list: list) -> list:
    player_stats = []
    homerun_stats = []
    for each in players_list:
        for player in players_id:
            if each in player.keys():
                stats = statsapi.player_stat_data(player[each]['id'], group="[hitting]", type="season")
                player_stats.append({each: stats})
                for stat in stats['stats']:
                    homerun_stats.append({each: {"homeRuns": stat['stats']['homeRuns']}})
    return player_stats, homerun_stats


def grab_players_ids(players_list: list) -> list:
    players_id = []
    for player in players_list:
        players = statsapi.lookup_player(player)
        for data in players:
            player_id = {data['fullName']: {"id": data['id']}}
            players_id.append(player_id)

    return players_id


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

    players_id = grab_players_ids(players_list)
    player_stats, homerun_stats = grab_player_stats(players_id, players_list)

    if args.write_csv_bool:
        with open(f"mlb_hr_leaders_{date_time}.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            fields = ['Name', 'Homeruns']

            csvwriter.writerow(fields)

            for player in players_list:
                for each in homerun_stats:
                    if player in each.keys():
                        row = [player, each[player]['homeRuns']]
                        csvwriter.writerow(row)


if __name__ == '__main__':
    main()
