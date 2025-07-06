document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.checklist').forEach(table => {
        table.style.display = 'none';
    });

    // add event listeners to the bunk and class selectors
    document.querySelector('#bunk-selector').onchange = function() {show_table(`bunk-${this.value}`)};

});

function show_table(table_name) {
    document.querySelectorAll('.checklist').forEach(table => {
        table.style.display = 'none';
    });
    document.querySelector(`#${table_name}`).style.display = 'block';

    if (document.querySelector('#group-id')) {
        document.querySelector('#group-id').value = table_name;
    }
}