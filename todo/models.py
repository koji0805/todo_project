from django.db import models 

class Todo(models.Model):
    title = models.CharField("タスク名", max_length=30)
    description = models.TextField("詳細", blank=True)
    deadline = models.DateField("締切")
    user = models.ForeignKey(
        'accounts.Users',on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title