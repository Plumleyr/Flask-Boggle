from flask import Flask, session, render_template, request, redirect, url_for, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'BOGGLEz'

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

# before load makes a high score and games played session variable to keep track of times played and your best score

@app.before_first_request
def before_first_request():
    session['high_score'] = 0
    session['games_played'] = 0

# loads the starting game template and makes a guessed words session list to keep track of the words you have already guessed

@app.route('/')
def get_start_game_form():
    session['guessed_words'] = []
    return render_template('start_game.html')

# creates a new board through the boggle class make board function. Sets the new board to a board session variable and then loads the boggle game template

@app.route('/boggle', methods = ['GET','POST'])
def show_board():
    if request.method == 'POST':
        new_board = boggle_game.make_board()
        session['board'] = new_board
        return render_template('jinja.html')

# gets the json post data for the word value being sent through the input on the board html and checks it to make sure it is a word
# within our words list. It then makes sure that the word has not already been guess by checking if its in our guessed words list or not.
# finally we return the json data of our response variable with the key as result. 

@app.route('/check_word', methods = ['GET', 'POST'])
def find_word():
    word = request.json.get('word')
    response = boggle_game.check_valid_word(session['board'], word)
    if(word not in session['guessed_words']):
        guessed_words = session['guessed_words']
        guessed_words.append(word)
        session['guessed_words'] = guessed_words
    return jsonify({'result': response})

# gets the timer value and updates it every 1000 ms through the front end post request.

@app.route('/update_timer', methods = ['POST'])
def start_timer():
    timer = request.json.get('timer')
    return jsonify({'timer' : timer})

# is an axios get request from the front end to get our sessions guessed words list.

@app.route('/get_guessed_words', methods=['GET'])
def get_guessed_words():
    guessed_words = session.get('guessed_words')
    return jsonify({'guessed_words': guessed_words})

# after the timer hits 0 on our front end checks to see if score is higher than our highest score on the front end and updates the value if true.
# Then it adds one to our games played var since we finished a game.

@app.route('/game_finished', methods=['POST'])
def update_stats():
    score = request.json.get('score')
    if(score > session['high_score']):
        session['high_score'] = score
    session['games_played'] += 1
    return jsonify({'score' : score})

