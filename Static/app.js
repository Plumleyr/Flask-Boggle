$(document).ready(function(){
    $form = $('#boggle_board');
    $form.submit(async function(evt){
        evt.preventDefault();
        let wordValue = $('#word_input').val();
        const res = await axios.post('/check_word', { word: wordValue });
        console.log(res);
        wordValue = '';
    });
});