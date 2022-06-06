from flask import Flask, jsonify

from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

@app.route('/movie/<title>')
def get_movie_by_title(title):
    return jsonify(movie_by_title(title))


@app.route('/movie/<int:year1>/to/<int:year2>')
def get_movie_between_years(year1, year2):
    return jsonify(movie_between_years(year1, year2))

@app.route('/rating/<viewers>')
def get_movie_by_rating(viewers):
    return jsonify(movie_by_rating(viewers))

app.route('/genre/<genre>')
def get_movie_by_genre(genre):
    return jsonify(movie_by_genre(genre))
app.route('/')

if __name__ == "__main__":
    app.run(debug=True)