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
            createForm = CreateTaskForm(request.POST)
            completeForm = CompleteTaskForm(request.POST)
            createTeamForm = CreateTeamForm(request.POST)
            joinTeamForm = JoinTeamForm(request.POST)
            commentOnTaskForm = CommentOnTask(request.POST)
            if createForm.is_valid():
                title = createForm.cleaned_data['title']
                desc = createForm.cleaned_data['desc']
                endDate = createForm.cleaned_data['endDate']
                t = Task(title=title, description=desc, endDate=endDate, startDate=datetime.datetime.now(), createdOnDate=datetime.datetime.now(), parentUser=request.user)
                request.user.tasksOutstanding += 1
                request.user.save()
                t.save()
                return redirect('index')
            elif completeForm.is_valid():
                taskToComplete = Task.objects.get(pk=completeForm.cleaned_data['taskId'])
                taskToComplete.complete = True
                taskToComplete.completeDate = datetime.datetime.now()
                taskToComplete.save()
                request.user.tasksOutstanding -= 1
                request.user.completedTasks += 1
                request.user.save()
                return redirect('index')
            elif createTeamForm.is_valid():
                name = createTeamForm.cleaned_data['name']
                private = createTeamForm.cleaned_data['private']
                t = Team(name=name, private=private, owner=request.user)
                t.save()
                t.users.set([request.user])
                t.save()
                return redirect('index')
            elif joinTeamForm.is_valid():
                teamPK = joinTeamForm.cleaned_data['teamPrimKey']
                t = Team.objects.get(pk=teamPK)
                if not t.private:
                    t.users.add(request.user)
                t.save()
                return redirect('index')
            elif commentOnTaskForm.is_valid():
                parentTask = commentOnTaskForm.cleaned_data['parentTask']
                content = commentOnTaskForm.cleaned_data['content']
                t = Task.objects.get(pk=parentTask)
                c = Comment(parentUser=request.user, parentTask=t, content=content)
                c.save()
                t.comments.add(c)
                return redirect('index')
            else:
                return redirect('index')

        # on GET or redirect, simply build the context and return
        else:
            # return the rendered html file with the context
            return render(request, 'index.html', context=buildIndexContext(request))

    # if user not authenticated, redirect to login page
    else:
        return redirect('login')
    

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