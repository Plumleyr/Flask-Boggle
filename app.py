from flask import Flask, session, render_template, request, redirect, url_for, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'BOGGLEz'

toolbar = DebugToolbarExtension(app)

@app.route('/')
def get_start_game_form():
    if request.method == 'POST':
        boggle_game = Boggle()
        new_board = boggle_game.make_board()
        session['board'] = new_board
        return redirect(url_for('show_board'))
    return render_template('start_game.html')

@app.route('/boggle', methods = ['POST'])
def show_board():
    if request.is_json:
        data = request.json
        word = data.get('word')
        print(word)
        
    return render_template('jinja.html')

