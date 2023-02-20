import sys
import json
import os
import uuid
import sqlite3


def main():
    playlist = get_playlist()
    games = get_games(playlist)
    db_cursor = get_db_cursor()
    new_playlist = replace_playlist_id(playlist, db_cursor)
    games_info = get_games_info(games, new_playlist["id"],  db_cursor)
    # close connection to database
    con.close()
    save_playlist(new_playlist, games_info)


def get_playlist():
    try:
        f = open("playlist.json")
    except OSError:
        print("Error: please provide the playlist's file")
        sys.exit()
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
    # get existing playlists' id
    res = cur.execute("SELECT id FROM playlist")
    existing_ids = []
    for i in res.fetchall():
        existing_ids.append(i[0])
    # create a new id for the new, sorted playlist, ensuring that it is not a duplicate
    while 1:
        id = str(uuid.uuid4())
        if id not in existing_ids:
            break
    playlist["id"] = id
    return playlist


def get_games_info(games, id, cur):
    # for each game, get the corresponding title and add that information to the game's dictionary
    for game in games:
        game["playlistId"] = id
        res = cur.execute("SELECT title FROM game WHERE id = '%s' " % game["gameId"])
        try:
            title = res.fetchall()[0][0]
        # if the id could not be found, it means the playlist contains a game without an associated id
        # that game won't show up anyway in Flashpoint, so it is given a dummy title.
        except IndexError:
            title = ""
        game["title"] = title
    return games


def save_playlist(playlist, games):
    games = clean(games)
    # copy the sorted games list into a new, sorted playlist
    playlist["games"] = games
    # save the sorted playlist in a new file
    with open("sorted_playlist.json", "w") as f:
        json.dump(playlist, f, indent=4)


def clean(games):
    sorted_games = sort(games)
    ordered_games = update_game_order(sorted_games)
    return ordered_games


def sort(games):
    # sort list of dictionaries by title
    sorted_games = sorted(games, key = lambda game: (game["title"].lower()))
    # remove titles, as they are no longer necessary
    for game in sorted_games:
        del game["title"]
    return sorted_games


def update_game_order(games):
    # update games' order in the playlist
    counter = 0
    for game in games:
        game["order"] = counter
        counter = counter + 1
    return games


if __name__ == "__main__":
    main()

# TODO: sort by [field]
# TODO: add other fields
