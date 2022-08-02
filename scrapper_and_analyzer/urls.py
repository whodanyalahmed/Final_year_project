from django.urls import path
from . import views
urlpatterns = [

    # call the index function
    path('', views.home, name='index'),
    path('results', views.result, name='results'),
    # path('app/', index, name='home'),
]
