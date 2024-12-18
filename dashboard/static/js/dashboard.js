function show_alert() {
    const answer = Cookies.get('answer');
    if ([null, undefined].includes(answer)) {
        return;
    }

    Cookies.remove('answer');
    alert(answer);
}

function edit_block() {
    const btn = $('.edit-block');
    const converter = $('.converter');
    const quiz = $('.quiz');

    let btn_text;

    btn.off('click').on('click', () => {
        if (converter.hasClass('d-block')) {
            converter.removeClass('d-block').addClass('d-none');
            quiz.removeClass('d-none').addClass('d-block');
    
            btn_text = 'Quiz -> Converter';
        } else {
            quiz.removeClass('d-block').addClass('d-none');
            converter.removeClass('d-none').addClass('d-block');
    
            btn_text = 'Converter -> Quiz';
        }
    })
}

$(document).ready(() => {
    $('.current-year').text(
        new Date().getFullYear()
    )

    edit_block();
    show_alert();
})