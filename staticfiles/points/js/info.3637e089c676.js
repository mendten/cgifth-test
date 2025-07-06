document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#info-edit').style.display = 'none';

    document.querySelector('.bi').addEventListener('click', () => {
        document.querySelector('#info-view').style.display = 'none';
        document.querySelector('#info-edit').style.display = 'block';
        document.querySelector('.bi').style.display = 'none';
    })

    const button = document.querySelector('#save')
    button.addEventListener('click', () => {
        check_ranks_inputs(button)
    })

    document.querySelector('#cancel').addEventListener('click', () => {
        document.querySelector('#info-view').style.display = 'inline-block';
        document.querySelector('#info-edit').style.display = 'none';
        document.querySelector('.bi').style.display = 'block';
    })

    document.querySelector('#add-rank').addEventListener('click', () => {
        add_rank()
    })

});


function add_rank() {
    const rank_input = document.getElementById('new-rank-template');
    const new_ranks_div = document.getElementById('new-ranks');

    const new_rank = document.createElement('span');
    new_rank.innerHTML = rank_input.innerHTML;
    new_ranks_div.appendChild(new_rank);
}


function check_ranks_inputs(button) {
    // This function reviews each ranks line and ensures that the inputs are valid. If any of them are not, inform the user that we will not create the rank.
    // get all inputs that are in the div called 'new-ranks'
    let inputs = document.querySelectorAll('#new-ranks input');

    let valid = true;
    let message = 'Some of your ranks are missing titles or points. Please fill them in before saving. If any rank is missing a Title, "From" value, or "To" value, we will not that rank.';

    inputs.forEach(input => {
        if (input.value === '') {
            valid = false;
        }
    })
    if (valid) {
        console.log('valid form')
        button.form.submit();
    } else {
        if (confirm(message)) {
            console.log('invalid form, user is submitting anyway.')
            button.form.submit();
        }
    }
}