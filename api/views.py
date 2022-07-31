from uuid import uuid4
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import MenuSerializer, Menu, NewsSerializer, News
from rest_framework import status
import pyrebase
from requests.utils import requote_uri

from api import serializers

config = {
    'apiKey': "AIzaSyBAMLQ1dz5oblsp0fRhimciOBC6HY_ES84",
    'authDomain': "myweb-59a0a.firebaseapp.com",
    'projectId': "myweb-59a0a",
    'storageBucket': "myweb-59a0a.appspot.com",
    'messagingSenderId': "324236950024",
    'appId': "1:324236950024:web:8ca9dd3b7872427f21afbd",
    'measurementId': "G-3F334QY1NB",
    'databaseURL': '',
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]
    return Response(routes)


@api_view(['GET'])
def getMenu(request):
    menus = Menu.objects.all()
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)
    

@api_view(['POST'])
def addMenu(request): 
    generated_id = uuid4()
    image_name = f'image/food_{request.data["title"]}_{generated_id}'
    data = storage.child(image_name).put(request.data['image'])
    image_url = storage.child(image_name).get_url(data['downloadTokens'])
    image_url = requote_uri(image_url)
    request.data['image'] = image_url
    request.data['token'] = data['downloadTokens']
    menu = MenuSerializer(data=request.data)
    if menu.is_valid():
        menu.validated_data['id'] = generated_id
        obj = menu.save()
        return Response(menu.data, status=status.HTTP_201_CREATED)
    else:
        print('error', menu.errors)
        return Response(menu.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getNews(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addNews(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteFood(request, id):
    try:
        instance = Menu.objects.get(id=id)
        image_name = f'image/food_{instance.title}_{instance.id}'
        storage.delete(image_name, instance.token)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
