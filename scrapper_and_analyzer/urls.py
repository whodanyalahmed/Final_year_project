from django.urls import path
from . import views
urlpatterns = [

    # call the index function
    path('', views.home, name='Dashboard'),
    path('results', views.result, name='results'),
    path('minimum', views.Minimum, name="minimum")
    # path('app/', index, name='home'),
]
