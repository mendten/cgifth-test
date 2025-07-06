document.addEventListener('DOMContentLoaded', function() {

    let current = document.querySelector('#week').value;

    document.querySelector('#week-selector').querySelector(`option[value="${current}"]`).selected = true;

    document.querySelector('#week-selector').onchange = function() {
        this.parentElement.submit();
    };

    document.querySelectorAll('.show-col').forEach(button => {  
        button.onclick = function() {
            let col = this.dataset.column;
            if (button.checked == true) {
                document.querySelectorAll(`.${col}`).forEach(cell => {
                    cell.style.display = 'table-cell';
                });
            } else {
                document.querySelectorAll(`.${col}`).forEach(cell => {
                    cell.style.display = 'none';
                });
            }
        };
    });

});