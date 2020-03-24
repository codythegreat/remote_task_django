from django.db import models
from users.models import CustomUser
from datetime import datetime, timezone, timedelta


class Task(models.Model):
    # Type of task
    ROOT_TASK = 1
    SUB_TASK = 2
    REQ_COMPLETE_TASK = 3
    TASK_TYPE = (
        (ROOT_TASK, "Task"),
        (SUB_TASK, "Sub Task")
    )
    taskType = models.PositiveSmallIntegerField(
       choices=TASK_TYPE,
       default=1,
    )

    # primary person working on task
    parentUser = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    # title of the task
    title = models.CharField(max_length=255)

    # description of task (body)
    description = models.TextField(null=True, blank=True)

    # dates for task begining/end
    createdOnDate = models.DateTimeField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(null=True, blank=True)

    # related tasks (if root this is sub, and vice versa)
    relatedTasks = models.ManyToManyField('self', blank=True)

    # completion information
    complete = models.BooleanField(default=False)
    completeDate = models.DateTimeField(null=True, blank=True)

    # comments on the task itself
    comments = models.ManyToManyField('Comment', blank=True)

    # any files to be attached to the task
    files = models.ManyToManyField('FileAttachment', blank=True)

    def __str__(self):
        return self.title

    # return positive if root task
    def isRoot(self):
        return self.taskType == self.ROOT_TASK

    # return positive if sub task
    def isSub(self):
        return self.taskType == self.SUB_TASK

    # return positive if complete
    def isComplete(self):
        return complete

    # return true if end date and past due
    def isPastDue(self):
        return self.endDate < datetime.now(timezone.utc)

    def isDayOld(self):
        return self.startDate > datetime.now(timezone.utc) - timedelta(days=1)

    def isWeekOld(self):
        return self.startDate > datetime.now(timezone.utc) - timedelta(days=7)

    def isMonthOld(self):
        return self.startDate > datetime.now(timezone.utc) - timedelta(days=30)




class Team(models.Model):
    # name of the team
    name = models.CharField(max_length=255)

    # owner of the team
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='ownedTeam', null=True)

    # people in the team
    users = models.ManyToManyField('users.CustomUser', blank=True)

    # true if a team is private
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    # parent user of the post
    parentUser = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    # task that the user is replying to
    parentTask = models.ForeignKey('Task', on_delete=models.CASCADE)

    # text content of comment
    content = models.CharField(max_length=512)

    # any files to be attached to the comment
    files = models.ManyToManyField('FileAttachment', blank=True)

    # if replying to user, email is required
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.content

    # tells us if the comment is a reply
    def isReplyingToUser(self):
        return self.email != ''


class FileAttachment(models.Model):
    # the file attachment
    attachment = models.FileField(upload_to="uploads/%Y/%m/%d/")

    def __str__(self):
        return self.attachment.name