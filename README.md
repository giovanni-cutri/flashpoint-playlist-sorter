![Socialify](https://github.com/giovanni-cutri/flashpoint-playlist-sorter/blob/main/images/socialify.png)

# flashpoint-playlist-sorter
 A simple tool to sort [Flashpoint](https://bluemaxima.org/flashpoint/) playlists by the field of your choice.

## Setting up

Make sure you have Python 3 installed on your machine.

- Download the *flashpoint.py* file from this repository and place it in any folder.
- Inside that same folder, you will need to copy two files:
    - The playlist you want to sort, in JSON format (which is the default export format from the Flashpoint launcher);
     - The *flashpoint.sqlite* file, which you can find in your local Flashpoint copy, inside the *Data* folder.

## Usage

```
python flashpoint.py [OPTIONS]...
```

By default, the program will assume that the playlist to sort is inside a file called *playlist.json*, will sort it by title in ascending order and will output the sorted playlist in a file called *sorted_playlist.json*.

You can modify this behaviour by passing the following arguments:

```
-h, --help                         show this help message and exit
-i [INPUT], --input [INPUT]        the input file which contains the playlist you want to sort in JSON format; default is playlist.json                                 
-o [OUTPUT], --output [OUTPUT]     the output file which is where the sorted playlist will be saved to; default is sorted_playlist.json 
-da, --date-added                  sort by date added
-dev, --developer                  sort by developer
-dm, --date-modified               sort by date modified
-lp, --last-played                 sort by last played
-pl, --platform                    sort by platform
-pt, --playtime                    sort by playtime
-pu, --publisher                   sort by publisher
-s, --series                       sort by series
-t, --title                        sort by title
-desc, --descending                sort in descending order
-r, --random                       random sort
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/flashpoint-playlist-sorter/blob/main/LICENSE) file for details.
