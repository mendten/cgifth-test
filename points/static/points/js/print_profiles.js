document.addEventListener('DOMContentLoaded', () => {
    
    const campers = document.querySelectorAll('.id-list');
    const camper_list = []
    for (let i = 0; i < campers.length; i++) {
        camper_list.push(campers[i].value);
    }

    for (let j = 0; j < camper_list.length; j++) {
        const tasks = document.querySelectorAll(`.task-${camper_list[j]}`);
        const percents = document.querySelectorAll(`.percent-${camper_list[j]}`);

        let task_list = []
        for (let i = 0; i < tasks.length; i++) {
            task_list.push(tasks[i].innerHTML);
        }

        let percent_list = []
        for (let i = 0; i < percents.length; i++) {
            percent_list.push(percents[i].innerHTML);
        }
    
        for (let i = 0; i < task_list.length; i++) {
            let canvas = document.createElement('canvas');
            canvas.setAttribute('id', task_list[i]);
            canvas.setAttribute('width', '200px');
            canvas.setAttribute('height', '200px');
            canvas.style.width = '200px';
            canvas.style.height = '200px';
            canvas.style.display = 'inline-block';
            new Chart(canvas, {
                type: 'pie',
                data: {
                    labels: [`Percentage earned for ${task_list[i]}`, 'Remainder (did not earn)'],
                    datasets: [{
                        label: task_list[i],
                        data: [percent_list[i], 100 - percent_list[i]],

                    }]
                },
                // make the dougnut size 200x200
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        title: {
                            display: true,
                            text: task_list[i]
                        }
                    },
                    backgroundColor: [
                        'rgb(0, 255, 0)',
                        'rgb(255, 255, 255)',
                    ],
                }
            });
            document.getElementById(`doughnuts-${camper_list[j]}`).append(canvas);
        }
    }
});