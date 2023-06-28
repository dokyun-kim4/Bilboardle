"""
Website for playing Bilboardle
"""
from flask import Flask, render_template, redirect, request
from songs import song,get_bilboard,compile_songinfo

app = Flask(__name__)

songlist = compile_songinfo(get_bilboard())
song_names = [entry.title for entry in songlist]


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/bilboardle')
def game():
    return render_template("game.html", songs = song_names)
  

if __name__ == '__main__':
    app.run(debug=True)