from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework.generics import CreateAPIView
from .models import User

class SignUpView(CreateAPIView):
    queryset=User.objects.all()
    serializer_class=SignUpSerializer
    
