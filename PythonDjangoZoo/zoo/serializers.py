from rest_framework import serializers
from .models import TelegramUser, UserQuestion

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['tgId', 'userName', 'name', 'secondName', 'email', 'phoneNumber']
class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = '__all__'
