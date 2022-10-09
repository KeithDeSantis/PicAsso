# PicAsso: `Picture Assorting Assistant`

A side-project I've been working on that loosely organizea images by their dominant color.

I tried multiple methods to sort the images into color clusters, mainly trying to use some AI skills I'd learned, including:

* `Genetic Algorithms` (no longer included)
* `Hill Climbing with Random Restarts`
* `Expansive Sorting`

At the moment the code is configured to run Expansive Sorting as I was most please with those results. The original intention with the program was to create a collage of my favorite albums, but it can be used on any set of images.

Has capabilites to download album art of all of a user's liked songs, given a `config.py` file is provided with the following constants:

* `CLIENT`: The client token of an application made through Spotify for Developers
* `CLIENT_SECRET`: The corresponding secret token
* `REDIRECT_URI`: The redirect uri setup for the app on the Spotify for Developers page
* `NUMBER_OF_LIKED_SONGS`: The number of liked songs for the given user
* `SAMPLE_SIZE`: Size of sample taken from liked songs if you choose to uncomment the sampling line in `main.py`
* `ROOMIE_LIST_ID`: A temporary variable used to store a playlist ID for in progress playlist compatibility