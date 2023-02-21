![Socialify](https://github.com/giovanni-cutri/flashpoint-playlist-sorter/blob/main/images/socialify.png)

# flashpoint-playlist-sorter
 A simple tool to sort [Flashpoint](https://bluemaxima.org/flashpoint/) playlists by your field of choice.

## Setting up

- Download the *flashpoint.py* file and place it in any folder.
- Inside that same folder, you will need to copy two files:
    - The playlist you want to sort, in JSON format (which is the default export format for Flashpoint);
     - The *flashpoint.sqlite* file, which you can find in your local Flashpoint copy, inside the *Data* folder.

## Usage

```
python flashpoint.py [OPTIONS]...
```

By default, the program will assume that the playlist to sort is inside a file called *playlist.json* and will output the sorted playlist in a file called *sorted_playlist.json*.

You can modify this behaviour by passing the following arguments:

```
-h, --help                         show this help message and exit
-i [INPUT], --input [INPUT]        the input file which contains the playlist you want to sort in JSON format; default is playlist.json                                 
-o [OUTPUT], --output [OUTPUT]     the output file which is where the sorted playlist will be saved to; default is sorted_playlist.json 
-da, --date-added                  sort by date added
-dev, --developer                  sort by developer
-dm, --date-modified               sort by date modified
-pl, --platform                    sort by platform
-pu, --publisher                   sort by publisher
-s, --series                       sort by series
-t, --title                        sort by title
-desc, --descending                sort by descending order
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/flashpoint-playlist-sorter/blob/main/LICENSE) file for details.
