from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramUser, UserQuestion
from .serializers import TelegramUserSerializer, UserQuestionSerializer
from rest_framework.exceptions import NotFound

class TelegramUserListCreateView(generics.ListCreateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

class TelegramUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

class UserQuestionListCreateView(generics.ListCreateAPIView):
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer

class UserQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer

class TelegramUserByTelegramIdView(APIView):
    def get(self, request, *args, **kwargs):
        # Получаем telegramId из query параметров
        telegram_id = request.query_params.get('telegramId')
        
        if not telegram_id:
            return Response({"detail": "telegramId parameter is required."}, status=400)
        
        try:
            # Ищем пользователя по telegramId
            user = TelegramUser.objects.get(tgId=telegram_id)
        except TelegramUser.DoesNotExist:
            raise NotFound("User with this telegramId not found.")
        
        # Сериализуем пользователя и возвращаем данные
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Получаем telegramId из query параметров
        telegram_id = request.query_params.get('telegramId')
        
        if not telegram_id:
            return Response({"detail": "telegramId parameter is required."}, status=400)
        
        try:
            # Ищем пользователя по telegramId
            user = TelegramUser.objects.get(tgId=telegram_id)
        except TelegramUser.DoesNotExist:
            raise NotFound("User with this telegramId not found.")
        
        # Обновляем данные пользователя
        serializer = TelegramUserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Получаем telegramId из query параметров
        telegram_id = request.query_params.get('telegramId')
        
        if not telegram_id:
            return Response({"detail": "telegramId parameter is required."}, status=400)
        
        try:
            # Ищем пользователя по telegramId
            user = TelegramUser.objects.get(tgId=telegram_id)
        except TelegramUser.DoesNotExist:
            raise NotFound("User with this telegramId not found.")
        
        # Удаляем пользователя
        user.adelete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class GenerateQuizWithGPT(APIView):
    def get(self, request):
        return Response({"GPT": "Версия чата-гпт 4.о"})
    def post(self, request):
        # Получаем текст из тела запроса
        text = request.data.get('text')
        
        if not text:
            return Response({"detail": "Text parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Возвращаем ответ с принятым текстом
        return Response({"GPT": "Обработанный текст: " + text})
