from uuid import uuid4
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import MenuSerializer, Menu
from rest_framework import status
import pyrebase
from requests.utils import requote_uri


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
    firebase = pyrebase.initialize_app(config)
    generated_id = uuid4()
    image_name = f'image/food_{request.data["title"]}_{generated_id}'
    storage = firebase.storage()
    data = storage.child(image_name).put(request.data['image'])
    image_url = storage.child(image_name).get_url(data['downloadTokens'])
    image_url = requote_uri(image_url)
    menu = MenuSerializer(data=request.data)
    request.data['image'] = image_url
    if menu.is_valid():
        
        menu.validated_data['id'] = generated_id
        obj = menu.save()
        return Response(menu.data, status=status.HTTP_201_CREATED)
    else:
        print('error', menu.errors)
        return Response(menu.errors, status=status.HTTP_400_BAD_REQUEST)