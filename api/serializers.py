from rest_framework.serializers import ModelSerializer
from base.models import Menu, News

class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News 
        fields = '__all__'

        