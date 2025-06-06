from django.urls import path
from chatbot.views import RegisterView, LoginView, ChatView, ChatHistoryView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('chat/', ChatView.as_view()),
    path('chat/history/', ChatHistoryView.as_view()),  # 👈 This one
]
