from django.urls import path
from .views import IndexView, upgrade_me

app_name = 'protect'
urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('upgrade/', upgrade_me, name='upgrade'),

]
