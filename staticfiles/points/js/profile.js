document.addEventListener('DOMContentLoaded', () => {
    
    const totals = document.getElementById('myChart');

    const tasks = document.querySelectorAll('.task');
    const percents = document.querySelectorAll('.percent');

    let task_list = []
    for (let i = 0; i < tasks.length; i++) {
        task_list.push(tasks[i].innerHTML);
    }

    let percent_list = []
    for (let i = 0; i < percents.length; i++) {
        percent_list.push(percents[i].innerHTML);
    }
  
    new Chart(totals, {
      type: 'bar',
      data: {
        labels: task_list,
        datasets: [{
          label: 'Entire Summer, Percentage of Points Earned per Task',
          data: percent_list,
          borderWidth: 1,
          barPercentage: 0.75,
        }]
      },
      options: {
        indexAxis: 'y',
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });

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
        document.getElementById('doughnuts').append(canvas);
    }
});