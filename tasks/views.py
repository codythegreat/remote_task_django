from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
# for performing search functions:
from django.db.models import Q
# for displaying error messages on bad form input
from django.contrib import messages 

# task model that is used on index page
from tasks.models import Task, Comment, Team

# customuser model for saving stats on task actions
from users.models import CustomUser

# Create new task, complete task, and create new team forms
from tasks.forms import CreateTaskForm, CompleteTaskForm, CreateTeamForm, JoinTeamForm, CommentOnTask

# for saving form inputs
import datetime


def index(request):
    # check if the user is authenticated
    if request.user.is_authenticated:
        # On post, parse the form and return a redirect to the same page (GET method)
        if request.method == 'POST':

            # forms we'll use on the index page
            createForm = CreateTaskForm(request.POST)
            completeForm = CompleteTaskForm(request.POST)
            createTeamForm = CreateTeamForm(request.POST)
            joinTeamForm = JoinTeamForm(request.POST)
            commentOnTaskForm = CommentOnTask(request.POST)

            # if any form is valid, parse, then redirect back to index (GET request)
            if createForm.is_valid():
                parseCreateTaskForm(createForm, request.user)
                return redirect('index')
            elif completeForm.is_valid():
                parseCompleteTaskForm(completeForm, request.user)
                return redirect('index')
            elif createTeamForm.is_valid():
                parseCreateTeamForm(createTeamForm, request.user)
                return redirect('index')
            elif joinTeamForm.is_valid():
                parseJoinTeamForm(joinTeamForm, request.user)
                return redirect('index')
            elif commentOnTaskForm.is_valid():
                parseCommentOnTaskForm(commentOnTaskForm, request.user)
                return redirect('index')
            else:
                return redirect('index')

        # on GET or redirect, simply build the context and return
        else:
            return render(request, 'index.html', context=buildIndexContext(request))

    # if user not authenticated, redirect to login page
    else:
        return redirect('login')
    
# parse the create task form
def parseCreateTaskForm(form, user):
    title = form.cleaned_data['title']
    desc = form.cleaned_data['desc']
    endDate = form.cleaned_data['endDate']
    t = Task(
        title=title, 
        description=desc, 
        endDate=endDate, 
        startDate=datetime.datetime.now(), 
        createdOnDate=datetime.datetime.now(), 
        parentUser=user
    )
    user.tasksOutstanding += 1
    user.save()
    t.save()

# parse the complete task form
def parseCompleteTaskForm(form, user):
    taskToComplete = Task.objects.get(pk=form.cleaned_data['taskId'])
    taskToComplete.complete = True
    taskToComplete.completeDate = datetime.datetime.now()
    taskToComplete.save()
    user.tasksOutstanding -= 1
    user.completedTasks += 1
    user.save()

# parse the create team form
def parseCreateTeamForm(form, user):
    name = form.cleaned_data['name']
    private = form.cleaned_data['private']
    t = Team(name=name, private=private, owner=user)
    t.save()
    t.users.set([user])
    t.save()

# parse the join team form
def parseJoinTeamForm(form, user):
    teamPK = form.cleaned_data['teamPrimKey']
    t = Team.objects.get(pk=teamPK)
    if not t.private:
        t.users.add(user)
    t.save()

# parse comment on task form
def parseCommentOnTaskForm(form, user):
    parentTask = form.cleaned_data['parentTask']
    content = form.cleaned_data['content']
    t = Task.objects.get(pk=parentTask)
    c = Comment(parentUser=user, parentTask=t, content=content)
    c.save()
    t.comments.add(c)

# Search function for adding a team
def getTeamQuerySet(query=None):
    querySet = []
    queries = query.split(" ")
    for q in queries:
        teams = Team.objects.filter(
            Q(name__icontains=q)
        ).distinct()
        for team in teams:
            querySet.append(team)
    return list(set(querySet))

# based on request, builds and returns a context for index page
def buildIndexContext(request):
    tasks = Task.objects.filter(parentUser=request.user)
    tasksIncomplete = len(Task.objects.filter(parentUser=request.user, complete=False).order_by("-startDate"))
    taskComments = Comment.objects.filter(parentTask__in=tasks)
    numTasks = len(Task.objects.filter(parentUser=request.user))
    
    if (Team.objects.filter(users__in=[request.user])) != None:
        team = Team.objects.filter(users__in=[request.user])
        teamTasks = []
        for t in team:
            teamTasks.append(Task.objects.filter(parentUser__in=t.users.all()))
    else:
        team = None
        teamTasks = None

    # context can be used for rendering data to the html templates
    context = {
        'tasks': tasks,
        'taskComments': taskComments,
        'numTasks': numTasks,   
        'taskIncomplete': tasksIncomplete,
        'tasksOutstanding': request.user.tasksOutstanding,
        'team': team,
        'teamTasks': teamTasks
    }

    # perform search function if user is searching
    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)
        if str(query) != "":
            context['teamQueries'] = getTeamQuerySet(str(query))
    return context