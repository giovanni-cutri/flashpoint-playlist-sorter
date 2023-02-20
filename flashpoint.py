import json
import uuid
import sqlite3

# load playlist json in a dictionary
f = open("playlist.json")
playlist = json.load(f)
f.close()

# replace playlist's id
id = str(uuid.uuid4())
playlist["id"] = id

# extract games from the playlist, obtaining a list of dictionaries, one for each game
games = playlist["games"]

# initialize connection to the database
con = sqlite3.connect("flashpoint.sqlite")
cur = con.cursor()

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

# close connection to database
con.close()

# sort list of dictionaries by title
sorted_games = sorted(games, key = lambda game: (game["title"].lower()))

# update games' order in the list
counter = 0
for game in sorted_games:
    game["order"] = counter
    counter = counter + 1

# copy the sorted games list into a new, sorted playlist
sorted_playlist = playlist
sorted_playlist["games"] = sorted_games

# remove titles
for game in sorted_playlist["games"]:
    del game["title"]

# save the sorted playlist in a new file
with open("sorted_playlist.json", "w") as f:
    json.dump(sorted_playlist, f, indent=4)



# TODO: check uuid duplicate
# TODO: sort by [field]
# TODO: add other fields
