from django.urls import path
from . import views
urlpatterns = [

    # call the index function
    path('', views.home, name='Dashboard'),
    path('results', views.result, name='results'),
    path('minimum', views.Minimum, name="minimum"),
    path('maximum', views.maximum, name="maximum"),
    path('list', views._list, name="list"),
    path("list_results", views.list_results, name="list_result"),
    path('prediction', views.prediction, name="prediction"),

    # path('app/', index, name='home'),
]
