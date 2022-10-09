# <u>`PicAsso`</u>: `Picture Assorting Assistant`

A side-project I've been working on that loosely organizea images by their dominant color.

I tried multiple methods to sort the images into color clusters, mainly trying to use some AI skills I'd learned, including:

* `Hill Climbing with Random Restarts`
* `Expansive Sorting with Hill Climbing Touch Ups`
* `Genetic Algorithms` (no longer included)

At the moment the code is configured to run Expansive Sorting as I was most please with those results. The original intention with the program was to create a collage of my favorite albums, but it can be used on any set of images.

## <u>Running `PicAsso`</u>

To run PicAsso, set up a directory on the same level as this README named `images_main` that contains the images to be sorted and a `config.py` file with the following constants:

* `CLIENT`: The client token of an application made through Spotify for Developers
* `CLIENT_SECRET`: The corresponding secret token
* `REDIRECT_URI`: The redirect uri setup for the app on the Spotify for Developers page
* `SAMPLE_SIZE`: Size of sample taken from liked songs if you choose to use the sampling line in `main.py`
* `ROWS`: Set to None by default but can be adjusted if a specific number of rows is desired.
*`COLUMNS`: Set to None by default but can be adjusted if a specfic number of columns is desired.

To run PicAsso perform the following command:

`python3 main.py <hill_climbing_flag> <runtime>`

Where `hill_climbing_flag` is only set if you want to run using solely hill climbing for `runtime` number of seconds. The hill climbing flag can be any form of h, hill,hillclimb, or hillclimbing, regardless of case.

## <u>Spotify Integration</u>

PicAsso is intended to be used when downloading album art from one's Spotify liked songs and/or a Spotify playlist.

If the set of images is not going to be downloaded from Spotify, they must simply be placed in the aforementioned `images_main` directory.

To download the images run:

`python3 spotify.py <playlist_flag> <playlist_id>`

Where `playlist_flag` is only set if you are downloading from a playlist instead of a user's liked songs. The `playlist_id` is the Spotify id of the playlist, which can be found following these [instructions](https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html#:~:text=To%20find%20the%20Spotify%20playlist,Link%22%20under%20the%20Share%20menu.&text=The%20playlist%20id%20is%20the,after%20playlist%2F%20as%20marked%20above.). Similarly to the hillclimbing flag, the playlist flag can be any form of p, play, or playlist, regardless of case.