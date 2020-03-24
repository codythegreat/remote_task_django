$(document).ready(() => {
    var comingUp = $('#legend-coming-up-text')
    var pastDue = $('#legend-past-due-text')
    var complete = $('#legend-completed-text')
    var task = $('.task')
    var teamTasks = $('#team-member-tasks')
    var teamMembersContainer = $('#team-member-container')

    // on click of legend item, toggle corresponding tasks and line-through legend item
    comingUp.click( () => {
        if (comingUp.css('text-decoration').includes('line-through')) {comingUp.css('text-decoration', 'unset');}
        else {comingUp.css('text-decoration', 'line-through');}
        $('.task-noncomplete').toggle();
    });
    pastDue.click( () => {
        if (pastDue.css('text-decoration').includes('line-through')) {pastDue.css('text-decoration', 'unset');}
        else {pastDue.css('text-decoration', 'line-through');}
        $('.task-past-due').toggle();
    });
    complete.click( () => {
        if (complete.css('text-decoration').includes('line-through')) {complete.css('text-decoration', 'unset');}
        else {complete.css('text-decoration', 'line-through');}
        $('.task-complete').toggle();
    });

    // On sidebar task click, toggle the description and complete button
    task.find('.task-enlarge-button').click(function() {
        if ($( this ).html() == '▲') {
            $( this ).html('▼');
        } else {
            $( this ).html('▲');
        }
        $( this ).parent().find('.comment').toggle();
        $( this ).parent().find('.desc').toggle();
        $( this ).parent().find('input.task-to-complete').css('display', 'none');
        $( this ).parent().find('input.task-to-comment').css('display', 'none');
        $( this ).parent().find('form').toggle();
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