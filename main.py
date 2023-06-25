"""
Website for playing Bilboardle
"""
from flask import Flask, render_template, redirect, request
from songs import get_bilboard

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/bilboardle')
def game():
    return render_template("game.html", songs = get_bilboard())
  

if __name__ == '__main__':
    app.run(debug=True)