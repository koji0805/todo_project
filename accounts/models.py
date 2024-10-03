from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('accounts:home')

class Todo(models.Model):
    title = models.CharField("タスク名", max_length=30)
    description = models.TextField("詳細", blank=True)
    deadline = models.DateTimeField("締切")
    urgency = models.IntegerField('緊急度',choices=[(i, i) for i in range(1, 6)], default=3)
    importance = models.IntegerField('重要度',choices=[(i, i) for i in range(1, 6)], default=3)
    user = models.ForeignKey(
        'accounts.Users',on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
    
    def is_past_due(self):
        return self.deadline < timezone.now()
    
    def is_approaching_deadline(self):
        return timezone.now() > self.deadline - timezone.timedelta(days=3)