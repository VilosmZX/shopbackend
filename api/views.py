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
    menu = MenuSerializer(data=request.data)
    if menu.is_valid():
        menu.save()
        return Response(menu.data, status=status.HTTP_201_CREATED)
    else:
        print('error', menu.errors)
        return Response(menu.errors, status=status.HTTP_400_BAD_REQUEST)