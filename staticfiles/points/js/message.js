document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#to').onchange = function() {
        if (this.value === 'specific') {
            document.querySelector('#specific-view').style.display = 'block';
        } else {
            document.querySelector('#specific-view').style.display = 'none';
        }
    }

    document.querySelectorAll('.btn-act').forEach(btn => {
        btn.onclick = function() {
            let form = btn.parentElement
            if (confirm('Are you sure you want to delete this message?')) {
                form.submit()
            }
        }
    });

});