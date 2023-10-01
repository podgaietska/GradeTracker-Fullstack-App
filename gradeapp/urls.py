from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name="gradeapp"),
    path('add-course', views.add_course, name="add-course")
    
]