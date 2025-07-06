document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#sheet-type').addEventListener('change', () => {
        show_parent_view(document.querySelector('#sheet-type').value);
    });

    document.querySelectorAll('.element-display').forEach(elem => {
        elem.onchange = () => {
            show_view(elem.value);
        }
    });

    const add_new_task_elems = document.querySelectorAll('.edit-task');
    add_new_task_elems.forEach(elem => {
        elem.style.display = 'none';
    });

    const add_task_buttons = document.querySelectorAll('.add-new-task-button');
    add_task_buttons.forEach(button => {
        button.onclick = () => {
            create_new_task(button, add_new_task_elems);
        }
    });

    const edit_task_buttons = document.querySelectorAll('.edit-tasks-button');
    edit_task_buttons.forEach(button => {
        button.onclick = () => {
            edit_tasks(button);
        }
    });

    const cancel_task_changes_button = document.querySelectorAll('.cancel-task-changes-button');
    cancel_task_changes_button.forEach(button => {
        button.onclick = () => {
            cancel_edit(button);
        }
    });

    const is_active_checkboxes = document.querySelectorAll('[name="task-active-checkbox"]');
    is_active_checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            set_active(checkbox);
        });
    });

    document.querySelectorAll('.num-update').forEach(checkbox => {
        checkbox.onchange = () => {
            total(checkbox.dataset.str);
        }
    });

    document.querySelectorAll('.non-generic').forEach(input => {
        input.onchange = () => { 
            unmark_generic(input)
        }
    });

    document.querySelectorAll('.total').forEach(span => {
        total(span.dataset.str)
    });

    show_parent_view(document.querySelector('#sheet-type').value)
    add_listeners_to_delete_task_buttons();
    add_listeners_to_sequence_input();

});


function add_listeners_to_delete_task_buttons() {
    const delete_task_buttons = document.querySelectorAll('.bi-trash');
    delete_task_buttons.forEach(button => {
        button.onclick = () => {
            delete_task_line(button);
        }
    });
}


function add_listeners_to_sequence_input() {
    const sequence_inputs = document.querySelectorAll('[name="task-sequence"]');
    sequence_inputs.forEach(button => {
        button.onchange = () => {
            update_sequence(button);
        }
    });
}


function show_parent_view(view) {
    document.querySelectorAll('.parent-view').forEach(view => {
        view.style.display = 'none';
    });
    let elem_to_display = document.querySelector(`#${view}-view`);
    elem_to_display.style.display = ''
    let child_elem_selector = elem_to_display.querySelector('.element-display');
    show_view(child_elem_selector.value);
}


function show_view(view) {
    console.log(view)
    document.querySelectorAll('.child-view').forEach(view => {
        view.style.display = 'none';
    });
    let elem_to_display = document.querySelector(`#${view}-view`);
    elem_to_display.style.display = ''
}


function create_new_task(button) {

    // Call the edit_tasks function to hide the original task lines and show the new task elements
    edit_tasks(button);
    
    let task_table = button.parentElement;

    // Get the last sequence number and create a new task line
    let current_last_sequence = parseInt(task_table.querySelector('.task-line:last-child').querySelector('.task-line-sequence').querySelector('input').value) + 1;

    new_task_line = document.createElement('tr');

    // Add the new task line with some of the generic details
    new_task_html = `
    <tr class="edit-task edit-task-tbody">\
    <input type="hidden" name="task-line-id" value="false">\
    <input type="hidden" name="task-action" value="create">`

    // If the button value is not generic, add the active checkbox
    if (button.value && button.value != 'generic') {
        new_task_html += `<td class="task-line-active">\
        <input type="checkbox" name="task-active-checkbox" checked class="non-generic">\
        <input type="hidden" name="task-active" value="True">\
        </td>`
    }

    // Add some more generic details
    new_task_html += `
    <td class="task-line-sequence"><input type="number" name="task-sequence" value="${current_last_sequence}" placeholder="${current_last_sequence}" required></td>\
    <td><input type="text" name="task-name" placeholder="Task" required></td>\
    <td><input type="number" name="task-points" min="0" max="99" placeholder="Value" required></td>`
    
    // If the button is not masterlist or generic, add the task type selector
    if (button.value && button.value != 'masterlist' && button.value != 'generic') {
        unmark_generic(button);
        new_task_html += `<td class="task-line-input-type">\
                            <select id="input-type-{{ blank_line.task.id }}" name="task-input-type" class="non-generic">\
                                <option value="checkbox">Checkbox</option>\
                                <option value="custom">Select Number</option>\
                            </select></td>`
    }

    new_task_html += `
    <td><i class="btn btn-sm btn-outline-danger bi bi-trash"></i></td>
    </tr>`;

    new_task_line.innerHTML = new_task_html;
    new_task_line.classList.add('new-task', 'task-line', 'edit-task');

    task_table.querySelector('tbody').appendChild(new_task_line);

    add_listeners_to_delete_task_buttons();
    add_listeners_to_sequence_input();
}


