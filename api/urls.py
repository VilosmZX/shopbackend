from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.getRoutes),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/r/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('menus/', views.getMenu, name = 'menu'),
    path('add-menu/', views.addMenu, name = 'addmenu'),
    path('news/', views.getNews, name='news'),
    path('add-news/', views.addNews, name = 'addnews'),
    path('delete-menu/<str:id>/', views.deleteFood, name = 'deleteFood')
] 