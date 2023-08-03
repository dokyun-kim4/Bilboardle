# Bilboardle (Default gamemode)

A Worlde-like game where the user tries to guess a song from the top 100 Bilboard chart  

# Playlist mode (In progress)

Using a custom spotify playlist, the user tries to guess a song from the playlist.  

## Spotify API
To run this game locally, you need to sign up for a [Spotify API key](https://developer.spotify.com/documentation/web-api/tutorials/getting-started).

After following the instructions in the Spotify documentation, create a file named `.env` in the root directory with the following variables.
- ID = YOUR SPOTIFY CLIENT ID
- ID_SECRET = YOUR SPOTIFY CLIENT SECRET ID
- URI = YOUR SPOTIFY APP'S REDIRECT URI

## How to play
After making a guess, the game will display if the guessed song matches any of the following with the answer.
- Artist
- Duration
- Explicit?
- Bilboard ranking (will always be green for playlist mode)
- Release date
- Title
