from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_start_game(self):
        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertIn('<button>Boggle!</button>', html)
            self.assertEqual(session['guessed_words'], [])

    def test_show_board(self):
        with self.client as client:
            resp = client.post('/boggle')
            self.assertTrue('board' in session)
            self.assertIsNotNone(session['board'])
    
    def test_find_word(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['board']=[['A', 'B', 'C', 'D', 'E'],
                                 ['F', 'G', 'H', 'I', 'J'],
                                 ['K', 'L', 'M', 'N', 'O'],
                                 ['P', 'Q', 'R', 'S', 'T'],
                                 ['U', 'V', 'W', 'X', 'Y']]
                response = self.client.post('/check_word', json={
                    'word':'DIM'
                })
                self.assertEqual(response.json['result'], 'ok')
    
    def test_start_timer(self):
        with self.client as client:
            response = self.client.post('/update_timer', json={
                'timer' : 60
            })
            self.assertEqual(response.json['timer'], 60)

    def test_update_stats(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['high_score'] = 3
                session['games_played'] = 0
                response = self.client.post('/game_finished', json={
                    'score': 12
                })
                self.assertEqual(session['high_score'], 12)
                self.assertEqual(session['games_played'], 1)

