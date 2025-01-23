from rest_framework import serializers
from .models import TelegramUser, UserQuestion, QuizAnswer, QuizResult


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['id','tgId', 'userName', 'name', 'secondName', 'email', 'phoneNumber']
class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = '__all__'



class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ['question', 'answer']

class QuizResultSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True)  

    class Meta:
        model = QuizResult
        fields = ['telegramUser', 'suggested_animal', 'reasoning', 'care_recommendations', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        telegramUser = validated_data.pop('telegramUser')
        
        # Создаем объект QuizResult без answers
        quiz_result = QuizResult.objects.create(telegramUser=telegramUser, **validated_data)
        
        # Создаем объекты QuizAnswer и связываем их с QuizResult
        for answer_data in answers_data:
            answer = QuizAnswer.objects.create(telegramUser=telegramUser, **answer_data)
            quiz_result.answers.add(answer)
        
        return quiz_result