document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#tasks-selector').style.display = 'none';

    document.querySelector('#stat-selector').onchange = function() {
        if (this.value == 'specific') {
            document.querySelector('#tasks-selector').style.display = 'block';
        } else {
            document.querySelector('#tasks-selector').style.display = 'none';
        }
    }
});