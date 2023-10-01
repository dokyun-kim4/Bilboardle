"""
Website for playing Bilboardle
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from songs import compare_song, song_from_name,load_songlist, load_playlist
import random

app = Flask(__name__)

#Load songs
songlist = load_songlist()


# pick a random song object
answer_song = random.choice(songlist)
print(answer_song)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/bilboardle')
def game():
    song_names = [entry.title for entry in songlist]
    return render_template("game.html", names = song_names)

# -------------- PLAYLIST MODE ----------------- #
@app.route('/playlist',methods = ['GET','POST'])
def playlist():
    if request.method=='POST':
        link = request.form['id']
        id = link.split('https://open.spotify.com/playlist/')[1].split('?')[0]

        return redirect(url_for('playlist_game',id=id))
    return render_template('playlist.html')

@app.route('/playlist-game/<id>')
def playlist_game(id):
    global songlist
    songlist = load_playlist(id)
    global answer_song
    answer_song = random.choice(songlist)
    print(answer_song)
    
    song_names = [entry.title for entry in songlist]
    return render_template('playlist_game.html',names=song_names)

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
    app.run(debug=True)