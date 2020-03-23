from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # added by me
    completedTasks = models.IntegerField(default=0)
    tasksOutstanding = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)

    # Who traks the user's tasks
    associatedUser = models.ManyToManyField('self', blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email.split("@")[0]