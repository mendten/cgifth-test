document.addEventListener('DOMContentLoaded', function() {

    // document.querySelectorAll('.checklist').forEach(table => {
    //     table.style.display = 'none';
    // });

    // // add event listeners to the bunk and class selectors
    // document.querySelector('#bunk-selector').onchange = function() {show_table(`bunk-${this.value}`)};


    document.querySelectorAll('.bunk-week-selector').forEach(selector => {
        selector.addEventListener('change', function() {
            show_table();
        });
    });

    show_table();
});


function show_table() {
    bunk = document.querySelector('#bunk-selector').value;
    week = document.querySelector('#week-selector').value;
    
    document.querySelectorAll('.bunk-view').forEach(table => {
        table.style.display = 'none';
    });
    document.querySelectorAll('.week-view').forEach(table => {
        table.style.display = 'none';
    });
    
    bunk_to_display = document.querySelector(`#bunk-${bunk}`)
    bunk_to_display.style.display = 'block';
    week_to_display = bunk_to_display.querySelector(`.week-${week}`)
    week_to_display.style.display = 'block';
}