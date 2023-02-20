import sys
import json
import os
import uuid
import sqlite3

# load playlist into a dictionary
try:
    f = open("playlist.json")
except OSError:
    print("Error: please provide the playlist's file")
    sys.exit()
playlist = json.load(f)
f.close()

# extract games from the playlist, obtaining a list of dictionaries, one for each game
games = playlist["games"]

# initialize connection to the database
if not os.path.isfile("flashpoint.sqlite"):
    print("Error: please provide the database file")
    sys.exit()
con = sqlite3.connect("flashpoint.sqlite")
cur = con.cursor()

# get existing playlists' id
res = cur.execute("SELECT id FROM playlist")
existing_ids = []
for i in res.fetchall():
    existing_ids.append(i[0])

# create a new id for the new sorted playlist, ensuring that it is not a duplicate
while 1:
    id = str(uuid.uuid4())
    if id not in existing_ids:
        break
playlist["id"] = id

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



# TODO: sort by [field]
# TODO: add other fields
