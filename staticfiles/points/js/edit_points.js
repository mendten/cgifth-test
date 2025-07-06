document.addEventListener('DOMContentLoaded', function() {

    // add functionality to the bunk-class-toggle button
    document.querySelector('#bunk-class-toggler').onclick = function() {
        document.querySelectorAll('.list').forEach(list => {
            if (list.style.display === 'none') {
                list.style.display = 'inline-block';
                list.querySelector('select').disabled = false;
            } else {
                list.style.display = 'none';
                list.querySelector('select').disabled = true;
            }
        });
    }

    // if there is 'id=' in the url, then search bunk and class lists for that id
    // once found, show the parent list and select the option
    if (window.location.href.includes('id=')) {
        // first, hide and disable both bunk and class lists
        document.querySelectorAll('.list').forEach(list => {
            list.style.display = 'none';
            list.querySelector('select').disabled = true;
        });
        // split the url after 'id=' and before the next '&'
        let id = window.location.href.split('id=')[1].split('&')[0];
        console.log(id)
        let group = document.querySelector(`[value="${id}"]`);
        let list = group.closest('.list');
        list.style.display = 'inline-block';
        list.querySelector('select').disabled = false;
        group.selected = true;
    } else {
        // by default, hide the class list
        document.querySelector('#class-header').style.display = 'none';
    }
    
    if (document.querySelector('#current-week')) {
        document.querySelector('#week-selector').querySelectorAll('option').forEach(option => {
            if (option.innerHTML === document.querySelector('#current-week').value) {
                option.selected = true;
            }
        });
    }

});

