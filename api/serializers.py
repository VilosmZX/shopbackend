from rest_framework.serializers import ModelSerializer
from base.models import Menu

class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'