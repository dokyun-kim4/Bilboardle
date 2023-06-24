"""
Website for playing Bilboardle
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    pass

@app.route('/bilboardle')
def game():
    pass

if __name__ == '__main__':
    app.run(debug=True)