document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.checklist').forEach(table => {
        table.style.display = 'none';
    });

    // add functionality to the bunk-class-toggle button
    document.querySelector('#bunk-class-toggler').onclick = function() {
        document.querySelectorAll('.list').forEach(list => {
            if (list.style.display === 'none') {
                list.style.display = 'block';
            } else {
                list.style.display = 'none';
            }
        });
    }

    // by default, hide the class list
    document.querySelector('#class-header').style.display = 'none';

    if (document.querySelector('#fcl')) {
        document.querySelector('#fcl').style.display = 'none';
    }

    // add event listeners to the bunk and class selectors
    document.querySelector('#bunk-selector').onchange = function() {show_table(`bunk-${this.value}`)};
    document.querySelector('#class-selector').onchange = function() {show_table(`lc-${this.value}`)};
    
    // add event listeners to the bunk and class selectors
    document.querySelector('#bunk-selector').addEventListener('change', 
        () => set_id(`bunk-${document.querySelector('#bunk-selector').value}`));
    document.querySelector('#class-selector').addEventListener('change',
        () => set_id(`lc-${document.querySelector('#class-selector').value}`));

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


function set_id(table_name) {

    // get the first 2 letters of the table name
    let table_type = table_name.slice(0, 2);
    document.querySelector(`#${table_type}`).value = table_name;
}