document.addEventListener('DOMContentLoaded', function() {

    let current = document.querySelector('#current');
    
    document.querySelectorAll('.week-option').forEach(option => {
        console.log(option)
        if (option.innerHTML == (parseInt(current.value) - 1)) {
            option.selected = true;
        }
    });
    
    let send = document.querySelector('#send-button');

    document.querySelector('#password').onkeyup = function() {
        if (password.value != '') {
            send.disabled = false;
            send.classList.remove('btn-secondary');
            send.classList.add('btn-primary');
            send.setAttribute('type', 'submit');
            
        } else {
            send.disabled = true;
            send.classList.remove('btn-primary');
            send.classList.add('btn-secondary');
            send.setAttribute('type', 'button');
        }
    };
});