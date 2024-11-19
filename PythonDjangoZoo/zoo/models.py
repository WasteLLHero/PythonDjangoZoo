from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Username")

    def __str__(self):
        return self.username if self.username else f"User {self.tg_id}"