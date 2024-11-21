from django.urls import path
from .views import (
    TelegramUserByTelegramIdView,
    TelegramUserListCreateView, 
    TelegramUserDetailView, 
    UserQuestionListCreateView,
    UserQuestionDetailView,
    GenerateQuizWithGPT
)

urlpatterns = [
    path('zoo/telegram-user/create', TelegramUserListCreateView.as_view(), name='user_list_create'),
    path('zoo/telegram-user/<int:pk>/', TelegramUserDetailView.as_view(), name='user_detail'),
    path('zoo/questions-create', UserQuestionListCreateView.as_view(), name='hello_world'),
    path('zoo/questions-list', UserQuestionDetailView.as_view(), name='hello_world'),
    path('zoo/generate-quiz', GenerateQuizWithGPT.as_view(), name='hello_world'),
     path('zoo/telegram-user/', TelegramUserByTelegramIdView.as_view(), name='user-detail-by-tgId'),
]
