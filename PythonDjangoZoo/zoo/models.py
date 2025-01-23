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

class QuizAnswer(models.Model):
    telegramUser = models.ForeignKey(
        'TelegramUser', 
        on_delete=models.CASCADE, 
        related_name='QuizAnswer', 
        verbose_name="Telegram User"
    )
    question = models.TextField()  # Вопрос из викторины
    answer = models.TextField()  # Ответ пользователя
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания ответа

    def __str__(self):
        return f"{self.telegramUser.userName}: {self.question[:50]} - {self.answer[:50]}"


class QuizResult(models.Model):
    telegramUser = models.ForeignKey(
        'TelegramUser', 
        on_delete=models.CASCADE, 
        related_name='QuizResult', 
        verbose_name="Telegram User"
    )
    answers = models.ManyToManyField(
        'QuizAnswer', 
        related_name='QuizResult', 
        verbose_name="Quiz Answer"
    )
    suggested_animal = models.CharField(max_length=255)  # Рекомендованное животное
    reasoning = models.JSONField()  # Обоснование результата (полный JSON)
    care_recommendations = models.JSONField()  # Рекомендации по уходу (полный JSON)
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания результата

    def __str__(self):
        return f"{self.telegramUser.userName}: {self.suggested_animal}"
    

class TelegramUser(models.Model):
    tgId = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    userName = models.CharField(max_length=150, verbose_name="Username")
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Name")
    secondName = models.CharField(max_length=150, blank=True, null=True, verbose_name="Second Name")
    registrationDate = models.DateField(auto_now_add=True)
    email = models.CharField(max_length=50, blank=True, null=True,)
    phoneNumber = models.CharField(max_length=50, blank=True, null=True)
    isAdmin = models.BooleanField(default=False)
    def __str__(self):
        return self.userName if self.userName else f"User {self.tgId}"
