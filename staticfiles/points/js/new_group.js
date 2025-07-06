document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#group-type').onchange = () => show_view(document.querySelector('#group-type').value)

    show_view(document.querySelector('#group-type').value);

});


function show_view(group_type) {

    document.querySelectorAll('.if').forEach(element => {
        element.style.display = 'none';
    });
    
    document.querySelectorAll(`.if-${group_type}`).forEach(element => {
        element.style.display = 'block';
    })

}