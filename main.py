"""
Website for playing Bilboardle
"""
from flask import Flask, render_template, request, jsonify
from songs import compare_song, song_from_name,load_songlist
import random

app = Flask(__name__)

#Load songs
songlist = load_songlist()


# pick a random song object
answer_song = random.choice(songlist)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/bilboardle')
def game():
    song_names = [entry.title for entry in songlist]
    return render_template("game.html", names = song_names)

# -------------- PLAYLIST MODE ----------------- #
@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

@app.route('/playlist-game')
def playlist_game():
    return render_template('playlist_game.html')

# ---------------------------------------------- #

@app.route("/check_guess", methods=["POST"])
def check_guess():
    data = request.get_json()
    title = str(data.get("guess"))  # Convert the guess to a string for comparison
    
    user_guess = song_from_name(query=title,songlist=songlist)
    
    result = compare_song(guess=user_guess,answer=answer_song)
    print(result)

    # Return the JSON response
    response = {"result": result}
    return jsonify(response)




if __name__ == '__main__':
    app.run(debug=False)