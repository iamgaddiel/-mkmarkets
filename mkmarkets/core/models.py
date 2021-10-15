from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} | balance: {self.balance}"

