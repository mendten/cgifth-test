document.addEventListener("DOMContentLoaded", function(event) {

    const max_bonus = document.querySelector('#max-bonus').dataset.num

    document.querySelectorAll('.day-selector').forEach(btn => {
        // if buttons date is tomorow or later, disable it
        if (new Date(btn.dataset.day) <= new Date()) {
            btn.onclick = () => show_chart(btn.dataset.day)
        } else {
            btn.classList.add('disabled');
        }
    });

    document.querySelectorAll('input, select').forEach(input => {
        input.onchange = () => update(input);
    });

    document.querySelectorAll('[type="tel"]').forEach(input => {
        // if input is greater than max bonus, set it to max bonus
        input.onkeyup = () => {
            if (parseInt(input.value) > max_bonus) {
                input.value = max_bonus;
            }
            update(input);}
    });

    document.querySelectorAll('.auto-fire').forEach(div => {

        if (div.querySelector('[type="checkbox"]')) {
            update(div.querySelector('input'))
        } else {
            update(div.querySelector('select'))
        }
    });

    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.onclick = () => {
            if (confirm('Are you sure you want to save these points?')) {
                // get the form 
                let form = btn.closest('form');
                let div_elem = form.closest('.daily-chart')
                // if we are connected to the internet, submit the form
                if (navigator.onLine) {
                    // submit the form
                    form.submit();
                // if we are not connected to the internet, save the form to local storage
                } else {
                    // get the form's id
                    let id = form.id;
                    // get the form's data
                    let data = new FormData(form);
                    // convert the data to a javascript object
                    data = Object.fromEntries(data);

                    // create an array for the campers
                    data['camper'] = [];
                    // get all the campers in the form
                    let campers = form.querySelectorAll('[name="camper"]');
                    // add the campers to the data
                    campers.forEach(camper => {
                        // add campers id to 'camper' key in data
                        data['camper'].push(camper.value);
                    });
                    // save the data to local storage
                    localStorage.setItem(id, JSON.stringify(data));
                    // display a message to the user
                    alert('Points saved to local storage.');
                }
                // update the html in cache so if the user refreshes the page, they will see the points they just saved
                // first we need to open the cache. We can just use startswith('django-pwa') because we know that is the name of the cache
                caches.keys().then(cacheNames => {
                    cacheNames
                        .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                        .forEach(cacheName => {
                            caches.open(cacheName).then(cache => {
                                // get the html from the cache
                                cache.match('/staff').then(response => {
                                    // get the html as a document
                                    response.text().then(html => {
                                        // create a new document
                                        let doc = new DOMParser().parseFromString(html, 'text/html');
                                        // get the div for this day
                                        let div = doc.getElementById(div_elem.id);
                                        // replace the div with the new div
                                        div.outerHTML = div_elem.outerHTML;

                                    // save the new html to the cache
                                    cache.put('/staff', new Response(doc.documentElement.outerHTML, { headers: { 'Content-Type': 'text/html' } }));
                                    });                                 
                                });
                            });
                        });
                });
            }
        }
    });

    today = new Date();

    // if last_week is in the URL, get yesterdays date
    if (window.location.href.includes('last_week')) {
        today.setDate(today.getDate() - 1);
    }

    // if the url contains 'day=', show the chart for that day
    if (window.location.href.includes('day=')) {
        let day = window.location.href.split('day=')[1];
        // increase the day by 1 because the url format causes the day to be off by 1
        day = new Date(day);
        day.setDate(day.getDate() + 1);
        day = day.toISOString().split('T')[0];
        show_chart(day);
    } else {
        show_chart(today);
    }

    if (document.querySelector('#staff-logout')) {
        document.querySelector('#staff-logout').onclick = () => {
            // clear the service worker cache
            caches.keys().then(cacheNames => {
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .forEach(cacheName => {
                        caches.delete(cacheName);
                    });
            });
            // uninstall service worker
            navigator.serviceWorker.getRegistrations().then(function(registrations) {
                for(let registration of registrations) {
                    registration.unregister()
                }
            });
        }
    }
});


function show_chart(day) {

    // convert day to a date object
    day = new Date(day).toDateString();

    document.querySelectorAll('.daily-chart').forEach(div => {
        div.style.display = 'none';
        div_day = new Date(div.id).toDateString();
        if (div_day == day) {
            div.style.display = 'block';
        }
    });

    document.querySelectorAll('.day-selector').forEach(btn => {
        btn.classList.remove('active');
        btn_day = new Date(btn.dataset.day).toDateString();
        if (btn_day == day) {
            btn.classList.add('active');
        }
    });
}

function update(input) {

    // get parent table
    let table = input.closest('table');

    // get camper and day from input
    let camper = input.dataset.camper;
    let day = table.dataset.day;

    // get the totals box
    let total_elem = document.getElementById(`camper-${camper}-${day}-total`);
    
    // create a blank points list and a total
    let points_list = '';
    let total = 0;

    // loop through all the inputs in the table for this camper and day
    table.querySelectorAll(`[data-camper="${camper}"]`).forEach(point => {
        console.log(point.nodeName)
        // first check if it's the bonus input
        if (point.dataset.task == 'bonus') {
            // if it's empty, set it to 0
            if (point.value == '') {
                point.value = 0;
            } else {
                // if it's not empty, make sure it's a number
                point.value = parseInt(point.value);
                point.setAttribute('value', point.value)
            }
            // add the value to the points list and total
            total += parseInt(point.value);
        // if it's not the bonus input, check if it's checked off
        } else if (point.checked == true) {
            // add the value to the points list and total
            total += parseInt(point.value);
            // add checked to the inputs html so it will be checked when the page is refreshed
            point.setAttribute('checked', '');
        // if it's not checked off, add a 0 to the points list
        } else if (point.nodeName == 'SELECT') {
            console.log(`this is a selection box ${point.value}`)
            total += parseInt(point.value);
        }
    });

    // set the total element's innerHTML to the total
    total_elem.innerHTML = total;

}


// check if the user is connected to the internet
window.addEventListener('online',  () => {
    console.log('online')
    // make sure we are actually online
    if (navigator.onLine) {
        // if there are any forms saved to local storage, submit them
        for (let i = 0; i < localStorage.length; i++) {
            // get the form from local storage
            let form = JSON.parse(localStorage.getItem(localStorage.key(i)));
            console.log(`attempting to submit ${form.day}`)

            fetch('/offline_forms', {
                method: 'POST',
                body: JSON.stringify(form),
                headers: {
                    'Host': 'cgifth.herokuapp.com',
                    'Origin': 'https://cgifth.herokuapp.com',
                }
            })
            // let the user know that the form was submitted
            .then(response => {
                if (response.status == 200) {
                    console.log(`Checklist submitted for ${form.day}`);
                }
            })
        }
        // clear local storage
        localStorage.clear();
    }
});