function edit_tasks(button) {

    let task_table = button.parentElement;
    
    // Find and hide the original task lines
    let original_tasks = task_table.querySelectorAll('.task-tbody');
    original_tasks.forEach(task => {
        task.style.display = 'none';
    });

    // Show the new task elements
    let add_new_task_elems = button.parentElement.querySelectorAll('.edit-task');
    add_new_task_elems.forEach(elem => {
        elem.style.display = '';
    });
}


function update_sequence(button) {
    let task_line = button.parentElement.parentElement;
    let original_sequence = task_line.querySelector('[name="task-sequence"]').dataset.ovalue;
    let sequence = task_line.querySelector('[name="task-sequence"]').value;
    let task_table = button.parentElement.parentElement.parentElement;

    let existing_seqeunces = task_table.querySelectorAll('[name="task-sequence"]');

    existing_seqeunces.forEach(seq => {
        if (seq == button) {
            return;
        }
        if (seq.value > original_sequence) {
            seq.dataset.ovalue = parseInt(seq.value) - 1;
            seq.value = parseInt(seq.value) - 1;
        }
        if (seq.value >= sequence) {
            seq.dataset.ovalue = parseInt(seq.value) + 1;
            seq.value = parseInt(seq.value) + 1;
        }

    });
}


function cancel_edit(button) {
    let task_table = button.parentElement;

    // Find and show the original task lines
    let original_tasks = task_table.querySelectorAll('.task-tbody');
    original_tasks.forEach(task => {
        task.style.display = '';
    });

    // Hide the new task elements
    let add_new_task_elems = button.parentElement.querySelectorAll('.edit-task');
    add_new_task_elems.forEach(elem => {
        elem.style.display = 'none';
    });
}


function set_active(checkbox) {
    let task_line = checkbox.parentElement
    let input = task_line.querySelector('[name="task-active"]');
    if (checkbox.checked) {
        input.value = 'True';
    } else {
        input.value = 'False';
    }
}


function delete_task_line(button) {
    let task_line = button.parentElement.parentElement;
    let task_id = task_line.querySelector('[name="task-line-id"]');
    if (confirm('Are you sure you want to delete this task?')) {
        if (task_id.value != 'false') {
                task_line.querySelector('[name="task-action"]').value = 'delete';
                task_line.style.display = 'none';
        } else {
            // remove the line html from the page
            task_line.remove();
        }
    }
}


function total(str) {
    let total = 0;
    document.querySelectorAll(`[data-str=${str}]`).forEach(checkbox => {
        if (checkbox.checked) {
            total += parseInt(checkbox.dataset.value);
        }
    });
    document.querySelector(`#${str}-total`).innerHTML = total;
}


function unmark_generic(input) {
    // get parent div of input
    let parent = input.closest('.child-view');
    // if there is an input in the div with 'use-generic in the name, uncheck it
    if (parent.querySelector('[name*="use-generic"]')) {
        parent.querySelector('[name*="use-generic"]').checked = false;
    }
}