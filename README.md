# **<u>`PicAsso`</u>: `Picture-Assorting Assistant`**

A side-project I've been working on that loosely organize images by their dominant color, either into a collage, or into a given reference image, making each pixel of the reference out of an image from the provided set.
___
## **<u>Running `PicAsso`</u>**

To run PicAsso, fill the directory `images_main` with images to be sorted and create a `config.py` on in the same directory as this `README.md` file with the following constants:

* `CLIENT`: The client token of an application made through Spotify for Developers
* `CLIENT_SECRET`: The corresponding secret token
* `REDIRECT_URI`: The redirect uri setup for the app on the Spotify for Developers page
* `SAMPLE_SIZE`: Size of sample taken from liked songs if you choose to use the sampling line in `main.py`
* `ROWS`: Set to None by default but can be adjusted if a specific number of rows is desired.
* `COLUMNS`: Set to None by default but can be adjusted if a specfic number of columns is desired.

There are 2 different modes PicAsso can run in, each having it's own script.

### <u>Pixelizing a Reference</u>

This mode will recreate a reference image using the images from `/images_main` as pixels. To run first create a file named `reference_picture.jpeg` in the same directory as this `README.md` and run the following command:

`python3 pixel.py`

The pixelized image will be saved as `pixeled.jpeg`.

### <u>Color Sorting a Collage</u>

This mode creates a rectangular collage of the images provided in `/images_main` and attempts to sort them by color.

By default this mode will run expansive sorting with touchup hillclimbing since it has the best performance. To create a collage run:

`python3 collage.py`

The collage will be saved as `collage.jpeg`.

If you wish to run this mode using solely hill climbing, run:

`python3 collage.py <hill_climbing_flag> <runtime>`

Where `hill_climbing_flag` is only set if you want to run using solely hill climbing for `runtime` number of seconds. The `hill_climbing_flag` can be any form of h, hill, hillclimb, or hillclimbing, regardless of case.

___
## **<u>Spotify Integration</u>**

PicAsso is intended to be used when downloading album art from one's Spotify liked songs and/or a Spotify playlist.

If the set of images is not going to be downloaded from Spotify, they must simply be placed in the aforementioned `images_main` directory.

To download the images run:

`python3 spotify.py`

 If you are downloading from a playlist instead of a user's liked songs, run:

`python3 spotify.py <playlist_flag> <playlist_id>`

Similarly to the hillclimbing flag, the playlist flag can be any form of p, play, or playlist, regardless of case. The `playlist_id` is the Spotify id of the playlist, which can be found following these [instructions](https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html#:~:text=To%20find%20the%20Spotify%20playlist,Link%22%20under%20the%20Share%20menu.&text=The%20playlist%20id%20is%20the,after%20playlist%2F%20as%20marked%20above.).
___
## **<u>Nerdy Technical Stuff</u>**
I tried multiple methods to sort the images into color clusters, mainly trying to use some AI skills I'd learned, including:

* `Hill Climbing with Random Restarts`
* `Expansive Sorting with Hill Climbing Touch Ups`
* `Genetic Algorithms` (no longer included)

At the moment the code is configured to run Expansive Sorting as I was most please with those results. The original intention with the program was to create a collage of my favorite albums, but it can be used on any set of images.

The comparisons of the images is done using each images dominant color. The dominant color is saved as an RGB 3-tuple and the "difference" between two images is defined as the sum of the differences of each distinct value in the two RGB 3-tuples:

`sum([abs(rgb1[color] - rgb2[color]) for color in rgb_tuple])`

In order to save time, the initial determining of image's dominant colors is done through threading, spanwing a unique thread for each image that determines its dominant color and save the RGB 3-tuple before terminating.
___
## *<u>Dependencies</u>**

PicAsso relies on the following dependecies:

* `numpy`
* `from PIL: Image`
* `scipy.cluster`
* `scipy.misc`
* `scipy`
* `spotifpy`
* `spotipy.oauth2`
* `requests`
* `json`

* `Python Standard Library`