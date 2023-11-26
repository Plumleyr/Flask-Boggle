from flask import Flask, session, render_template, request, redirect, url_for, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'BOGGLEz'

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def get_start_game_form():
    return render_template('start_game.html')

@app.route('/boggle', methods = ['POST', 'GET'])
def show_board():
    if request.method == 'GET':
        new_board = boggle_game.make_board()
        session['board'] = new_board
        return render_template('jinja.html')

@app.route('/check_word', methods = ['GET', 'POST'])
def find_word():
    print(request.json)
    word = request.json.get('word')
    result = boggle_game.check_valid_word(session['board'], word)
    return jsonify({'response': result})

