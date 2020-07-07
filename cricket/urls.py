from django.urls import path , include
from cricket import views

app_name='cricket'

urlpatterns = [
    path('<int:id>/', views.index, name='index'),
    path('search/', views.player_search, name='player_search'),
]

