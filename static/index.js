// toggles line-through css property of parameter
const toggleLegendLineThrough = (legendElement) => {
    if (legendElement.css('text-decoration').includes('line-through')) {
        legendElement.css('text-decoration', 'unset');
    } else {
        legendElement.css('text-decoration', 'line-through');
    }
};

// ternary changes direction of arrow base on previous value
const changeTaskEnlargeButtonArrowDirection = (taskEnlargeButton) => {
    taskEnlargeButton.html(
        taskEnlargeButton.html() == '▲' ? '▼' : '▲'
    );
};

// on task toggle, show hide these elements
const toggleHiddenChildrenOnTask = (task) => {
    task.find('.comment').toggle();
    task.find('.desc').toggle();
    task.find('form').toggle();
};

// on task toggle, always hide form ID inputs
const hideTaskIdFormInputs = (task) => {
    task.find('input.task-to-complete').css('display', 'none');
    task.find('input.task-to-comment').css('display', 'none');
};

$(document).ready(() => {
    // clickable legend elements
    var legendComingUp = $('#legend-coming-up-text');
    var legendPastDue = $('#legend-past-due-text');
    var legendComplete = $('#legend-completed-text');

    // tasks that are toggled by clicking legend elems
    var tasksNonComplete = $('.task-noncomplete');
    var tasksComplete = $('.task-complete');
    var tasksPastDue = $('.task-past-due');

    // toggle button for task to enlarge / minimize
    var taskEnlargeButton = $('.task-enlarge-button');


    var teamTasks = $('#team-member-tasks');
    var teamMembersContainer = $('#team-member-container');

    // on click of legend item, line-through legend and toggle associated tasks
    legendComingUp.click( () => {
        toggleLegendLineThrough(legendComingUp);
        tasksNonComplete.toggle();
    });
    legendPastDue.click( () => {
        toggleLegendLineThrough(legendPastDue);
        tasksPastDue.toggle();
    });
    legendComplete.click( () => {
        toggleLegendLineThrough(legendComplete);
        tasksComplete.toggle();
    });

    // On sidebar task click, toggle the description and complete button task.find('.task-enlarge-button').
    taskEnlargeButton.click(function() {
        changeTaskEnlargeButtonArrowDirection($( this ));
        toggleHiddenChildrenOnTask($( this ).parent());
        hideTaskIdFormInputs($( this ).parent());
    });

    // on click of create task button, check fields for errors
    $('#create-task-submit').submit(function() {
        if ($('#create-task-title').val().length < 1) {
            $('#create-task-error').html('My Error Message').toggle();
            return false;
        }
        if ($('#create-task-date').val().length < 1) {
            $('#create-task-error').html('My Error Message').toggle();
            return false;
        }
    });

    // for both team members and tasks, if none, display none found message
    if (teamMembersContainer.children().length == 0) {
        teamMembersContainer.append('<p>No Team Members Found</p>');
    }
    if (teamTasks.children().length == 0) {
        // normal line height if no tasks to be displayed
        teamTasks.css('line-height', 'unset');
        teamTasks.append('<p>No Team Member Tasks Found</p>');
    }
}); 
