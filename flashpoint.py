import argparse
import sys
import json
import os
import uuid
import sqlite3
import re
import random


def main():
    args = parse_arguments()
    field = get_field_to_sort(args)
    playlist = get_playlist(args.input)
    games = get_games(playlist)
    db_cursor = get_db_cursor()
    new_playlist = replace_playlist_id(playlist, db_cursor)
    if field != "random":
        games_info = get_games_info(games, db_cursor, field)
    else:
        games_info = games
    # close connection to database
    con.close()
    save_playlist(new_playlist, games_info, field, args.output, args.descending)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Sort your Flashpoint playlist by the field of your choice!")
    parser.add_argument("-i", "--input", help="the input file which contains the playlist you want to sort in JSON format; default is playlist.json", nargs="?",
                        default="playlist.json", type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-o", "--output", help="the output file which is where the sorted playlist will be saved to; default is sorted_playlist.json", nargs="?",
                        default="sorted_playlist.json")
    # you can only sort by one field, so the following arguments are mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-da", "--date-added", help="sort by date added", action="store_true")
    group.add_argument("-dev", "--developer", help="sort by developer",  action="store_true")
    group.add_argument("-dm", "--date-modified", help="sort by date modified",  action="store_true")
    group.add_argument("-lp", "--last-played", help="sort by last played",  action="store_true")
    group.add_argument("-pl", "--platform", help="sort by platform", action="store_true")
    group.add_argument("-pt", "--playtime", help="sort by playtime",  action="store_true")
    group.add_argument("-pu", "--publisher", help="sort by publisher", action="store_true")
    group.add_argument("-rd", "--release-date", help="sort by release date", action="store_true")
    group.add_argument("-s", "--series", help="sort by series",  action="store_true")
    group.add_argument("-t", "--title", help="sort by title", action="store_true")
    group.add_argument("-r", "--random", help="random sort", action="store_true")
    # finally, specify if you want to sort in descending order
    parser.add_argument("-desc", "--descending", help="sort in descending order", action="store_true")
    args = parser.parse_args()
    return args


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    elif os.path.splitext(arg)[-1] != ".json":
        parser.error("The file %s is not in JSON format!" % arg)
    else:
        return arg


def get_field_to_sort(args):
    if args.date_added:
        field = "dateAdded"
    elif args.developer:
        field = "developer"
    elif args.date_modified:
        field = "dateModified"
    elif args.last_played:
        field = "lastPlayed"
    elif args.platform:
        field = "platformName"
    elif args.playtime:
        field = "playtime"
    elif args.publisher:
        field = "publisher"
    elif args.release_date:
        field = "releaseDate"
    elif args.series:
        field = "series"
    elif args.title:
        field = "title"
    elif args.random:
        field = "random"
    # by default, the sorting field is "title"
    else:
        field = "title"
    return field


def get_playlist(input_file):
    f = open(input_file)
    # load playlist into a dictionary    
    playlist = json.load(f)
    f.close()
    return playlist


def get_games(playlist):
    # extract games from the playlist, obtaining a list of dictionaries, one for each game
    games = playlist["games"]
    return games


def get_db_cursor():
    # initialize connection to the database
    if not os.path.isfile("flashpoint.sqlite"):
        print("Error: please provide the database file")
        sys.exit()
    global con
    con = sqlite3.connect("flashpoint.sqlite")
    cur = con.cursor()
    return cur


def replace_playlist_id(playlist, cur):
    # create a new id for the new, sorted playlist
    id = str(uuid.uuid4())
    playlist["id"] = id
    return playlist


def get_games_info(games, cur, field):
    # for each game, get the value for the corresponding field of interest and add that information to the game's dictionary
    for game in games:
        res = cur.execute("SELECT %s FROM game WHERE id = '%s' " % (field, game["gameId"]))
        try:
            value = res.fetchall()[0][0]
        # if the id could not be found, it means the playlist contains a game without an associated id
        # that game won"t show up anyway in Flashpoint, so it is given a dummy value for the field
        except IndexError:
            value = ""
        game[field] = value
    return games


def save_playlist(playlist, games, field, output_file, descending):
    games = rearrange(games, field, descending)
    # copy the sorted games list into a new, sorted playlist
    playlist["games"] = games
    # update playlist's title
    if field == "random":
        playlist["title"] = playlist["title"].split(" - Sorted by")[0] + " - Randomized"
    else:
        playlist["title"] = playlist["title"].split(" - Sorted by")[0] + " - Sorted by " + clean(field)
        if descending:
            playlist["title"] = playlist["title"] + " (Descending)"
    # save the sorted playlist in a new file
    with open(output_file, "w") as f:
        json.dump(playlist, f, indent=4)


def rearrange(games, field, descending):
    # sort the games in the playlist
    sorted_games = sort(games, field, descending)
    # update the games' "order" values in the playlist
    ordered_games = update_game_order(sorted_games)
    return ordered_games


def sort(games, field, descending):
    # sort list of dictionaries by value
    if field != "random":
        if descending:
            sorted_games = sorted(games, key=lambda game: remove_initial_articles(game[field]), reverse=True)
        else:
            sorted_games = sorted(games, key=lambda game: remove_initial_articles(game[field]))
        # remove values, as they are no longer necessary
        for game in sorted_games:
            del game[field]
        return sorted_games
    else:
        random.shuffle(games)
        return games


def remove_initial_articles(value):

    # ignore leading definite and indefinite articles ("the", "a", and "an" when alphabetizing)
    # in the regular expression, "^" ensures that they are found at the beginning of the string,
    # while the trailing space ensures that they are not the first letters of another word (e.g. thermal)
    
    if not isinstance(value, int):
        value = value.lower()
        replacements = [
            (r"^the ", ""),
            (r"^a ", ""),
            (r"^an ", "")
        ]
        for old, new in replacements:
            value = re.sub(old, new, value)
    return value


def update_game_order(games):
    # update games' order in the playlist
    counter = 0
    for game in games:
        game["order"] = counter
        counter = counter + 1
    return games


def clean(field):
    # cleans field name (e.g. dateAdded becomes Date Added)
    matches = re.search("([A-Z])", field)
    if matches:
        capital_letter = matches.groups(1)[0]
        field = field.replace(capital_letter, " " + capital_letter)
    field = field[0].capitalize() + field[1:]
    return field 


if __name__ == "__main__":
    main()
