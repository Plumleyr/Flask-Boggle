$(document).ready(function(){
    $('#boggle_board').submit(function(evt){
        evt.preventDefault();
        let wordValue = $('#word_input').val();

        $.ajax({
            url:'/boggle',
            method:'post',
            contentType:'application/json',
            data:{
                word: wordValue
            }
        });
    });

    $('tr').on('click', function(){
        let closestTd = $(this).closest('td');
    });
})