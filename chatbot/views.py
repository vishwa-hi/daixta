import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer

# OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            message = request.data.get("message")
            if not message:
                return Response({"error": "Message is required."}, status=400)

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",  # Required by OpenRouter
                "X-Title": "daixtabot-chat"
            }

            payload = {
                "model": "mistralai/mixtral-8x7b-instruct",  # You can change the model
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            }

            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            reply = data["choices"][0]["message"]["content"]

            chat = ChatHistory.objects.create(user=request.user, message=message, response=reply)
            return Response(ChatHistorySerializer(chat).data)

        except Exception as e:
            print(f"[OpenRouter ERROR]: {e}")
            return Response({"error": "AI response failed."}, status=500)


class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_history = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
        serializer = ChatHistorySerializer(chat_history, many=True)
        return Response(serializer.data)
    
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer