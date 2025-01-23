from django.urls import path
from .views import (
    GenerateAnimalFromQuestionAnswerWithGPT,
    QuizResultView,
    TelegramUserAdminView,
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
    path('zoo/questions-create', UserQuestionListCreateView.as_view(), name='questions_create'),
    path('zoo/questions-list', UserQuestionDetailView.as_view(), name='questions_list'),
    path('zoo/generate-quiz', GenerateQuizWithGPT.as_view(), name='quiz_generate'),
    path('zoo/generate-animal-by-quiz', GenerateAnimalFromQuestionAnswerWithGPT.as_view(), name='generate_animal_by_quiz'),
    path('zoo/telegram-user/', TelegramUserByTelegramIdView.as_view(), name='user_detail_by_tgId'),
    path('zoo/telegram-admin/', TelegramUserAdminView.as_view(), name='user_admin'),
    path('zoo/quiz-results/', QuizResultView.as_view(), name='quiz_results_create'),
    path('zoo/quiz-results/<int:tg_id>/', QuizResultView.as_view(), name='quiz_results'),
]
