from django.db import models

class UserQuestion(models.Model):
    userQuestion = models.TextField()
    date = models.DateTimeField()
    telegramUser = models.ForeignKey(
        'TelegramUser', 
        on_delete=models.CASCADE, 
        related_name='questions', 
        verbose_name="Telegram User"
    )
    def __str__(self):
        return f"Question by {self.telegramUser} on {self.date}"


class TelegramUser(models.Model):
    tgId = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    userName = models.CharField(max_length=150, verbose_name="Username")
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Name")
    secondName = models.CharField(max_length=150, blank=True, null=True, verbose_name="Second Name")
    registrationDate = models.DateField(auto_now_add=True)
    email = models.CharField(max_length=50, blank=True, null=True,)
    phoneNumber = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.userName if self.userName else f"User {self.tgId}"
