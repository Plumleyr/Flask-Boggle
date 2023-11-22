from flask import Flask, session, render_template, request, redirect, url_for, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'BOGGLEz'

toolbar = DebugToolbarExtension(app)

@app.route('/')
def get_start_game_form():
    return render_template('start_game.html')

@app.route('/boggle', methods = ['GET', 'POST'])
def show_board():
    if request.method == 'POST':
        print(request.form.get('word'))

    boggle_game = Boggle()
    new_board = boggle_game.make_board()
    session['board'] = new_board
    return render_template('jinja.html')
