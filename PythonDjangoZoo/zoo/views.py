import json
import aiohttp
from django.shortcuts import render
from .promt import create_promt
from rest_framework import generics
from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QuizResult, TelegramUser, UserQuestion
from .serializers import TelegramUserSerializer, UserQuestionSerializer, QuizResultSerializer
from rest_framework.exceptions import NotFound 
from async_requests import ArequestPost, ArequestPostGPT
from decouple import config
from rest_framework.permissions import IsAuthenticated



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
        telegram_id = request.query_params.get('telegramId')
        
        if not telegram_id:
            return Response({"detail": "telegramId parameter is required."}, status=400)
        
        try:
            user = TelegramUser.objects.get(tgId=telegram_id)
        except TelegramUser.DoesNotExist:
            raise NotFound("User with this telegramId not found.")
        
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        telegram_id = request.query_params.get('telegramId')
        
        if not telegram_id:
            return Response({"detail": "telegramId parameter is required."}, status=400)
        
        try:
            user = TelegramUser.objects.get(tgId=telegram_id)
        except TelegramUser.DoesNotExist:
            raise NotFound("User with this telegramId not found.")
        
        serializer = TelegramUserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        telegram_id = request.query_params.get('telegramId')
        
        if not telegram_id:
            return Response({"detail": "telegramId parameter is required."}, status=400)
        
        try:
            user = TelegramUser.objects.aget(tgId=telegram_id)
        except TelegramUser.DoesNotExist:
            raise NotFound("User with this telegramId not found.")
        
        user.adelete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class TelegramUserAdminView(APIView):
    def get(self, request, *args, **kwargs):  
        try:
            admins = TelegramUser.objects.filter(isAdmin=True)
        except TelegramUser.DoesNotExist:
            raise NotFound("Error...")
        
        serializer = TelegramUserSerializer(admins, many=True)  
        return Response(serializer.data)

class GenerateQuizWithGPT(APIView):
    async def get(self, request):
        return Response({"GPT": "Версия чата-гпт 4.о"})

    async def post(self, request):

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {config('ya_token')}"
        }
        promt = await create_promt(
            """Мне нужно сгенерировать 10 вопрос для викторины 'Какое животное подходит для тебя' с 4 вариантами ответов. 
            Правильного варианта ответа нет, т.к исходя из ответа мы будем подбирать для пользователя наиболее подходящее животно. """, 
            """Ты человек, который проводит викторины касательно животных. Мне нужно сгенерировать 10 вопрос для викторины "Какое животное подходит для тебя" с 4 вариантами ответов. Правильного варианта ответа нет, т.к исходя из ответа мы будем подбирать для пользователя наиболее подходящее животно. Ответ выдай в формате json:
        [
        {
            "number": 1,
            "question": "Какую среду обитания ты предпочитаешь?",
            "options": [
            "Лес",
            "Море",
            "Пустыня",
            "Горы"
            ]
        },
        {
            "number": 2,
            "question": "Какой уровень активности тебе больше подходит?",
            "options": [
            "Очень активный",
            "Умеренно активный",
            "Редко активный",
            "Пассивный"
            ]
        }
        ]""")
        response = await ArequestPost(url, json=promt, headers=headers)
        result = response
        rez = result["result"]["alternatives"][0]["message"]["text"]
        rez = rez.replace("`", "")
        data = json.loads(rez)
        return Response(data)
    



class GenerateAnimalFromQuestionAnswerWithGPT(APIView):
    async def post(self, request):
        answers = request.data.get('answers')
        if not answers:
            return Response({"detail": "Answers parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {config('ya_token')}"
        }
        promt = await create_promt(
            """Основываясь на ответах на вопросы подбери наиболее подходящее животное, которое можно взять из приюта.""", 
            f"""Ты человек, который проводит викторины касательно животных. Основываясь на этих ответах на вопросы подбери наиболее подходящее животное, которое можно взять из приюта. Также дай рекомендации по уходу (если животное крайне сложно в уходе, то вежливо предложи рассмотреть еще вариант). 
            {answers}""" + """Ответ должен быть в формате json:
            {
                "suggested_animal": "",
                "reasoning": {
                    "habitat_preference": "",
                    "activity_level": "",
                    "diet": "",
                    "social_preference": "",
                    "lifestyle": "",
                    "important_values": ""
                },
                "care_recommendations": {
                    "exercise": "",
                    "diet": "",
                    "housing": "",
                    "attention": "",
                    "grooming": "",
                    "health": ""
                }
            }""")
        
        print("""Основываясь на ответах на вопросы подбери наиболее подходящее животное, которое можно взять из приюта.""" + f"""Ты человек, который проводит викторины касательно животных. Основываясь на этих ответах на вопросы подбери наиболее подходящее животное, которое можно взять из приюта. Также дай рекомендации по уходу (если животное крайне сложно в уходе, то вежливо предложи рассмотреть еще вариант). 
            {answers}""" + """Ответ должен быть в формате json:
            {
                "suggested_animal": "",
                "reasoning": {
                    "habitat_preference": "",
                    "activity_level": "",
                    "diet": "",
                    "social_preference": "",
                    "lifestyle": "",
                    "important_values": ""
                },
                "care_recommendations": {
                    "exercise": "",
                    "diet": "",
                    "housing": "",
                    "attention": "",
                    "grooming": "",
                    "health": ""
                }
            }""")
        response = await ArequestPost(url, json=promt, headers=headers)
        result = response
        rez = result["result"]["alternatives"][0]["message"]["text"]
        rez = rez.replace("`", "")
        print(rez)
        data = json.loads(rez)
        return Response(data)
    



class QuizResultView(APIView):

    def post(self, request):
        print(request.data)
        try:
            tg_id = request.data.get("tgId")
            user = TelegramUser.objects.get(tgId=tg_id) 
            print(f"{user}")
        except TelegramUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        data['user'] = user.id  
        serializer = QuizResultSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, tg_id):
        try:
            # Получаем пользователя по Telegram ID
            user = TelegramUser.objects.get(tgId=tg_id)
        except TelegramUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем результаты викторин для пользователя
        quiz_results = QuizResult.objects.filter(telegramUser=user)
        serializer = QuizResultSerializer(quiz_results, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
