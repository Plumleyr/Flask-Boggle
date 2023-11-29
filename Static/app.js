$(document).ready(function(){
$boggleForm = $('#boggle_board');
$startForm = $('#start_game');
let score = 0;
let timer;
let timerStarted = false;

// Checks to see if a timer has already been started if not will make one that updates our timer var and after the timer hits 0 will post
// to our servers game finished URL.

async function startTimer(){
    if(!timerStarted){
        timerStarted = true;
        let remainingTime = 60;
        const resp = await axios.post('/update_timer', { timer: remainingTime });
        $('.timer').text(remainingTime);
        timer =  setInterval(async () => {
            remainingTime--;
            axios.post('/update_timer', { timer: remainingTime });
            $('.timer').text(remainingTime);
            if (remainingTime == 0){
                clearInterval(timer);
                $boggleForm.hide();
                $('.msg').text(`Game is Over! You scored ${score} points`);
                const resp2 = await axios.post('/game_finished', {
                    score : score,
                });
            }
        }, 1000);
    }
}

// Gets the input value from our guess, sets everything to caps to make it case insensitive, checks our guessed words to
// set a value and compare the word later on. then posts to our check word url to check if the word is available or not.
// then goes through a series of if statements to provide the required outcome to the validation of our submitted word.
// finally it clears the input allowing users to immediately guess again.

async function getWordValue(){
    let wordValue = $('#word_input').val();
    let upperWordValue = wordValue.toUpperCase();
    const resp2 = await axios.get('/get_guessed_words');
    const guessedWords = resp2.data.guessed_words;
    const resp = await axios.post('/check_word', {word : upperWordValue});
    let result = resp.data.result;
    if(result == 'not-on-board'){
        $('.msg').text(`${upperWordValue} not on board`);
    }else if(result == 'not-word'){
        $('.msg').text(`${upperWordValue} not a word`);
    }else if(guessedWords.includes(upperWordValue)){
        $('.msg').text(`Already guessed ${upperWordValue}`);
    }else{
        $('.msg').text(`${upperWordValue} is a word on board + ${upperWordValue.length} to score`);
        score += upperWordValue.length;
        $('.score').text(`${score}`);
        $('.words-guessed').append($(`<li>${upperWordValue}</li>`));
    }
    $('#word_input').val('');
}

// starts the game with the above functions and prevents the default form submission.

function startGame(evt){
    evt.preventDefault();
    startTimer();
    getWordValue();
}

// when the first word is submitted initializes the startgame func.

$boggleForm.on('submit', startGame);
})